import { Component, signal, inject, OnDestroy, OnInit, ViewChild, ElementRef, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import * as mammoth from 'mammoth';

interface AnalysisResult {
  score: number;
  matched_skills: string[];
  missing_skills: string[];
  bonus_skills: string[];
  hiring_decision: string;
  recommendations: string;
  interview_questions: string[];
  red_flags: string[];
}

interface HistoryEntry {
  id: string;
  timestamp: number;
  cvFileName: string;
  jdSnippet: string;
  result: AnalysisResult;
}

const STORAGE_KEY = 'hr_assistant_history';

@Component({
  selector: 'app-root',
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit, OnDestroy {
  private http = inject(HttpClient);
  private sanitizer = inject(DomSanitizer);

  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

  cvFile: File | null = null;
  jobDescription = signal('');
  loading = signal(false);
  result = signal<AnalysisResult | null>(null);
  errorMessage = signal<string | null>(null);

  previewType = signal<'pdf' | 'docx' | null>(null);
  pdfPreviewUrl = signal<SafeResourceUrl | null>(null);
  docxHtml = signal<string | null>(null);
  previewOpen = signal(false);
  private blobUrl: string | null = null;

  jdCategories = signal<string[]>([]);
  selectedJdCategory = signal<string>('');
  jdLoading = signal(false);

  history = signal<HistoryEntry[]>([]);
  activeHistoryId = signal<string | null>(null);

  readonly historySortedByScore = computed(() =>
    [...this.history()].sort((a, b) => b.result.score - a.result.score)
  );

  constructor() {
    this.loadHistory();
  }

  ngOnInit(): void {
    this.http.get<{ categories: string[] }>('http://localhost:8000/job-descriptions').subscribe({
      next: (data) => this.jdCategories.set(data.categories),
      error: () => {},
    });
  }

  // ── History ──────────────────────────────────────────────

  private loadHistory(): void {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) this.history.set(JSON.parse(raw));
    } catch { }
  }

  private saveToHistory(result: AnalysisResult): void {
    const entry: HistoryEntry = {
      id: Date.now().toString(),
      timestamp: Date.now(),
      cvFileName: this.cvFile!.name,
      jdSnippet: this.jobDescription().trim().slice(0, 90),
      result,
    };
    const updated = [entry, ...this.history()].slice(0, 30);
    this.history.set(updated);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
  }

  clearHistory(): void {
    this.history.set([]);
    this.activeHistoryId.set(null);
    localStorage.removeItem(STORAGE_KEY);
  }

  viewHistoryEntry(entry: HistoryEntry): void {
    this.result.set(entry.result);
    this.activeHistoryId.set(entry.id);
    setTimeout(() => document.querySelector('.results')?.scrollIntoView({ behavior: 'smooth' }), 80);
  }

  removeHistoryEntry(id: string, event: Event): void {
    event.stopPropagation();
    const updated = this.history().filter(e => e.id !== id);
    this.history.set(updated);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
    if (this.activeHistoryId() === id) this.activeHistoryId.set(null);
  }

  formatDate(ts: number): string {
    return new Date(ts).toLocaleString('ro-RO', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
  }

  // ── Preview ──────────────────────────────────────────────

  async onFileSelected(event: Event): Promise<void> {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0] ?? null;
    this.cvFile = file;
    this.result.set(null);
    this.errorMessage.set(null);
    this.activeHistoryId.set(null);
    this.previewOpen.set(false);
    this._revokeBlobUrl();

    if (!file) { this.previewType.set(null); return; }

    const ext = file.name.split('.').pop()?.toLowerCase();
    if (ext === 'pdf') {
      this.blobUrl = URL.createObjectURL(file);
      this.pdfPreviewUrl.set(this.sanitizer.bypassSecurityTrustResourceUrl(this.blobUrl));
      this.docxHtml.set(null);
      this.previewType.set('pdf');
    } else if (ext === 'docx') {
      const arrayBuffer = await file.arrayBuffer();
      const res = await mammoth.convertToHtml({ arrayBuffer });
      this.docxHtml.set(res.value);
      this.pdfPreviewUrl.set(null);
      this.previewType.set('docx');
    }
  }

  openPreview(): void { this.previewOpen.set(true); }
  closePreview(): void { this.previewOpen.set(false); }

  private _revokeBlobUrl(): void {
    if (this.blobUrl) { URL.revokeObjectURL(this.blobUrl); this.blobUrl = null; }
  }

  ngOnDestroy(): void { this._revokeBlobUrl(); }

  // ── JD Import ────────────────────────────────────────────

  onJdCategoryChange(name: string): void {
    this.selectedJdCategory.set(name);
    if (!name) return;
    this.jdLoading.set(true);
    this.http.get<{ content: string }>(`http://localhost:8000/job-descriptions/${name}`).subscribe({
      next: (data) => {
        this.jobDescription.set(data.content.trim());
        this.jdLoading.set(false);
      },
      error: () => { this.jdLoading.set(false); },
    });
  }

  // ── Form ─────────────────────────────────────────────────

  resetForm(): void {
    this.cvFile = null;
    this.jobDescription.set('');
    this.selectedJdCategory.set('');
    this.result.set(null);
    this.errorMessage.set(null);
    this.previewType.set(null);
    this.previewOpen.set(false);
    this.activeHistoryId.set(null);
    this._revokeBlobUrl();
    if (this.fileInput) this.fileInput.nativeElement.value = '';
  }

  get canAnalyze(): boolean {
    return !this.loading() && !!this.cvFile && this.jobDescription().trim().length > 0;
  }

  analyze(): void {
    if (!this.canAnalyze) return;
    this.loading.set(true);
    this.result.set(null);
    this.errorMessage.set(null);

    const formData = new FormData();
    formData.append('cv_file', this.cvFile!);
    formData.append('job_description', this.jobDescription());

    this.http.post<AnalysisResult>('http://localhost:8000/analyze', formData).subscribe({
      next: (data) => {
        this.result.set(data);
        this.loading.set(false);
        this.saveToHistory(data);
      },
      error: (err) => {
        this.errorMessage.set(err.error?.detail ?? 'Eroare la comunicarea cu serverul.');
        this.loading.set(false);
      },
    });
  }

  // ── Display helpers ───────────────────────────────────────

  get hiringDecisionLabel(): string {
    return this.decisionLabel(this.result()?.hiring_decision);
  }

  decisionLabel(decision: string | undefined): string {
    const labels: Record<string, string> = {
      strong_match: 'Potrivire Excelenta',
      good_match: 'Potrivire Buna',
      partial_match: 'Potrivire Partiala',
      weak_match: 'Potrivire Slaba',
    };
    return labels[decision ?? ''] ?? decision ?? '';
  }

  scoreColor(score: number): string {
    if (score >= 70) return '#22c55e';
    if (score >= 50) return '#f59e0b';
    return '#ef4444';
  }

  get currentScoreColor(): string {
    return this.scoreColor(this.result()?.score ?? 0);
  }
}
