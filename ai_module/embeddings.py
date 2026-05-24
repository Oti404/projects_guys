from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union


try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading the SentenceTransformer model: {e}")
    model = None

def generate_embeddings(text_list: List[str]) -> Union[np.ndarray, dict]:
    """
    Takes a list of strings (e.g., skills, job titles) and converts them
    into a numerical matrix where similar concepts are mathematically closer.
    
    Args:
        text_list: A list of skills or texts.
        
    Returns:
        np.ndarray: A numpy array containing the embeddings.
        dict: An error message if the model fails to load or input is invalid.
    """
    if not model:
        return {"error": "SentenceTransformer model is not initialized."}
    
    if not text_list:
        return {"error": "The input text list is empty."}
    
    try:
        embeddings = model.encode(text_list)
        return embeddings
    except Exception as e:
        return {"error": f"Failed to generate embeddings: {str(e)}"}

def calculate_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """s
    Calculates the cosine similarity between two embeddings.
    Cosine similarity measures the angle between two vectors.
    A score of 1.0 means identical meaning, 0.0 means completely unrelated.
    
    Args:
        embedding1: First vector.
        embedding2: Second vector.
        
    Returns:
        float: A similarity score between -1.0 and 1.0.
    """
    try:
        dot_product = np.dot(embedding1, embedding2)
        norm_a = np.linalg.norm(embedding1)
        norm_b = np.linalg.norm(embedding2)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        similarity = dot_product / (norm_a * norm_b)
        return float(similarity)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0