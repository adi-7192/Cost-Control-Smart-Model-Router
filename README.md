# 🚀 Cost-Control Smart Model Router

An intelligent LLM routing system that automatically selects the most cost-effective AI model based on prompt complexity, reducing API costs by up to 70% while maintaining response quality.

## ✨ Features

- **🧠 Smart Routing**: Automatically classifies prompts and routes to optimal models
- **💰 Cost Optimization**: Uses cheaper models for simple tasks, expensive ones only when needed
- **� Real-time Savings Comparison**: See exactly how much you save vs using GPT-4o for everything
- **📈 Scale Projections**: Visualize daily, monthly, and yearly savings at 1000 requests/day
- **�🔌 Multi-Provider Support**: Works with OpenAI (GPT-4o), Google (Gemini), and more
- **📊 Real-time Analytics**: Track costs, usage, and cumulative savings via Streamlit dashboard
- **🎯 Intelligent Classification**: LLM-powered or rule-based prompt analysis
- **🔄 Auto-Discovery**: Automatically detects and uses best available models
- **🎨 Modern UI**: Beautiful Streamlit dashboard with dark theme and gradient cards
- **🛠️ Extensible**: Easy to add new models and classifiers

## 🎯 How It Works

```
User Prompt → Smart Classifier → Route to Best Model → Return Response
                    ↓
            [Simple] → Phi-3 (Fast & Cheap)
            [Moderate] → Gemini 2.5 Flash (Balanced)
            [Complex] → GPT-4o (Powerful)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10-3.13 (recommended: 3.13)
- pip
- (Optional) OpenAI API Key
- (Optional) Google AI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cost-control-smart-router.git
   cd cost-control-smart-router
   ```

2. **Create virtual environment**
   ```bash
   python3.13 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys (optional for demo)
   ```

5. **Run the backend server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Run the Streamlit dashboard** (in a new terminal)
   ```bash
   streamlit run dashboard.py
   ```

7. **Access the application**
   - Dashboard: http://localhost:8501
   - API: http://localhost:8000

## 🔑 Configuration

### Environment Variables

Create a `.env` file (or copy from `.env.example`):

```bash
# Classifier Type
CLASSIFIER_TYPE=rules  # Options: "rules" or "llm"

# Database
DATABASE_URL=sqlite:///./sql_app.db

# API Keys (Optional - system works without them in demo mode)
OPENAI_API_KEY=your-openai-key-here
GOOGLE_API_KEY=your-google-api-key-here
```

### Adding API Keys via Dashboard

1. Open the Streamlit dashboard at http://localhost:8501
2. Click **Settings** in the sidebar
3. Expand **🔑 API Configuration**
4. Enter your API keys
5. Click **💾 Save API Keys**

The system will automatically:
- Detect available models
- Enable smart LLM-based classification
- Route to real AI models

## 📊 API Endpoints

### `POST /route`
Route a prompt to the best model

**Request:**
```json
{
  "prompt": "Explain quantum physics"
}
```

**Response:**
```json
{
  "model": "GPT-4o",
  "difficulty": "complex",
  "reasoning": "Requires deep technical explanation",
  "response": "Quantum physics is...",
  "cost": 0.0075,
  "tokens": 250,
  "latency_ms": 1200
}
```

### `GET /stats`
Get usage statistics

### `GET /logs`
Get recent request history (last 100)

### `POST /config/keys`
Update API keys programmatically

## 🎨 Dashboard Features

- **💬 Prompt Testing**: Submit prompts and see real-time routing decisions
- **📝 Response Display**: View full AI-generated responses
- **� Cost Savings Comparison**: Beautiful gradient card showing:
  - What you paid (with smart routing)
  - What GPT-4o would have cost
  - Exact savings amount and percentage
- **�📊 Scale Projections**: See potential savings at 1000 requests/day:
  - Daily, monthly, and yearly projections
  - Big picture impact visualization
- **📊 Metadata**: See model used, cost, latency, and reasoning
- **📈 Analytics Dashboard**: 
  - Total requests and actual costs
  - Cost without routing comparison
  - **Cumulative savings tracker**
  - Model and difficulty distribution charts
- **📋 Recent Logs**: Monitor all routing decisions in a table
- **⚙️ Settings**: Add/update API keys directly from sidebar
- **🎨 Modern UI**: Dark theme with horizontal charts and clean layout

## 🧩 Extending the System

### Adding a New Model

1. Create a new client in `app/llm/providers.py`:

```python
class ClaudeClient(LLMClient):
    async def generate(self, prompt: str, max_tokens: int = 100):
        # Your implementation
        return response_text, cost, tokens
```

2. Register in router (`app/router.py`):

```python
self.clients = {
    "simple": Phi3Client(),
    "moderate": GeminiClient(),
    "complex": ClaudeClient()  # New model
}
```

See `EXTENDING.md` for detailed instructions.

## 📈 Cost Savings Example

**Without Smart Routing** (using GPT-4o for everything):
- 1000 requests/day
- Average: $0.03/request
- **Monthly cost: $900**

**With Smart Routing**:
- 600 simple → Phi-3 ($0.00005/request) = $0.03
- 300 moderate → Gemini ($0.0005/request) = $0.15
- 100 complex → GPT-4o ($0.03/request) = $3.00
- **Monthly cost: $3.18** (99.6% savings!)

## 🛠️ Development

### Running Tests

```bash
python verify.py
```

### Project Structure

```
├── app/
│   ├── main.py              # FastAPI application
│   ├── router.py            # Core routing logic
│   ├── models.py            # Pydantic/SQLAlchemy models
│   ├── database.py          # Database setup
│   ├── config.py            # Configuration
│   ├── classifier/          # Prompt classifiers
│   │   ├── base.py
│   │   ├── rules.py         # Rule-based classifier
│   │   ├── llm.py           # LLM-based classifier
│   │   └── factory.py
│   └── llm/                 # LLM clients
│       ├── base.py
│       ├── providers.py     # Model implementations
│       ├── factory.py
│       └── model_discovery.py
├── dashboard.py             # Streamlit dashboard
├── requirements.txt
├── .env.example
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) and [Streamlit](https://streamlit.io/)
- Powered by OpenAI and Google AI
- Inspired by the need for cost-effective AI solutions

---

**⭐ If you find this project useful, please consider giving it a star!**
