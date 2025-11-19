# 🚀 Cost-Control Smart Model Router

An intelligent LLM routing system that automatically selects the most cost-effective AI model based on prompt complexity, reducing API costs by up to 70% while maintaining response quality.

## ✨ Features

- **🧠 Smart Routing**: Automatically classifies prompts and routes to optimal models
- **💰 Cost Optimization**: Uses cheaper models for simple tasks, expensive ones only when needed
- **🔌 Multi-Provider Support**: Works with OpenAI (GPT-4o), Google (Gemini), and more
- **📊 Real-time Analytics**: Track costs, usage, and routing decisions
- **🎯 Intelligent Classification**: LLM-powered or rule-based prompt analysis
- **🔄 Auto-Discovery**: Automatically detects and uses best available models
- **📈 Interactive Dashboard**: Beautiful web UI for testing and monitoring
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

- Python 3.10+ (3.14 not recommended due to some package compatibility)
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
   python -m venv venv
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

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Open the dashboard**
   ```
   Open simple_dashboard.html in your browser
   ```

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

1. Open `simple_dashboard.html`
2. Navigate to **Settings** section
3. Enter your API keys
4. Click **Save Keys**

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

**Response:**
```json
{
  "total_requests": 150,
  "total_cost_usd": 0.45,
  "breakdown": {
    "Phi-3-Mini": {"count": 80, "cost": 0.004},
    "Gemini 2.5 Flash": {"count": 50, "cost": 0.015},
    "GPT-4o": {"count": 20, "cost": 0.431}
  }
}
```

### `GET /logs`
Get recent request history (last 50)

### `POST /config/keys`
Update API keys programmatically

## 🎨 Dashboard Features

- **Prompt Testing**: Submit prompts and see real-time routing decisions
- **Response Display**: View full AI-generated responses
- **Metadata**: See model used, cost, latency, and reasoning
- **Analytics**: Track total costs and model distribution
- **Recent Logs**: Monitor all routing decisions
- **Settings**: Add/update API keys directly from UI

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

### Adding a Custom Classifier

See `EXTENDING.md` for detailed instructions on:
- Creating custom classifiers
- Implementing new routing strategies
- Adding model providers

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
├── simple_dashboard.html    # Web dashboard
├── requirements.txt
├── .env.example
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by OpenAI and Google AI
- Inspired by the need for cost-effective AI solutions

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**⭐ If you find this project useful, please consider giving it a star!**
