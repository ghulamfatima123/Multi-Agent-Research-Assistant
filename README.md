# Multi-Agent Research Assistant

**SMARA** is a Python console app demonstrating agent-to-agent communication using a custom MCP (Model Context Protocol).  
It can extract YouTube transcripts, perform web searches, and summarize content—coordinated by a central agent.

---

### 🚀 Features
- **Transcript Agent**: Fetches and cleans YouTube transcripts.  
- **Search Agent**: Queries Serper.dev or falls back to DuckDuckGo scraping.  
- **Summarizer Agent**: Uses OpenRouter API or extractive summarization.  
- **Coordinator Agent**: Orchestrates workflows based on user input.  
- Supports **Interactive** and **CLI** modes.

---

### 🔁 Example Workflows

**YouTube Video Analysis**
```python
from agents import CoordinatorAgent

coordinator = CoordinatorAgent()
result = coordinator.run("https://youtube.com/watch?v=dQw4w9WgXcQ")
print(result)
Web Research

python
Copy
Edit
from agents import CoordinatorAgent

coordinator = CoordinatorAgent()
result = coordinator.run("latest developments in quantum computing")
print(result)
🗂️ Project Structure
bash
Copy
Edit
Multi-Agent Research Assistant/
├── main.py              # Entry point and CLI interface
├── agents.py            # All agent implementations
├── mcp_protocol.py      # MCP communication protocol
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
└── README.md            # This file
🔄 Message Flow Example
yaml
Copy
Edit
1. coordinator → transcript_agent: extract_transcript
2. transcript_agent → coordinator: success
3. coordinator → summarizer_agent: summarize_text
4. summarizer_agent → coordinator: success
📡 Agent Communication Protocol
Implements a custom MCP (Model Context Protocol) for structured communication:

python
Copy
Edit
@dataclass
class MCPMessage:
    id: str
    method: str
    params: Dict[str, Any]
    timestamp: float
    agent_from: str
    agent_to: str
🧩 Adding New Agents
To add a new agent:

Inherit from the MCPAgent base class.

Implement handle_request() and run() methods.

Register the agent with the coordinator.

python
Copy
Edit
class CustomAgent(MCPAgent):
    def __init__(self):
        super().__init__("custom_agent")
    
    def handle_request(self, method: str, params: dict) -> dict:
        # Handle incoming MCP messages
        pass
    
    def run(self, input_data: Any) -> str:
        # Main processing logic
        pass
