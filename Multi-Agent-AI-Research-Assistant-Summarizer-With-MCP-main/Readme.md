

readme.md:
```
# 🤖 Multi-Agent AI Research Assistant & Summarizer With MCP

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://langchain.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.1+-purple.svg)](https://langgraph.com)
[![MCP](https://img.shields.io/badge/MCP-Protocol-orange.svg)](https://modelcontextprotocol.io)

A sophisticated multi-agent AI platform that leverages **LangGraph**, **Model Context Protocol (MCP)**, and **Google Gemini 2.0 Flash** to deliver comprehensive research, summarization, news aggregation, Q&A, and intelligent feedback processing capabilities.

## 🎯 Overview

This hackathon project combines cutting-edge AI technologies to create an intelligent research assistant that can:
- Generate detailed research reports with multiple data sources
- Provide concise summaries of complex topics
- Fetch and analyze latest news with fact-checking
- Answer questions based on research context
- Process user feedback with sentiment analysis

## 🏗️ System Architecture

### High-Level Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Streamlit UI]
        TABS[Report/Summary/News/Q&A Tabs]
    end
    
    subgraph "Application Layer"
        CLIENT[MCP Client]
        AGENTS[LangGraph React Agents]
        LLM[Google Gemini 2.0 Flash]
    end
    
    subgraph "MCP Server Layer"
        SERVER[FastMCP Server]
        TOOLS[MCP Tools]
    end
    
    subgraph "External Services"
        DUCK[DuckDuckGo Search]
        BRIGHT[BrightData API]
        GEMINI[Google Gemini API]
    end
    
    subgraph "Data Storage"
        REPORTS[Local MD Files]
        SESSION[Session State]
    end
    
    UI --> CLIENT
    CLIENT --> AGENTS
    AGENTS --> LLM
    AGENTS --> SERVER
    SERVER --> TOOLS
    TOOLS --> DUCK
    TOOLS --> BRIGHT
    LLM --> GEMINI
    AGENTS --> REPORTS
    UI --> SESSION
```

### Multi-Agent System Flow

```mermaid
graph LR
    subgraph "Agent Orchestration"
        RA[Report Agent]
        SA[Summary Agent]
        NA[News Agent]
        QA[Q&A Agent]
        FA[Feedback Agent]
    end
    
    subgraph "MCP Tools"
        ST[search_topic]
        SU[summarize_topic]
        NT[get_news_topic]
    end
    
    subgraph "LangGraph Components"
        RE[React Executor]
        PM[Prompt Manager]
        OP[Output Parser]
    end
    
    RA --> ST
    SA --> SU
    NA --> NT
    QA --> PM
    FA --> PM
    
    ST --> RE
    SU --> RE
    NT --> RE
    
    RE --> OP
```

## 🔄 User Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant Agent as LangGraph Agent
    participant MCP as MCP Server
    participant Tools as External APIs
    participant Storage as File System
    
    User->>UI: Enter research topic
    User->>UI: Click "Generate Report"
    
    UI->>Agent: Invoke report_agent
    Agent->>MCP: Call search_topic tool
    MCP->>Tools: Query DuckDuckGo/BrightData
    Tools-->>MCP: Return search results
    MCP-->>Agent: Processed results
    
    Agent->>MCP: Call get_news_topic tool
    MCP->>Tools: Fetch latest news
    Tools-->>MCP: Return news data
    MCP-->>Agent: Processed news
    
    Agent->>Agent: Merge report + news
    Agent-->>UI: Return comprehensive report
    
    UI->>Storage: Save report as MD file
    UI->>User: Display formatted report
    
    alt Summary Generation
        User->>UI: Click "Generate Summary"
        UI->>Agent: Invoke summary_agent
        Agent->>MCP: Call summarize_topic
        MCP-->>Agent: Return summary
        Agent-->>UI: Formatted summary
        UI->>User: Display summary
    end
    
    alt Q&A Interaction
        User->>UI: Ask question
        UI->>Agent: Invoke Q&A with context
        Agent->>Agent: Process with report context
        Agent-->>UI: Return answer
        UI->>User: Display answer
    end
    
    alt Feedback Processing
        User->>UI: Submit feedback
        UI->>Agent: Invoke feedback_agent
        Agent->>Agent: Classify sentiment
        Agent->>Agent: Generate response
        Agent-->>UI: Return personalized response
        UI->>User: Display AI response
    end
```

## 🛠️ Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Interactive web interface |
| **Backend** | Python + AsyncIO | Asynchronous processing |
| **AI Framework** | LangChain + LangGraph | Agent orchestration |
| **LLM** | Google Gemini 2.0 Flash | Language model |
| **Multi-Agent** | LangGraph React Agents | Specialized AI agents |
| **Protocol** | Model Context Protocol (MCP) | Tool integration |
| **Search** | DuckDuckGo MCP Server | Web search capabilities |
| **Data** | BrightData API | Enhanced web scraping |
| **Storage** | Local Markdown Files | Report persistence |

## 🚀 Features

### 🔍 Core Functionality
- **Intelligent Research Reports**: Generate comprehensive reports with title, introduction, key findings, sources, and conclusions
- **Smart Summarization**: Convert complex reports into digestible summaries with key highlights
- **Real-time News Aggregation**: Fetch latest reliable news with fact-checking and source verification
- **Context-Aware Q&A**: Ask questions based on generated research content
- **Sentiment-Based Feedback**: Automatic feedback classification with personalized AI responses

### 🤖 Advanced AI Features
- **Multi-Agent Orchestration**: Specialized agents for different tasks using LangGraph
- **Agentic Reasoning**: Dynamic tool usage and multi-step task execution
- **MCP Integration**: Seamless connection to external data sources
- **Asynchronous Processing**: Real-time interactions with concurrent operations
- **Memory Management**: Session-based context retention

### 🎨 User Experience
- **Tabbed Interface**: Organized sections for Reports, Summary, News, and Q&A
- **Color-Coded Sections**: Visual distinction between different content types
- **Auto-Save Reports**: Automatic markdown file generation with timestamps
- **Responsive Design**: Clean, modern interface with intuitive navigation

## 📁 Project Structure

```
multi-agent-ai-research-assistant/
├── research_client_ui.py      # Main Streamlit application
├── research_server.py         # FastMCP server with tools
├── get_mcp.py                # MCP client configuration
├── llm.py                    # Google Gemini LLM setup
├── feedback.py               # Sentiment analysis & response
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── reports/                 # Generated research reports
│   ├── report_2025-*.md    # Timestamped report files
└── screenshot_demo/         # Demo screenshots
```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js (for MCP servers)
- Google Gemini API key
- BrightData API token (optional)

### 1. Clone Repository
```bash
git clone <repository-url>
cd multi-agent-ai-research-assistant
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create `.env` file:
```env
api_key=YOUR_GOOGLE_GENAI_API_KEY
BRIGHT_DATA_API_TOKEN=YOUR_BRIGHTDATA_API_TOKEN
WEB_UNLOCKER_ZONE=unblocker
BROWSER_ZONE=scraping_browser
```

### 5. Start MCP Servers
```bash
# Terminal 1: DuckDuckGo MCP Server
npx duckduckgo-mcp-server

# Terminal 2: BrightData MCP Server (optional)
npx @brightdata/mcp
```

### 6. Launch Application
```bash
# Terminal 3: Main Application
streamlit run research_client_ui.py
```

## 🎮 Usage Guide

### Basic Workflow
1. **Enter Topic**: Input your research subject in the text field
2. **Generate Content**: Choose from Report, News, or Summary generation
3. **Interactive Q&A**: Ask questions about the generated content
4. **Provide Feedback**: Submit feedback to receive personalized AI responses

### Advanced Features
- **Report Merging**: Automatically combines research data with latest news
- **Context-Aware Answers**: Q&A agent uses report content as primary context
- **Sentiment Analysis**: Feedback system classifies and responds appropriately
- **Auto-Save**: All reports saved as timestamped markdown files

## 🔧 Configuration

### MCP Server Configuration
```python
config = {
    "mcpServers": {
        "duckduckgo-search": {
            "command": "npx",
            "args": ["-y", "duckduckgo-mcp-server"]
        },
        "bright_data": {
            "command": "npx",
            "args": ["@brightdata/mcp"],
            "env": {
                "API_TOKEN": "your_token",
                "WEB_UNLOCKER_ZONE": "unblocker",
                "BROWSER_ZONE": "scraping_browser"
            }
        }
    }
}
```

### Agent Prompts
Each agent has specialized prompts for optimal performance:
- **Report Agent**: Structured research with sources
- **Summary Agent**: Concise key points extraction
- **News Agent**: Latest reliable news aggregation
- **Q&A Agent**: Context-aware question answering

## 🚀 Deployment

### Local Development
```bash
streamlit run research_client_ui.py
```

### Production Deployment
1. Configure environment variables
2. Set up MCP servers as services
3. Deploy Streamlit app to cloud platform
4. Ensure API keys are securely managed

## 🔮 Future Enhancements

- [ ] **Additional MCP Servers**: Wikipedia, academic databases, social media
- [ ] **LangGraph Workflows**: Complex multi-step research pipelines
- [ ] **Visual Analytics**: Charts and graphs for report insights
- [ ] **Export Options**: PDF, DOCX, and presentation formats
- [ ] **Collaborative Features**: Multi-user research sessions
- [ ] **Advanced Memory**: Persistent conversation history
- [ ] **Custom Agents**: User-defined specialized research agents

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain Team** for the powerful AI framework
- **LangGraph** for multi-agent orchestration capabilities
- **Google** for Gemini 2.0 Flash API
- **Streamlit** for the intuitive web framework
- **MCP Community** for the Model Context Protocol

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Join our community discussions
- Check the documentation

---

**Built with ❤️ for the AI community**
```