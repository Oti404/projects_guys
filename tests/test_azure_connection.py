import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

def test_azure_connection():
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[
            {"role": "user", "content": "Răspunde cu un singur cuvânt: funcționează?"}
        ],
        max_tokens=10,
    )

    raspuns = response.choices[0].message.content
    print(f"\nRăspuns Azure: {raspuns}")
    assert raspuns is not None and len(raspuns) > 0

if __name__ == "__main__":
    test_azure_connection()
    print("Conexiune Azure OK!")

