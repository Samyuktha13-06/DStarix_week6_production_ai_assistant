# DStarix AI Assistant

A production-ready, intelligent AI Assistant integrating Conversational Chat, Retrieval-Augmented Generation (RAG), Persistent Conversation Memory, and Tool Calling. It is structured using a compiled LangGraph state workflow, with a FastAPI backend server and a responsive Streamlit user interface.

---

## Project Description

The DStarix AI Assistant is designed to serve as a conversational agent that automatically routes incoming user queries to the appropriate processing path:
1. **Chat**: General conversational queries using memory.
2. **RAG**: Answering specific questions regarding uploaded documents (such as rule books, policy files, or logs) using a localized vector database for context extraction.
3. **Tool Calling**: Routing mathematical calculations to a secure mathematical solver tool.

---

## Features

- **Intelligent Query Routing**: Powered by a custom `StateGraph` logic that classifies inputs to optimize response paths.
- **Dynamic Document Processing**: Upload, chunk (using `RecursiveCharacterTextSplitter`), embed (`all-MiniLM-L6-v2`), and persist PDF or TXT files into a local FAISS vector store database.
- **Source Attribution**: Inline source and page mapping indicators for all retrieved RAG answers.
- **Persistent Conversation Memory**: Conversational context retention across multiple turns using custom memory layers.
- **Safe Tool Execution**: Sandbox calculation environment filtering execution to only safe mathematical characters.
- **Evaluation Pipeline**: Modules to evaluate baseline retrieval rates, run configuration experiments (comparing chunk size and overlap limits), and check answer correctness/groundedness.

---

## Technologies Used

- **Core**: Python 3.14.2+
- **LLM Engine**: Groq SDK (`llama-3.3-70b-versatile`)
- **Workflow Orchestration**: LangGraph (`langgraph`) & LangChain (`langchain-core`)
- **Vector Database & Embeddings**: FAISS (`faiss-cpu`) & HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
- **Web API**: FastAPI (`fastapi` & `uvicorn`)
- **User Interface**: Streamlit (`streamlit`)
- **Testing**: Pytest (`pytest`)

---

## Installation Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd dstarix_ai_assistant
   ```

2. **Create and activate a virtual environment**:
   * **Windows**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * **Linux/macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Setup Instructions

1. **Configure Environment Variables**:
   Create a `.env` file in the project root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

2. **Run Initialization / Baseline Indexing (Optional)**:
   Build the initial vector store using the default document:
   ```bash
   python scripts/build_vector_store.py
   ```

---

## Usage Guide

To launch the full stack, start both the FastAPI backend server and the Streamlit frontend.

### 1. Run the FastAPI Backend
Start the backend server on `http://127.0.0.1:8000`:
```bash
uvicorn api.main:app --reload
```

### 2. Run the Streamlit User Interface
In a separate terminal window, start the Streamlit application:
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

### 3. Run the Evaluation Suite
To execute RAG evaluation, chunking comparison configurations, and answer verification scripts:
```bash
# Evaluate retrieval hit rates (k=2, 4, 6)
python evaluation/evaluate_retrieval.py

# Run chunk size / overlap comparison tests
python evaluation/chunk_experiment.py

# Test answer correctness & groundedness check
python evaluation/evaluate_answers.py
```

### 4. Run Automated Tests
```bash
python -m pytest
```

---

## Project Structure

```text
dstarix_ai_assistant/
│
├── .streamlit/
│   └── config.toml          # Streamlit file watcher options
│
├── api/
│   ├── main.py              # FastAPI server endpoints
│   └── schemas.py           # Request and response Pydantic models
│
├── documents/
│   └── uploads/             # Raw PDF/TXT documents uploaded via UI
│
├── data/
│   └── vector_store/        # Local FAISS index files
│
├── embeddings/
│   └── embedding_model.py   # HuggingFace embedder initialization
│
├── evaluation/
│   ├── evaluate_answers.py   # Answer quality testing framework
│   ├── evaluate_retrieval.py # Retrieval accuracy checks
│   ├── chunk_experiment.py   # Chunking comparison experiments
│   ├── rag_questions.json   # Standard evaluation Q&A set
│   └── evaluation_results.md# Generated results ledger
│
├── graph/
│   ├── nodes/
│   │   ├── chat_node.py     # Graph node handling LLM chat
│   │   ├── rag_node.py      # Graph node querying vector DB
│   │   ├── router_node.py   # Graph node classifying queries
│   │   └── tool_node.py     # Graph node calling tools
│   ├── graph_builder.py     # LangGraph compilation & workflow setup
│   └── state.py             # AssistantState TypedDict schema
│
├── loaders/
│   ├── chunk_documents.py   # Document text splitter wrapper
│   └── document_loader.py   # PDF / text extractor utilities
│
├── memory/
│   └── conversation_memory.py# Conversational memory buffer
│
├── retrieval/
│   ├── retriever.py         # Search lookup logic wrapper
│   └── vector_store.py      # FAISS store initialization & persistence
│
├── services/
│   └── rag_service.py       # Similarity and source formatter driver
│
├── tools/
│   ├── tools.py             # Math calculator tool definition
│   └── tool_registry.py     # Registration mapping
│
├── utils/
│   ├── config.py            # Dotenv configurations loader
│   ├── file_manager.py      # Disk upload handlers
│   ├── llm.py               # ChatGroq LLM model wrapper setup
│   └── source_formatter.py  # Source mapping utilities
│
├── app.py                   # Streamlit layout & interface loop
├── requirements.txt         # Project dependencies list
└── README.md                # Documentation guide
```

---

## Example Outputs

### Evaluation Run Output
```text
======================================================================
RAG RETRIEVAL EVALUATION | k=4
======================================================================

Q1: How long is the DStarix Generative AI internship?
   Retrieved chunks: 4
   Match score: 1.00
   Result: HIT
   Source: Internship Rule Book.pdf | Page 1

Q10: What is the monthly salary provided to interns?
   Retrieved documents: 4
   [OK] Unanswerable question included in evaluation

======================================================================
Retrieval Hit Rate: 100.00%
Hits: 9/9
======================================================================
```