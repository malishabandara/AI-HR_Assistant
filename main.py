from flask import Flask, request, jsonify
from flask_cors import CORS
import shutil
import os

from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from langchain.llms import HuggingFacePipeline

# 🧹 Clean vector DB on each deploy to save disk
shutil.rmtree("./db", ignore_errors=True)

app = Flask(__name__)
CORS(app)

# 📄 Your knowledge source (PDF)
PDF_PATH = "hr_manual.pdf"
if not os.path.exists(PDF_PATH):
    raise FileNotFoundError("❌ hr_policy.pdf not found! Upload your document.")

# 📚 Load and split PDF
print("🔄 Loading documents...")
loader = PyPDFLoader(PDF_PATH)
documents = loader.load_and_split()

# 🔤 Create embeddings
print("📦 Loading embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 🗃️ Create vectorstore
print("📚 Creating vector DB...")
vectorstore = Chroma.from_documents(documents, embedding=embeddings, persist_directory="./db")

# 🤖 Load lightweight LLM
print("🧠 Loading language model (flan-t5-small)...")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=256)
llm = HuggingFacePipeline(pipeline=pipe)

# 🔁 Retrieval QA setup
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

# 🌐 API route
@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question is required"}), 400

    print(f"❓ Question: {question}")
    answer = qa_chain.run(question)
    return jsonify({"answer": answer})

# Root check
@app.route('/')
def home():
    return "✅ HR Assistant API is live!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
