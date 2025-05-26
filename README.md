#  Multi-Agent Research Assistant (MARA)

A Python-based command-line tool demonstrating agent-to-agent communication using a custom Model Context Protocol (MCP). MARA can:

* Extract and clean YouTube transcripts
* Perform web searches via Serper API or DuckDuckGo scraping
* Summarize long texts using OpenRouter API or an extractive fallback
* Orchestrate a multi-step workflow through distinct agents

---

## Features

* **Transcript Extraction**: Fetches transcripts from YouTube URLs and cleans them of timestamps and extraneous whitespace.
* **Web Search**: Queries Serper API (if API key provided) or falls back to DuckDuckGo scraping.
* **Text Summarization**: Leverages OpenRouter free models for abstractive summaries or uses an extractive algorithm.
* **Agent Architecture**: Modular agents (`TranscriptAgent`, `SearchAgent`, `SummarizerAgent`) coordinated by `CoordinatorAgent` using the MCP protocol.

---

## Requirements

* Python 3.8+
* See `requirements.txt` for exact versions:

  ```text
  youtube-transcript-api==0.6.1
  requests==2.31.0
  python-dotenv==1.0.0
  beautifulsoup4==4.12.2
  ```

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Configuration

SMARA reads optional API keys and settings from a `.env` file in the project root:

```ini
# .env
SERPER_API_KEY=your_serper_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
MAX_SEARCH_RESULTS=5
SUMMARY_MAX_LENGTH=300
```

* **SERPER\_API\_KEY** (optional): For Serper.dev search API.
* **OPENROUTER\_API\_KEY** (optional): For OpenRouter summarization.
* **MAX\_SEARCH\_RESULTS**: Limits number of search results (default: 5).
* **SUMMARY\_MAX\_LENGTH**: Maximum token length for summaries (default: 300).

---

## Usage

1. **Interactive Mode**

   ```bash
   python main.py
   ```

   * Paste a YouTube URL or query to search.
   * Type `quit` or `exit` to stop.

2. **Single Query Mode**

   ```bash
   python main.py "<your query or YouTube URL>"
   ```

Example:

```bash
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

---

## Project Structure

```
├── config.py           # Loads environment variables and constants
├── mcp_protocol.py     # Defines MCPMessage & abstract MCPAgent
├── agents.py           # Implements Transcript, Search, Summarizer, Coordinator
├── main.py             # Entry point with interactive & single-query modes
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

### Core Components

* **MCPProtocol** (`mcp_protocol.py`): Defines the message format (`MCPMessage`) and base agent (`MCPAgent`) for sending/receiving messages.

* **Agents** (`agents.py`):

  * `TranscriptAgent`: Extracts and cleans YouTube transcripts.
  * `SearchAgent`: Performs web searches via Serper or DuckDuckGo fallback.
  * `SummarizerAgent`: Generates summaries via OpenRouter or extractive algorithm.
  * `CoordinatorAgent`: Routes user input through the appropriate workflow.

* **Main** (`main.py`): Displays a banner, handles CLI input, and invokes `CoordinatorAgent`.

---


**Enjoy using MARA!**
