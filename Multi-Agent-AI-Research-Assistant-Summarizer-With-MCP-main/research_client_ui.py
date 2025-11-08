import os
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '0'
os.environ['GRPC_POLL_STRATEGY'] = 'poll'

import streamlit as st
import asyncio
import datetime
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.runnables import RunnableLambda
from llm import get_llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from feedback import get_feedback
import re
from dotenv import load_dotenv

load_dotenv()

# Email authentication
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("Login Required")
    email = st.text_input("Enter your email:")
    if st.button("Login"):
        if email == os.getenv('STREAMLIT_EMAIL', 'krishagarwal52139@gmail.com'):
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Invalid email")
    st.stop()

# --- Initialize LLM & Parser ---
gemin_llm = get_llm()
str_parse = StrOutputParser()

# --- Streamlit Config ---
st.set_page_config(
    page_title="Multi-Agent AI Research Assistant & Summarizer With MCP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar / Header ---
st.sidebar.title("Multi-Agent AI Research Assistant & Summarizer With MCP")
st.sidebar.write("Generate detailed reports, summaries, interact with AI QnA, and give feedback.")
st.sidebar.markdown("---")

# --- Theme Colors ---
REPORT_COLOR = "#DDEBF7"    # Blue
NEWS_COLOR = "#DFF2BF"      # Green
SUMMARY_COLOR = "#EAD1DC"   # Purple
QNA_COLOR = "#FFE4B5"       # Orange

# --- MCP Client Initialization ---
@st.cache_resource
def init_client():
    return MultiServerMCPClient({
        "search_and_summarize": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http"
        }
    })

client = init_client()

async def load_tools():
    return await client.get_tools()

tools = asyncio.run(load_tools())

# --- Agents ---
def get_report_agent(topic):
    return gemin_llm.invoke(f"Research and create a detailed report on {topic} with Title, Introduction, Key Findings, Sources, and Conclusion.")

def get_summary_agent(content):
    return gemin_llm.invoke(f"Summarize this content: {content}")

def get_news_agent(topic):
    return gemin_llm.invoke(f"Get latest news on {topic} with Headlines, Summary, Key Details, and Sources.")

# --- Session State ---
if 'report' not in st.session_state:
    st.session_state['report'] = ""
if 'summary' not in st.session_state:
    st.session_state['summary'] = ""
if 'news' not in st.session_state:
    st.session_state['news'] = ""
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# --- Topic Input ---
st.subheader("📝 Enter Topic")
topic = st.text_input("Enter a topic to research:")

col1, col2, col3 = st.columns([1,1,1])
with col1:
    generate_report = st.button("Generate Detailed Report 📝")
with col2:
    generate_news = st.button("Fetch Latest News 📰")
with col3:
    generate_summary = st.button("Generate Summary 📄")

# --- Async Operations ---
async def generate_report_task(topic):
    report = get_report_agent(topic)
    report_text = str(report.content)
    news = get_news_agent(topic)
    news_text = str(news.content)
    
    merge_prompt = PromptTemplate(
        template="""
        You are an expert research and synthesis agent. Analyze the report and news, 
        then generate a single, comprehensive, well-structured report.

        Report Content:
        {report}

        News Content:
        {news}

        Instructions:
        - Integrate insights from both report and news
        - Include: Title, Introduction, Merged Insights, Key Highlights, Conclusion, Sources
        """,
        input_variables=["report", "news"]
    )
    merged_report = await (merge_prompt | gemin_llm | str_parse).ainvoke({'report':report_text,'news':news_text})
    return merged_report, news_text

async def generate_summary_task(report):
    summary = get_summary_agent(report)
    return str(summary.content)

async def fetch_news_task(topic):
    news = get_news_agent(topic)
    return str(news.content)

# --- Run Tasks ---
if topic:
    if generate_report:
        with st.spinner("Generating detailed report..."):
            report_text, news_text = asyncio.run(generate_report_task(topic))
            st.session_state['report'] = report_text
            st.session_state['news'] = news_text
            st.success("✅ Detailed report generated!")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            os.makedirs("reports", exist_ok=True)
            with open(f"reports/report_{timestamp}.md", "w", encoding="utf-8") as f:
                f.write(f"# Detailed Report on {topic}\n\n{report_text}")

    if generate_summary and st.session_state.get('report'):
        with st.spinner("Generating summary..."):
            summary_text = asyncio.run(generate_summary_task(st.session_state['report']))
            st.session_state['summary'] = summary_text
            st.success("✅ Summary generated!")

    if generate_news:
        with st.spinner("Fetching latest news..."):
            news_text = asyncio.run(fetch_news_task(topic))
            st.session_state['news'] = news_text
            st.success("✅ Latest news fetched!")

# --- Tabbed Output ---
tabs = st.tabs(["📄 Detailed Report","📝 Summary","📰 News","🤖 QnA"])
with tabs[0]:
    st.subheader("📄 Detailed Report")
    if st.session_state.get('report'):
        st.markdown(f"<div style='background-color:{REPORT_COLOR};padding:15px;border-radius:10px'>{st.session_state['report']}</div>", unsafe_allow_html=True)
    else:
        st.info("Generate a detailed report to see it here.")

with tabs[1]:
    st.subheader("📝 Summary")
    if st.session_state.get('summary'):
        with st.expander("View Summary"):
            st.markdown(f"<div style='background-color:{SUMMARY_COLOR};padding:10px;border-radius:10px'>{st.session_state['summary']}</div>", unsafe_allow_html=True)
    else:
        st.info("Generate a summary to see it here.")

with tabs[2]:
    st.subheader("📰 News")
    news_raw = st.session_state.get('news', "")

    if news_raw:
        news_raw = str(news_raw)  # ensure it's a string

        # Simple split by sections using regex fallback
        summary_match = re.search(r"\*\*Summary:\*\*(.*?)\*\*Key Details:\*\*", news_raw, re.S | re.M)
        keydetails_match = re.search(r"\*\*Key Details:\*\*(.*?)\*\*Sources:\*\*", news_raw, re.S | re.M)
        sources_match = re.search(r"\*\*Sources:\*\*(.*)", news_raw, re.S | re.M)

        summary = summary_match.group(1).strip() if summary_match else "No summary available."
        key_details_raw = keydetails_match.group(1).strip() if keydetails_match else ""
        sources_raw = sources_match.group(1).strip() if sources_match else ""

        key_details = [kd.strip("* \n") for kd in key_details_raw.split("\n") if kd.strip()]
        sources = [s.strip("* \n") for s in sources_raw.split("\n") if s.strip()]

        # Wrap all content in a single div with pre-wrap
        key_details_html = "".join([f"- {kd}\n" for kd in key_details])
        sources_html = "".join([f"- {src}\n" for src in sources])
        
        news_html = f"""
        <div style='background-color:{NEWS_COLOR};
                    padding:15px;
                    border-radius:10px;
                    white-space: pre-wrap;
                    line-height:1.5;'>
        <b>Summary:</b> {summary}

        <b>Key Details:</b>
        {key_details_html}
        <b>Sources:</b>
        {sources_html}
        </div>
        """
        st.markdown(news_html, unsafe_allow_html=True)

    else:
        st.info("Fetch news to see it here.")

with tabs[3]:
    st.subheader("🤖 Chat with AI QnA Agent")
    user_question = st.text_input("Ask a question:", key="qna_input")
    if st.button("Send Question"):
        if user_question:
            st.session_state['chat_history'].append({'user': user_question})

            prompt2 = PromptTemplate(
                template="""
                You are a QnA agent. Use the given context as the main reference, but if the context does not have enough information, generate the answer yourself using your knowledge.

                Context:  
                {detail_report}

                Question:  
                {user_question}

                Chat History:  
                {chat_history}

                Instructions:
                - First, try to answer based on the context.
                - If the context does not provide enough information, generate a valid and helpful answer yourself.
                - Always provide an answer; never say you cannot answer.
                """,
                input_variables=['detail_report','chat_history','user_question']
                )
            with st.spinner("🤖 AI is generating an answer..."):
                answer = asyncio.run((prompt2 | gemin_llm | str_parse).ainvoke({
                    'detail_report': st.session_state.get('report', ""),
                    'user_question': user_question,
                    'chat_history': st.session_state['chat_history']
                }))
                st.session_state['chat_history'].append({'bot': answer})

    for msg in st.session_state['chat_history']:
        if 'user' in msg:
            st.markdown(f"<div style='text-align:left'><b>You:</b> {msg['user']}</div>", unsafe_allow_html=True)
        if 'bot' in msg:
            st.markdown(f"<div style='text-align:right;background-color:{QNA_COLOR};padding:5px;border-radius:5px'><b>AI:</b> {msg['bot']}</div>", unsafe_allow_html=True)

    if st.button("Clear Chat"):
        st.session_state['chat_history'] = []

# --- Feedback Section ---
st.subheader("💬 Feedback & Rating")
feedback_input = st.text_area("Enter your feedback here:")
rating = st.slider("Rate this AI Assistant:", 1, 5, 5)
if st.button("Submit Feedback"):
    if feedback_input:
        feedback_response = get_feedback(feedback_input)
        st.success("✅ Feedback submitted!")
        st.markdown(f"**AI Response:** {feedback_response}")
        st.markdown(f"**Rating:** {'⭐'*rating}")
