# 🏛️ SchemeSense

**A RAG-based multilingual assistant that helps Indian citizens discover government welfare schemes — in Hindi, English, and Hinglish.**

## Problem

Information about government schemes is scattered across many portals and PDFs, written in formal English or complex Hindi. Citizens — especially farmers, women, SC/ST communities — miss schemes they're eligible for because:

- They don't know the exact scheme name to search for
- They ask questions in everyday Hindi or Hinglish, but portals expect formal language
- They depend on intermediaries who may not have complete information

## What SchemeSense Does

- **Curated dataset**: 200+ verified government schemes (Central + Madhya Pradesh)
- **Multilingual RAG**: Ask in Hindi, English, or Hinglish — get grounded answers with source citations
- **Retrieval evaluation**: Measured Hit@1, Hit@5, MRR across all 3 languages
- **Voice interface**: Speak your question instead of typing
- **Chat UI**: Simple Streamlit-based chat interface

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Chat UI                     │
│              (Hindi / English / Hinglish)                │
│         🎤 Voice Input    💬 Text Input                  │
└────────────────────┬────────────────────────────────────┘
                     │
              ┌──────▼──────┐
              │  RAG Module  │
              │ retrieval/   │
              │   rag.py     │
              └──┬───────┬───┘
                 │       │
    ┌────────────▼─┐  ┌──▼──────────────┐
    │  Retrieval   │  │   Generation    │
    │ E5-base +    │  │  Gemini 2.5     │
    │ ChromaDB     │  │  Flash          │
    └──────────────┘  └─────────────────┘
                 ▲
    ┌────────────┴──────────────────────┐
    │        Data Pipeline              │
    │ PDFs → Extract → Clean → Chunk   │
    │      → Embed → ChromaDB          │
    └───────────────────────────────────┘
```

## Setup

### 1. Clone and create virtual environment

```bash
git clone <repo-url>
cd schemesense
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey).

### 4. Data pipeline (if starting from scratch)

The processed data and ChromaDB embeddings are already included. If you need to rebuild:

```bash
# Step 1: Extract text from PDFs
python ingest/build_extended.py

# Step 2: Clean text and split into sections
python ingest/clean_split.py

# Step 3: Chunk sections with overlap
python ingest/chunk.py

# Step 4: Embed dev set into ChromaDB
python retrieval/embed_dev.py
```

## Usage

### Chat App (recommended)

```bash
streamlit run app/main.py
```

Opens a browser-based chat interface where you can:
- Type questions in Hindi, English, or Hinglish
- Use voice input via the sidebar microphone
- Filter schemes by State or Central level
- See source citations for every answer

### CLI Search

```bash
# Search for schemes
python retrieval/search_dev.py "MP mein students ko scholarship kaise milegi?"

# RAG answer (retrieve + generate)
python retrieval/rag.py "विधवा पेंशन योजना में कौन पात्र है?"
```

### Evaluation

```bash
python eval/run_eval.py
```

Runs 45 test queries (15 questions × 3 languages) and computes:
- **Hit@1**: Is the correct scheme ranked #1?
- **Hit@5**: Is the correct scheme in top 5?
- **MRR**: Mean Reciprocal Rank

Results are saved to `eval/results.json`.

## Project Structure

```
schemesense/
├── app/                        # Streamlit chat application
│   ├── main.py                 # App entry point
│   ├── voice.py                # Voice input/output helpers
│   └── components.py           # UI components
├── data/
│   ├── raw/myscheme/           # Raw PDFs from myscheme.gov.in
│   ├── processed/
│   │   ├── schemes_extended.json   # Extracted scheme records
│   │   ├── schemes_sections.json   # Section-split records
│   │   └── chunks.json             # Chunked text for embedding
│   ├── chroma/                 # ChromaDB vector store
│   └── schemes.json            # Hand-curated scheme entries
├── eval/
│   ├── questions.csv           # 45 test queries (en/hi/hinglish)
│   ├── run_eval.py             # Retrieval evaluation script
│   ├── results.json            # Evaluation results
│   └── quick_check.py          # Quick diagnostic checks
├── ingest/
│   ├── build_extended.py       # PDF extraction pipeline
│   ├── clean_split.py          # Text cleaning + section splitting
│   ├── chunk.py                # Chunking with sentence overlap
│   ├── fix_names.py            # Scheme name repair
│   ├── repair_regions.py       # Region/state field repair
│   └── reassign_dev.py         # Dev/full split assignment
├── notebooks/
│   ├── rag_experiment.py       # RAG grounding experiments
│   └── ...                     # Exploration scripts
├── retrieval/
│   ├── embed_dev.py            # Embed chunks into ChromaDB
│   ├── search_dev.py           # CLI semantic search
│   └── rag.py                  # Core RAG module (retrieve + generate)
├── voice/                      # (reserved for future voice models)
├── .env                        # API keys (not committed)
├── requirements.txt
└── notes.md                    # Project notes and learning log
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Embedding model | [intfloat/multilingual-e5-base](https://huggingface.co/intfloat/multilingual-e5-base) |
| Vector database | ChromaDB (local, cosine similarity) |
| LLM | Gemini 2.5 Flash (via Google GenAI SDK) |
| Frontend | Streamlit |
| Voice input | SpeechRecognition (Google STT) |
| Voice output | gTTS (Google Text-to-Speech) |
| PDF extraction | pdfplumber |
| Text cleaning | ftfy |
| Data source | [myscheme.gov.in](https://www.myscheme.gov.in/) via HuggingFace dataset |

## Data

- **Source**: ~2000 scheme PDFs from [myscheme.gov.in](https://www.myscheme.gov.in/) (via HuggingFace dataset `shrijayan/gov_myscheme`)
- **Dev set**: 200 schemes (all Madhya Pradesh + random sample) used for rapid iteration
- **Sections extracted**: Details, Benefits, Eligibility, Exclusions, Application Process, Documents Required, FAQ
- **Chunking**: Max 1200 chars per chunk, 150 char overlap, sentence-boundary-aware

## Key Findings

- **Cross-lingual retrieval works**: Hindi queries successfully retrieve English documents (and vice versa) using multilingual E5-base
- **Hinglish is harder**: Roman-script Hindi (Hinglish) queries often miss relevant chunks, likely due to vocabulary mismatches (e.g., "viklang" vs "disabled" vs "दिव्यांग")
- **LLM grounding matters**: Without RAG context, Gemini gives outdated amounts (₹1,250 vs actual ₹1,500 for Ladli Behna); with RAG context, it cites the correct figure

## Contributing

This is a research project for measuring retrieval strategies on multilingual government scheme queries. Contributions welcome for:
- Adding more verified schemes
- Improving Hinglish retrieval
- Building a WhatsApp/Telegram bot interface

## License

MIT
