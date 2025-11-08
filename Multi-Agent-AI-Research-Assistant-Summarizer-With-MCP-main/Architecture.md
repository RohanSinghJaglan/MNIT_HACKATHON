architecture.md:
```# 🏗️ System Architecture Documentation

## Overview

This document provides detailed architectural diagrams and technical specifications for the Multi-Agent AI Research Assistant & Summarizer with MCP integration.

## 🎯 System Architecture Diagrams

### 1. High-Level System Architecture

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI[Streamlit Web App]
        TABS[Tabbed Interface]
        INPUT[Topic Input]
        BUTTONS[Action Buttons]
        DISPLAY[Content Display]
    end
    
    subgraph "Application Logic Layer"
        CLIENT[MultiServerMCPClient]
        AGENTS[LangGraph React Agents]
        SESSION[Session Management]
        ASYNC[AsyncIO Handler]
    end
    
    subgraph "AI/LLM Layer"
        GEMINI[Google Gemini 2.0 Flash]
        PROMPTS[Prompt Templates]
        PARSERS[Output Parsers]
        CHAINS[LangChain Chains]
    end
    
    subgraph "MCP Protocol Layer"
        SERVER[FastMCP Server]
        TOOLS[MCP Tools Registry]
        TRANSPORT[HTTP Transport]
    end
    
    subgraph "External Services"
        DUCK[DuckDuckGo Search API]
        BRIGHT[BrightData Web Scraper]
        GENAI[Google GenAI API]
    end
    
    subgraph "Data Persistence"
        REPORTS[Markdown Reports]
        STATE[Session State]
        CACHE[Streamlit Cache]
    end
    
    UI --> CLIENT
    CLIENT --> AGENTS
    AGENTS --> GEMINI
    AGENTS --> SERVER
    SERVER --> TOOLS
    TOOLS --> DUCK
    TOOLS --> BRIGHT
    GEMINI --> GENAI
    AGENTS --> REPORTS
    UI --> SESSION
    SESSION --> STATE
    CLIENT --> CACHE
```

### 2. Multi-Agent System Architecture

```mermaid
graph LR
    subgraph "Agent Ecosystem"
        direction TB
        RA[Report Agent<br/>📊 Research & Analysis]
        SA[Summary Agent<br/>📝 Content Summarization]
        NA[News Agent<br/>📰 News Aggregation]
        QA[Q&A Agent<br/>🤖 Question Answering]
        FA[Feedback Agent<br/>💬 Sentiment Analysis]
    end
    
    subgraph "LangGraph Components"
        direction TB
        REACT[React Agent Executor]
        MEMORY[Agent Memory]
        TOOLS_REG[Tools Registry]
        STATE_GRAPH[State Graph]
    end
    
    subgraph "MCP Tools Interface"
        direction TB
        ST[search_topic<br/>🔍 Web Search]
        SUM[summarize_topic<br/>📄 Text Summary]
        NT[get_news_topic<br/>📡 News Fetch]
    end
    
    subgraph "Prompt Engineering"
        direction TB
        RP[Research Prompts]
        SP[Summary Prompts]
        NP[News Prompts]
        QP[Q&A Prompts]
        FP[Feedback Prompts]
    end
    
    RA --> REACT
    SA --> REACT
    NA --> REACT
    QA --> MEMORY
    FA --> STATE_GRAPH
    
    REACT --> ST
    REACT --> SUM
    REACT --> NT
    
    RA --> RP
    SA --> SP
    NA --> NP
    QA --> QP
    FA --> FP
```

### 3. Data Flow Architecture

```mermaid
flowchart TD
    START([User Input]) --> VALIDATE{Valid Topic?}
    VALIDATE -->|No| ERROR[Display Error]
    VALIDATE -->|Yes| ROUTE{Action Type?}
    
    ROUTE -->|Report| REPORT_FLOW[Report Generation Flow]
    ROUTE -->|Summary| SUMMARY_FLOW[Summary Generation Flow]
    ROUTE -->|News| NEWS_FLOW[News Fetching Flow]
    ROUTE -->|Q&A| QA_FLOW[Question Answering Flow]
    ROUTE -->|Feedback| FEEDBACK_FLOW[Feedback Processing Flow]
    
    subgraph "Report Generation Flow"
        REPORT_FLOW --> SEARCH[Search Topic via MCP]
        SEARCH --> NEWS_FETCH[Fetch Related News]
        NEWS_FETCH --> MERGE[Merge Report + News]
        MERGE --> FORMAT_REPORT[Format Report]
        FORMAT_REPORT --> SAVE_REPORT[Save as Markdown]
    end
    
    subgraph "Summary Generation Flow"
        SUMMARY_FLOW --> CHECK_REPORT{Report Exists?}
        CHECK_REPORT -->|No| NO_REPORT[Request Report First]
        CHECK_REPORT -->|Yes| SUMMARIZE[Generate Summary]
        SUMMARIZE --> FORMAT_SUMMARY[Format Summary]
    end
    
    subgraph "News Fetching Flow"
        NEWS_FLOW --> FETCH_NEWS[Fetch Latest News]
        FETCH_NEWS --> PARSE_NEWS[Parse News Content]
        PARSE_NEWS --> FORMAT_NEWS[Format News Display]
    end
    
    subgraph "Q&A Flow"
        QA_FLOW --> GET_CONTEXT[Get Report Context]
        GET_CONTEXT --> PROCESS_QUESTION[Process Question]
        PROCESS_QUESTION --> GENERATE_ANSWER[Generate Answer]
        GENERATE_ANSWER --> UPDATE_CHAT[Update Chat History]
    end
    
    subgraph "Feedback Flow"
        FEEDBACK_FLOW --> CLASSIFY[Classify Sentiment]
        CLASSIFY --> BRANCH{Positive/Negative?}
        BRANCH -->|Positive| POSITIVE_RESPONSE[Generate Positive Response]
        BRANCH -->|Negative| NEGATIVE_RESPONSE[Generate Negative Response]
        POSITIVE_RESPONSE --> DISPLAY_FEEDBACK[Display Response]
        NEGATIVE_RESPONSE --> DISPLAY_FEEDBACK
    end
    
    SAVE_REPORT --> DISPLAY[Display Results]
    FORMAT_SUMMARY --> DISPLAY
    FORMAT_NEWS --> DISPLAY
    UPDATE_CHAT --> DISPLAY
    DISPLAY_FEEDBACK --> DISPLAY
    NO_REPORT --> DISPLAY
    ERROR --> DISPLAY
    
    DISPLAY --> END([End])
```

### 4. MCP Protocol Integration

```mermaid
sequenceDiagram
    participant UI as Streamlit UI
    participant Client as MCP Client
    participant Server as FastMCP Server
    participant Tools as MCP Tools
    participant External as External APIs
    
    Note over UI,External: MCP Protocol Communication Flow
    
    UI->>Client: Initialize MCP Connection
    Client->>Server: Connect via HTTP Transport
    Server-->>Client: Connection Established
    
    UI->>Client: Request Available Tools
    Client->>Server: GET /tools
    Server-->>Client: Return Tools Registry
    Client-->>UI: Tools Available
    
    loop For Each Research Request
        UI->>Client: Invoke Tool (search_topic)
        Client->>Server: POST /tool/search_topic
        Server->>Tools: Execute search_topic
        Tools->>External: Query DuckDuckGo/BrightData
        External-->>Tools: Return Search Results
        Tools-->>Server: Processed Results
        Server-->>Client: Tool Response
        Client-->>UI: Formatted Results
    end
    
    Note over UI,External: Asynchronous Processing
    
    par Parallel Tool Execution
        UI->>Client: search_topic
        and UI->>Client: get_news_topic
    end
    
    Client-->>UI: Combined Results
```

### 5. Agent Interaction Patterns

```mermaid
stateDiagram-v2
    [*] --> Idle
    
    Idle --> ReportGeneration : Generate Report
    Idle --> SummaryGeneration : Generate Summary
    Idle --> NewsAggregation : Fetch News
    Idle --> QuestionAnswering : Ask Question
    Idle --> FeedbackProcessing : Submit Feedback
    
    state ReportGeneration {
        [*] --> SearchingTopic
        SearchingTopic --> FetchingNews
        FetchingNews --> MergingContent
        MergingContent --> FormattingReport
        FormattingReport --> SavingReport
        SavingReport --> [*]
    }
    
    state SummaryGeneration {
        [*] --> CheckingReport
        CheckingReport --> GeneratingSummary : Report Exists
        CheckingReport --> RequestingReport : No Report
        GeneratingSummary --> FormattingSummary
        FormattingSummary --> [*]
        RequestingReport --> [*]
    }
    
    state NewsAggregation {
        [*] --> FetchingLatestNews
        FetchingLatestNews --> ParsingNewsContent
        ParsingNewsContent --> FormattingNewsDisplay
        FormattingNewsDisplay --> [*]
    }
    
    state QuestionAnswering {
        [*] --> RetrievingContext
        RetrievingContext --> ProcessingQuestion
        ProcessingQuestion --> GeneratingAnswer
        GeneratingAnswer --> UpdatingChatHistory
        UpdatingChatHistory --> [*]
    }
    
    state FeedbackProcessing {
        [*] --> ClassifyingSentiment
        ClassifyingSentiment --> GeneratingResponse
        GeneratingResponse --> [*]
    }
    
    ReportGeneration --> Idle : Complete
    SummaryGeneration --> Idle : Complete
    NewsAggregation --> Idle : Complete
    QuestionAnswering --> Idle : Complete
    FeedbackProcessing --> Idle : Complete
```

## 🔧 Technical Implementation Details

### Agent Configuration

```python
# Report Agent Configuration
get_report_agent = create_react_agent(
    model=gemini_llm,
    tools=mcp_tools,
    prompt="""
    Research assistant with structured reporting capabilities.
    Uses search_topic tool for comprehensive information gathering.
    Outputs: Title, Introduction, Key Findings, Sources, Conclusion
    """
)

# Summary Agent Configuration  
get_summary_agent = create_react_agent(
    model=gemini_llm,
    tools=mcp_tools,
    prompt="""
    Summarization specialist for content condensation.
    Uses summarize_topic tool for key point extraction.
    Outputs: Title, Summary, Key Highlights, Conclusion
    """
)

# News Agent Configuration
get_news_agent = create_react_agent(
    model=gemini_llm,
    tools=mcp_tools,
    prompt="""
    News aggregation specialist for current events.
    Uses get_news_topic tool for latest information.
    Outputs: Headlines, Summary, Key Details, Sources
    """
)
```

### MCP Server Tools

```python
@mcp.tool()
async def search_topic(topic: str) -> str:
    """
    Comprehensive topic search with source attribution.
    Integrates multiple search engines via MCP protocol.
    """
    
@mcp.tool()
def summarize_topic(context: str) -> str:
    """
    Intelligent text summarization with key point extraction.
    Maintains context while reducing content length.
    """
    
@mcp.tool()
async def get_news_topic(topic: str) -> str:
    """
    Real-time news aggregation with fact verification.
    Sources from reliable news outlets with timestamps.
    """
```

### Asynchronous Processing

```python
async def generate_report_task(topic):
    # Parallel execution of report and news generation
    report_task = get_report_agent.ainvoke({"messages": [...]})
    news_task = get_news_agent.ainvoke({"messages": [...]})
    
    report_text, news_text = await asyncio.gather(
        report_task, news_task
    )
    
    # Merge and synthesize content
    merged_report = await merge_content(report_text, news_text)
    return merged_report
```

## 🔄 Integration Patterns

### 1. MCP Client Integration
- **Connection Management**: Persistent HTTP connections to MCP servers
- **Tool Discovery**: Dynamic tool registration and capability detection
- **Error Handling**: Graceful degradation when tools are unavailable

### 2. LangGraph Agent Orchestration
- **React Pattern**: Reasoning and acting cycles for complex tasks
- **Memory Management**: Context retention across agent interactions
- **Tool Selection**: Intelligent tool choice based on task requirements

### 3. Streamlit UI Integration
- **Session State**: Persistent data across user interactions
- **Async Handling**: Non-blocking UI updates during processing
- **Component Caching**: Performance optimization for repeated operations

## 📊 Performance Considerations

### Scalability Factors
- **Concurrent Requests**: AsyncIO enables multiple simultaneous operations
- **Memory Management**: Efficient session state handling
- **API Rate Limits**: Built-in throttling for external services

### Optimization Strategies
- **Caching**: Streamlit resource caching for MCP clients
- **Lazy Loading**: On-demand tool initialization
- **Batch Processing**: Grouped API calls where possible

## 🔒 Security Architecture

### API Key Management
- Environment variable isolation
- Secure credential storage
- API key rotation support

### Data Privacy
- Local report storage
- Session-based data isolation
- No persistent user data collection

### Input Validation
- Topic input sanitization
- MCP response validation
- Error boundary implementation

---

This architecture supports a robust, scalable, and maintainable multi-agent AI system with clear separation of concerns and efficient resource utilization.```