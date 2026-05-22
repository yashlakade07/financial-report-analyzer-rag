# Financial Report RAG Analyzer 📊

A Retrieval-Augmented Generation (RAG) system built to ingest, process, and analyze multi-page financial documents (like SEC 10-K reports or bank statements). This project leverages a 100% local, privacy-first AI stack to convert PDFs into vector embeddings and accurately answer complex financial queries.

## 🌟 Key Features
* **Privacy-First Processing:** All data processing and LLM inference happen locally. Documents never leave your machine.
* **Vector Search:** Uses **FAISS** (Facebook AI Similarity Search) for blazingly fast in-memory context retrieval.
* **Intelligent Chunking:** Implements LangChain's `RecursiveCharacterTextSplitter` to optimally segment dense financial data.
* **Source Attribution:** The UI explicitly cites the source page numbers for every generated answer to prevent hallucination.
* **Fully Containerized:** Clean microservices architecture with FastAPI (Backend) and Streamlit (Frontend).

---

## 🏗️ Architecture
1.  **Ingestion:** `PyPDFLoader` extracts text from uploaded documents.
2.  **Embedding:** `nomic-embed-text` converts text chunks into vector representations.
3.  **Storage:** Vectors are stored in a local **FAISS** database.
4.  **Retrieval & Generation:** User queries are embedded, matched against the FAISS database, and passed to **Qwen 2.5:7b** via an orchestration chain to generate a grounded response.

---

## 🛠️ Technical Stack
* **Orchestration:** LangChain
* **Generative Model:** Qwen 2.5:7b (via Ollama)
* **Embedding Model:** Nomic-Embed-Text (via Ollama)
* **Vector Database:** FAISS
* **Backend API:** FastAPI & Uvicorn
* **Frontend UI:** Streamlit
* **Containerization:** Docker & Docker Compose
* **Testing:** Pytest

---

## 🚀 Getting Started

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* [Ollama](https://ollama.com/) installed and running on your host machine.

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/financial-report-analyzer.git](https://github.com/YOUR_USERNAME/financial-report-analyzer.git)
   cd financial-report-analyzer

   ```

2. **Pull the required models via Ollama:**
```bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text

```


3. **Build and launch the application:**
```bash
docker-compose up --build

```


4. **Access the Interface:**
* **Frontend UI:** [http://localhost:8501](https://www.google.com/search?q=http://localhost:8501)
* **API Documentation:** [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)



---

## 🧪 Running Tests

To verify the backend API endpoints and RAG logic, run the test suite:

```bash
pytest tests/test_main.py -v

```

---

## 💡 Example Queries

Once a document is processed, try asking complex extraction questions:

* *"What was the single largest withdrawal made during this statement period, and who was the recipient?"*
* *"How much money was credited via NEFT on July 10th, 2019, and what was the source bank?"*
* *"Summarize the primary risk factors mentioned in this document."*


