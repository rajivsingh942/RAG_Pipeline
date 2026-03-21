# 🤖 Smart RAG - AI Document Analysis

Ask questions about your documents and get intelligent, context-aware answers powered by AI.

**Smart RAG** uses Retrieval Augmented Generation (RAG) to read your documents and answer questions with accuracy and context.

---

## 🚀 Quick Start (5 minutes)

### Windows
1. Extract the `RAG_PIPELINE` folder
2. **Double-click:** `START_ALL_WEB.bat`
3. Your browser opens automatically
4. Upload documents and start asking questions!

### macOS / Linux
See [INSTALL.md](INSTALL.md) for setup instructions

---

## ✨ Key Features

- ✅ **Multiple Document Types**: PDF, Word, Excel, and folder uploads
- ✅ **Smart Search**: AI understands meaning, not just keywords
- ✅ **Multiple LLMs**: OpenAI, Google Gemini, OpenRouter (choose your favorite)
- ✅ **Web Interface**: Modern, intuitive chat interface
- ✅ **Conversation History**: Keep track of all Q&A sessions
- ✅ **Private & Local**: All documents stored locally (your data, your control)
- ✅ **REST API**: Full API for programmatic access

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **USER_GUIDE.md** | How to use the app (recommended first read) |
| **INSTALL.md** | Setup instructions for all operating systems |
| **PROJECT.md** | Technical architecture and project structure |

---

## 💬 How It Works (Simple Explanation)

1. **You upload documents** (PDF, Word, Excel)
2. **Smart RAG reads them** and breaks into chunks
3. **Creates AI understanding** of the content (embeddings)
4. **You ask questions** in natural language
5. **Smart RAG finds relevant parts** and asks AI to answer
6. **You get accurate answers** based on your actual documents

**Result:** AI answers that are specific to YOUR documents, not generic.

---

## ⚙️ System Requirements

- **Windows 7+**, macOS 10.14+, or Linux (Ubuntu/Debian)
- **Python 3.10+** (can be installed automatically)
- **2GB+ RAM**
- **5GB disk space**
- **Internet connection** (only for LLM API calls)

---

## 🔑 API Keys Required

Smart RAG uses AI models from different providers. Choose one (Free options available!):

| Provider | Model | Cost | Link |
|----------|-------|------|------|
| **OpenAI** | GPT-4o-mini | Paid | https://platform.openai.com |
| **Google** | Gemini 1.5 Pro | Free tier | https://makersuite.google.com |
| **OpenRouter** | Llama-3-8b | Pay-as-you-go | https://openrouter.ai |

See [INSTALL.md](INSTALL.md) for how to get API keys.

---

## 🎯 Common Use Cases

### 📊 Business Reports
- Analyze quarterly earnings reports
- Extract key metrics
- Compare documents
- Generate summaries

### 📋 Research
- Search across research papers
- Find specific findings
- Compare methodologies
- Extract citations

### 📖 Learning
- Understand textbooks
- Ask follow-up questions
- Clarify complex topics
- Get examples

### 🏢 Compliance
- Review policy documents
- Find specific clauses
- Check requirements
- Track changes

---

## 🎓 What is RAG?

**RAG** = **Retrieval Augmented Generation**

Traditional AI: "What is the capital of France?" → Paris (generic knowledge)

**Smart RAG**: "According to my documents, what is X?" → Answer from YOUR actual documents

This makes answers:
- ✅ **Accurate** - Based on your real data
- ✅ **Specific** - About your actual documents  
- ✅ **Current** - Reflects your latest information
- ✅ **Verifiable** - You can see where answers come from

---

## 🔒 Privacy & Security

- ✅ **Documents stay local** - Stored only on your computer
- ✅ **No cloud storage** - We don't upload your files anywhere
- ✅ **API calls only** - Text sent to LLM API (for processing only)
- ✅ **Database locked** - SQL database in `backend/data/`
- ✅ **Open source** - You can audit the code

See full privacy details in [USER_GUIDE.md](USER_GUIDE.md#%EF%B8%8F-privacy--security)

---

## 🛠️ For Developers

See [PROJECT.md](PROJECT.md) for:
- Complete architecture overview
- Database schema
- API endpoints documentation
- Technology stack details
- Development workflow

### Tech Stack
- **Backend**: FastAPI + SQLAlchemy + FAISS
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **AI**: LangChain + SentenceTransformers
- **Database**: SQLite + FAISS vector index

---

## 📞 Troubleshooting

### Application won't start
→ See [INSTALL.md - Troubleshooting](INSTALL.md#-troubleshooting-windows-setup)

### Bad answers from AI
→ See [USER_GUIDE.md - Tips & Tricks](USER_GUIDE.md#-tips--tricks)

### API errors
→ See [USER_GUIDE.md - If Something Goes Wrong](USER_GUIDE.md#-if-something-goes-wrong)

### Technical questions
→ See [PROJECT.md](PROJECT.md)

---

## 📦 What's Included

```
RAG_PIPELINE/
├── START_ALL_WEB.bat          ← Run this to start
├── frontend/                   ← Web interface
├── backend/                    ← AI engine
├── DataSource/                 ← Sample documents
├── .env                        ← Configuration
└── Documentation/
    ├── README.md              ← This file
    ├── USER_GUIDE.md          ← How to use
    ├── INSTALL.md             ← Setup instructions
    └── PROJECT.md             ← Technical details
```

---

## 🎯 Next Steps

1. **First time?** → Run `START_ALL_WEB.bat`
2. **Need help?** → Read [USER_GUIDE.md](USER_GUIDE.md)
3. **Setting up?** → Follow [INSTALL.md](INSTALL.md)
4. **Developer?** → See [PROJECT.md](PROJECT.md)

---

## 💡 Tips for Best Results

✅ **DO:**
- Upload clear, well-formatted documents
- Ask specific questions
- Use complete sentences
- Wait for upload to finish
- Keep API keys in `.env` secure

❌ **DON'T:**
- Upload scanned images (OCR not supported)
- Ask questions before uploading documents
- Force-close the application
- Share `.env` file with others
- Upload corrupted files

---

## 🆙 Staying Updated

To update Smart RAG:
```bash
# Activate virtual environment, then:
pip install -r backend/requirements.txt --upgrade
```

---

## 📄 License

[License information will be added]

---

## 👋 Enjoy Using Smart RAG!

Have questions? Check the documentation above.

Happy analyzing! 🚀


---

For detailed instructions, see: **QUICKSTART.md**
