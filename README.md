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
1. **Ingestion:** `PyPDFLoader` extracts text from uploaded documents.
2. **Embedding:** `nomic-embed-text` converts text chunks into vector representations.
3. **Storage:** Vectors are stored in a local **FAISS** database.
4. **Retrieval & Generation:** User queries are embedded, matched against the FAISS database, and passed to **Qwen 2.5:7b** via an orchestration chain to generate a grounded response.

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
