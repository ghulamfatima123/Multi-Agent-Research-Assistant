"""
SMARA - Simplified Multi-Agent Research Assistant
Demonstrates Agent-to-Agent communication and MCP protocol
"""
import sys
from agents import CoordinatorAgent

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║   Multi-Agent Research Assistant                             ║
║     Agent-to-Agent Communication (MCP Protocol)              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def interactive_mode():
    coordinator = CoordinatorAgent()
    
    print("🔄 SMARA is ready! Enter your queries below.")
    print("   • Paste YouTube URL to analyze video")
    print("   • Enter topic to search and summarize")
    print("   • Type 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("📝 Query: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
                
            if not user_input:
                print("❌ Please enter a query or URL\n")
                continue
            
            print(f"\n🔄 Processing: {user_input}")
            print("=" * 60)
            
            result = coordinator.run(user_input)
            print(result)
            print("=" * 60)
            print("✅ Complete!\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

def single_query_mode(query: str):
    coordinator = CoordinatorAgent()
    print(f"🔄 Processing: {query}")
    print("=" * 60)
    
    try:
        result = coordinator.run(query)
        print(result)
        print("=" * 60)
        print("✅ Complete!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def main():
    print_banner()
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        single_query_mode(query)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()