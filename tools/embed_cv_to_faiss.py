import os
import json
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables (API key)
load_dotenv()

# Load CV analysis
with open("cv_analysis.json", "r", encoding="utf-8") as f:
    cv_data = json.load(f)

# Combine each CV’s analysis into a single string
texts = []
metadata = []

for entry in cv_data:
    combined_text = entry["analysis"]
    texts.append(combined_text)
    metadata.append({"source": entry["file_name"]})

# Create embeddings
embedding_model = OpenAIEmbeddings()

# Build FAISS vector DB
print("🔧 Embedding CVs and creating FAISS index...")
vectorstore = FAISS.from_texts(texts, embedding_model, metadatas=metadata)

# Save to disk
faiss_dir = "cv_faiss_index"
vectorstore.save_local(faiss_dir)

print(f"✅ FAISS vector index saved to: {faiss_dir}")
