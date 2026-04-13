# language-learn-mcp

A **Model Context Protocol (MCP) server** for intelligent language learning pedagogy. This server provides foundational tools for building language learning applications with scientifically-grounded CEFR (Common European Framework of Reference) level management, exercise generation, and learner progression tracking.

## Features

### 🎯 CEFR-Based Language Mixing
Automatically balances target language vs. English based on learner proficiency level (A1–C2), ensuring optimal language input at each stage:
- **A1**: ~10% target language, ~90% English
- **A2**: ~25% target language, ~75% English
- **B1**: ~50% target language, ~50% English
- **B2**: ~75% target language, ~25% English
- **C1**: ~90% target language, ~10% English
- **C2**: ~100% target language

### 🛠️ Language Learning Tools
- **Build System Prompts** – Create context-aware prompts tailored to learner level and learning objectives
- **Build Vocabulary Inputs** – Structure vocabulary data with frequency, CEFR alignment, and semantic fields
- **Generate Exercises** – Create dynamic exercises (translation, fill-in-the-blank, multiple choice, dialogue) adapted to proficiency level
- **Score Responses** – Evaluate learner responses with detailed feedback
- **Get Reinforcement Notes** – Suggest targeted review based on weak areas
- **Language Configuration** – Access structured data for 30+ languages with frequency-ranked vocabulary
- **Detect Drift** – Monitor and prevent learner disengagement or loss of motivation

### 🌍 Multi-Language Support
Pre-configured support for 30+ languages including:
- European languages (French, German, Spanish, Italian, Portuguese)
- Asian languages (Mandarin, Arabic, Japanese, Korean)
- And more—easily extensible for additional languages

### 📊 Learner Progress Tracking
Tools to manage vocabulary mastery, retention curves, and personalized learning paths.

## Architecture

```
language-learn-mcp/
├── src/
│   └── language_learn_mcp/
│       ├── server.py              # MCP server entrypoint
│       ├── types.py               # Type definitions
│       ├── config/
│       │   ├── cefr.py            # CEFR level definitions & vocab lists
│       │   ├── languages.py       # Language metadata & vocabularies
│       │   └── pedagogy.py        # Learning science parameters
│       └── tools/
│           ├── build_system_prompt.py
│           ├── build_vocab_input.py
│           ├── generate_exercise.py
│           ├── score_response.py
│           ├── detect_drift.py
│           ├── get_reinforcement_note.py
│           ├── get_mixing_config.py
│           └── get_language_config.py
├── Dockerfile                    # Docker container for MCP server
└── pyproject.toml               # Python project configuration
```

## Installation

### Prerequisites
- Python 3.11 or higher

### Local Installation

```bash
# Clone the repository
git clone https://github.com/abdullah1186/language-learn-mcp.git
cd language-learn-mcp

# Install in development mode
pip install -e .
```

### Docker Installation

```bash
docker build -t language-learn-mcp .
docker run -p 8000:8000 language-learn-mcp
```

## Usage

### Starting the MCP Server

```bash
language-learn-mcp
```

The server will start and listen for MCP protocol requests. Use it as a backend for language learning applications like **poly-pal**.

### Example: Using with Claude or Another AI Client

```python
import anthropic
from language_learn_mcp import mcp_client

# Initialize client
client = anthropic.Anthropic()

# Get language config
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=[/* language-learn-mcp tools */],
    messages=[
        {
            "role": "user",
            "content": "Generate a B1-level Spanish exercise on travel vocabulary."
        }
    ]
)
```

## Connection to poly-pal

**language-learn-mcp** is the pedagogical backbone for **poly-pal**, a WhatsApp-based language learning chatbot. While poly-pal implements specific tools and Supabase-based progress tracking, language-learn-mcp provides:

- **Reusable pedagogy framework** – CEFR-based level management and language mixing
- **Exercise generation** – Dynamically create diverse practice types
- **Response evaluation** – Score learner answers with pedagogically sound feedback
- **Language data** – Curated vocabulary lists aligned with CEFR levels
- **Drift detection** – Monitor engagement and suggest interventions

Together, they form a complete language learning platform: **language-learn-mcp** handles the *what and how to teach*, while **poly-pal** handles the *where (WhatsApp) and when (responsive messaging)*.

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Building Documentation

Documentation for each tool is embedded in docstrings. Use your IDE or MCP tools to introspect available methods.

## Configuration

Language profiles and CEFR vocabulary lists are configured in:
- `src/language_learn_mcp/config/languages.py` – Add new languages
- `src/language_learn_mcp/config/cefr.py` – Extend vocabulary lists
- `src/language_learn_mcp/config/pedagogy.py` – Adjust learning science parameters

## Contributing

Contributions are welcome! Areas of interest:
- Additional language profiles
- More exercise types
- Adaptive difficulty algorithms
- Integration tests with AI models



## Related Projects

- **[poly-pal](https://github.com/abdullah1186/poly-pal)** – WhatsApp language learning chatbot powered by language-learn-mcp
