import re
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from mcp_protocol import MCPAgent, MCPMessage
from config import config

class TranscriptAgent(MCPAgent):
    """Agent for YouTube transcript extraction"""
    
    def __init__(self):
        super().__init__("transcript_agent")
    
    def handle_request(self, method: str, params: dict) -> dict:
        if method == "extract_transcript":
            url = params.get("url", "")
            try:
                transcript = self.run(url)
                return {"success": True, "data": transcript}
            except Exception as e:
                return {"success": False, "error": str(e)}
        return {"success": False, "error": "Unknown method"}
    
    def run(self, url: str) -> str:
        """Extract YouTube transcript"""
        try:
            video_id = self._extract_video_id(url)
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            transcript = " ".join([item['text'] for item in transcript_list])
            return self._clean_transcript(transcript)
        except (NoTranscriptFound, TranscriptsDisabled):
            return "No transcript available for this video."
        except Exception as e:
            raise Exception(f"Transcript extraction failed: {e}")
    
    def _extract_video_id(self, url: str) -> str:
        patterns = [
            r"youtube\.com/watch\?v=([^&\n]+)",
            r"youtu\.be/([^&\n]+)"
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise Exception("Invalid YouTube URL")
    
    def _clean_transcript(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\[.*?\]', '', text)
        return text.strip()

class SearchAgent(MCPAgent):
    """Agent for web search with fallback options"""
    
    def __init__(self):
        super().__init__("search_agent")
    
    def handle_request(self, method: str, params: dict) -> dict:
        if method == "web_search":
            query = params.get("query", "")
            try:
                results = self.run(query)
                return {"success": True, "data": results}
            except Exception as e:
                return {"success": False, "error": str(e)}
        return {"success": False, "error": "Unknown method"}
    
    def run(self, query: str) -> str:
        """Perform web search with fallback methods"""
        # Try Serper API first (if available)
        if config.SERPER_API_KEY:
            try:
                return self._search_serper(query)
            except Exception as e:
                print(f"Serper failed: {e}, trying fallback...")
        
        # Fallback to basic web scraping
        return self._fallback_search(query)
    
    def _search_serper(self, query: str) -> str:
        """Search using Serper.dev (free tier: 2500 queries/month)"""
        headers = {
            "X-API-KEY": config.SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {"q": query, "num": config.MAX_SEARCH_RESULTS}
        
        response = requests.post(
            config.SERPER_URL, 
            headers=headers, 
            json=payload, 
            timeout=config.REQUEST_TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        for item in data.get("organic", [])[:config.MAX_SEARCH_RESULTS]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            results.append(f"**{title}**\n{snippet}\nSource: {link}\n")
        
        return "\n".join(results) if results else "No search results found."
    
    def _fallback_search(self, query: str) -> str:
        """Fallback search using web scraping (free but limited)"""
        try:
            # Simple DuckDuckGo search (no API key needed)
            search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; SMARA/1.0)'}
            
            response = requests.get(search_url, headers=headers, timeout=config.REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            for result in soup.find_all('div', class_='result')[:config.MAX_SEARCH_RESULTS]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem and snippet_elem:
                    title = title_elem.get_text().strip()
                    snippet = snippet_elem.get_text().strip()
                    link = title_elem.get('href', '')
                    results.append(f"**{title}**\n{snippet}\nSource: {link}\n")
            
            return "\n".join(results) if results else f"Basic search completed for: {query}"
            
        except Exception as e:
            return f"Search unavailable. Query was: {query}\nError: {e}"

class SummarizerAgent(MCPAgent):
    """Agent for text summarization with free options"""
    
    def __init__(self):
        super().__init__("summarizer_agent")
    
    def handle_request(self, method: str, params: dict) -> dict:
        if method == "summarize_text":
            text = params.get("text", "")
            max_length = params.get("max_length", config.SUMMARY_MAX_LENGTH)
            try:
                summary = self.run(text, max_length)
                return {"success": True, "data": summary}
            except Exception as e:
                return {"success": False, "error": str(e)}
        return {"success": False, "error": "Unknown method"}
    
    def run(self, text: str, max_length: int = None) -> str:
        """Summarize text using available methods"""
        if not text.strip():
            return "No content to summarize."
        
        max_length = max_length or config.SUMMARY_MAX_LENGTH
        
        # Try OpenRouter API first (if available)
        if config.OPENROUTER_API_KEY:
            try:
                return self._summarize_openrouter(text, max_length)
            except Exception as e:
                print(f"OpenRouter failed: {e}, using fallback...")
        
        # Fallback to extractive summarization (always free)
        return self._extractive_summary(text, max_length)
    
    def _summarize_openrouter(self, text: str, max_length: int) -> str:
        """Summarize using OpenRouter free models"""
        headers = {
            "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Use free model
        payload = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {
                    "role": "user", 
                    "content": f"Summarize this text in under {max_length} words:\n\n{text[:3000]}"
                }
            ],
            "max_tokens": max_length * 2,
            "temperature": 0.3
        }
        
        response = requests.post(
            config.OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    
    def _extractive_summary(self, text: str, max_length: int) -> str:
        """Free extractive summarization (no API needed)"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        if len(sentences) <= 3:
            return text
        
        # Score sentences by length and position
        scored = []
        for i, sentence in enumerate(sentences):
            score = len(sentence.split())
            if i < len(sentences) * 0.3:  # Boost early sentences
                score *= 1.5
            scored.append((score, i, sentence))
        
        # Select top sentences
        scored.sort(reverse=True)
        selected = []
        word_count = 0
        
        for score, orig_idx, sentence in scored:
            sentence_words = len(sentence.split())
            if word_count + sentence_words <= max_length:
                selected.append((orig_idx, sentence))
                word_count += sentence_words
        
        # Restore original order
        selected.sort()
        summary = '. '.join([sentence for _, sentence in selected])
        return summary + '.' if summary else "Unable to generate summary."

class CoordinatorAgent(MCPAgent):
    """Main coordinator that orchestrates other agents"""
    
    def __init__(self):
        super().__init__("coordinator")
        self.transcript_agent = TranscriptAgent()
        self.search_agent = SearchAgent()
        self.summarizer_agent = SummarizerAgent()
    
    def handle_request(self, method: str, params: dict) -> dict:
        return {"success": False, "error": "Coordinator handles orchestration only"}
    
    def run(self, user_input: str) -> str:
        """Orchestrate agents based on input"""
        print(f"\n🤖 Coordinator starting workflow for: {user_input[:50]}...")
        
        if self._is_youtube_url(user_input):
            return self._handle_youtube_workflow(user_input)
        else:
            return self._handle_search_workflow(user_input)
    
    def _is_youtube_url(self, text: str) -> bool:
        return any(domain in text.lower() for domain in ["youtube.com", "youtu.be"])
    
    def _handle_youtube_workflow(self, url: str) -> str:
        """Agent-to-agent workflow for YouTube analysis"""
        print("\n📋 YouTube Analysis Workflow")
        print("=" * 40)
        
        # Step 1: Coordinator → Transcript Agent
        message1 = self.send_message("transcript_agent", "extract_transcript", {"url": url})
        response1 = self.transcript_agent.receive_message(message1)
        
        if not response1["success"]:
            return f"❌ Transcript extraction failed: {response1['error']}"
        
        transcript = response1["data"]
        print(f"✅ Transcript extracted: {len(transcript)} characters")
        
        # Step 2: Coordinator → Summarizer Agent
        message2 = self.send_message("summarizer_agent", "summarize_text", {
            "text": transcript,
            "max_length": config.SUMMARY_MAX_LENGTH
        })
        response2 = self.summarizer_agent.receive_message(message2)
        
        if not response2["success"]:
            return f"❌ Summarization failed: {response2['error']}"
        
        summary = response2["data"]
        print(f"✅ Summary generated: {len(summary)} characters")
        
        # Format final response
        return f"""🎥 **YouTube Video Analysis**

📋 **Full Transcript** ({len(transcript)} chars)
{transcript[:500]}{'...' if len(transcript) > 500 else ''}

📊 **AI Summary**
{summary}

🔄 **Agent Communication Log**
1. coordinator → transcript_agent: extract_transcript
2. transcript_agent → coordinator: success
3. coordinator → summarizer_agent: summarize_text  
4. summarizer_agent → coordinator: success

✅ **Workflow Complete**"""
    
    def _handle_search_workflow(self, query: str) -> str:
        """Agent-to-agent workflow for search and summarization"""
        print(f"\n🔍 Search Analysis Workflow")
        print("=" * 40)
        
        # Step 1: Coordinator → Search Agent
        message1 = self.send_message("search_agent", "web_search", {"query": query})
        response1 = self.search_agent.receive_message(message1)
        
        if not response1["success"]:
            return f"❌ Search failed: {response1['error']}"
        
        search_results = response1["data"]
        print(f"✅ Search completed: {len(search_results)} characters")
        
        # Step 2: Coordinator → Summarizer Agent
        message2 = self.send_message("summarizer_agent", "summarize_text", {
            "text": search_results,
            "max_length": config.SUMMARY_MAX_LENGTH
        })
        response2 = self.summarizer_agent.receive_message(message2)
        
        if not response2["success"]:
            return f"❌ Summarization failed: {response2['error']}"
        
        summary = response2["data"]
        print(f"✅ Summary generated: {len(summary)} characters")
        
        # Format final response
        return f"""🔍 **Research Results for: "{query}"**

📊 **AI Summary**
{summary}

📋 **Detailed Search Results**
{search_results[:800]}{'...' if len(search_results) > 800 else ''}

🔄 **Agent Communication Log**  
1. coordinator → search_agent: web_search
2. search_agent → coordinator: success
3. coordinator → summarizer_agent: summarize_text
4. summarizer_agent → coordinator: success

✅ **Workflow Complete**"""
