# AI Projects Collection

This repository contains various AI/ML projects including prompt engineering, RAG systems, and agent implementations.

## 📁 Project Structure

- **`prompt_engineering/`** - Various prompting techniques (Zero-shot, Few-shot, CoT, Auto-CoT, Persona)
- **`rag/`** - RAG (Retrieval Augmented Generation) system with Qdrant vector database
- **`weather_agent/`** - AI agent with tool calling capabilities
- **`ollama_fastapi/`** - FastAPI server with Ollama integration
- **`hf_basic/`** - Hugging Face basic examples

## 🚀 Setup Instructions (Mac)

### Prerequisites
- Python 3.8 or higher
- Git
- Docker (for RAG project with Qdrant)
- Ollama (for ollama_fastapi project)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-github-repo-url>
   cd AI
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your actual API keys:
   ```bash
   nano .env  # or use any text editor
   ```

5. **For RAG project - Start Qdrant vector database**
   ```bash
   cd rag
   docker-compose up -d
   cd ..
   ```

6. **For Ollama projects - Install and start Ollama**
   ```bash
   # Install Ollama from https://ollama.ai
   # Then pull the required model
   ollama pull deepcoder:1.5b
   ```

## 🔑 Required API Keys

- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Google Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 📝 Running Individual Projects

### Weather Agent
```bash
python weather_agent/agent.py
```

### RAG Chat System
```bash
# Make sure Qdrant is running
cd rag
python index.py  # First time to index the PDF
python chat.py   # To chat with the system
```

### Ollama FastAPI Server
```bash
cd ollama_fastapi
uvicorn server:app --reload
```

### Prompt Engineering Examples
```bash
python prompt_engineering/zero.py
python prompt_engineering/few.py
python prompt_engineering/cot.py
# ... etc
```

## ⚠️ Important Notes

- Never commit your `.env` file to GitHub
- The `.env.example` file is a template - copy it to `.env` and fill in your actual keys
- Make sure Docker is running before starting the RAG system
- Some projects require specific models to be downloaded (Ollama, Hugging Face)

## 🛠️ Troubleshooting

### On Mac - If you get SSL certificate errors:
```bash
pip install --upgrade certifi
```

### If you get permission errors:
```bash
chmod +x <script-name>
```

### For M1/M2 Mac users:
Some packages might need Rosetta or specific builds. If you encounter issues:
```bash
# Use conda instead of pip for better M1/M2 support
conda create -n ai-env python=3.10
conda activate ai-env
pip install -r requirements.txt
```

## 📦 Dependencies

See `requirements.txt` for full list of dependencies.

Main frameworks used:
- OpenAI
- LangChain
- FastAPI
- Ollama
- Transformers
- PyTorch
