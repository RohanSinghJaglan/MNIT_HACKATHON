from fastmcp import FastMCP
from get_mcp import get_mcp_use
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm import get_llm


gemin_llm=get_llm()

mcp=FastMCP("search_and_summarize")

str_parse=StrOutputParser()
@mcp.tool()
async def search_topic(topic: str) -> str:
    """
    Search for a topic and returning a clear summary with sources.

    Args:
        topic (str): The topic to search.

    Returns:
        str: A concise response with details and source links.
    """

    prompt = PromptTemplate(
        template="""
        You are a search assistant. Use available search tools to gather reliable information 
        on the topic: {topic}.

        - Provide a clear and detailed response.  
        - Include the sources (website names/links) where the information was found.  
        - Ensure the response is accurate, concise, and well-structured.  
        """,
        input_variables=['topic']
    )

     # Generate prompt text
    prompt_text = str(prompt.invoke({'topic': topic}))

    # Await MCP agent to process the prompt
    result = await get_mcp_use(prompt_text)

    # Parse result into string
    result_parse = str_parse.parse(result)
    return result_parse

    # chain= prompt | get_mcp_use | str_parse
    # result= chain.invoke({'topic':topic})
    # return result

@mcp.tool()
def summarize_topic(context:str)->str:
    """
    Summarize the given context clearly and concisely.

    Args:
        context (str): The text to summarize.

    Returns:
        str: A short, clear summary of the context.
    """

    prompt = PromptTemplate(
        template="You are an AI assistant. Summarize the following context clearly and concisely:\n {context}",
        input_variables=['context']
    )

    chain= prompt | gemin_llm | str_parse
    result=chain.invoke({'context':context})
    return result

@mcp.tool()
async def get_news_topic(topic:str)->str:
    """
    Fetch the latest reliable news about a topic with sources.

    Args:
        topic (str): The news topic to search.

    Returns:
        str: A concise summary of recent news with source links.
    """


    prompt = PromptTemplate(
    template="""
    You are a news assistant. Use available news tools to gather the **latest and most reliable** news 
    about: {topic}.

    - Summarize the key points in a clear and concise manner.  
    - Highlight the most recent updates (if available).  
    - Include the news sources (website names/links) where the information was found.  
    - Ensure the response is factual, unbiased, and well-structured.  
    """,
    input_variables=['topic']
    )

    prompt_text = str(prompt.invoke({'topic': topic}))

    # Await MCP agent to process the prompt
    result = await get_mcp_use(prompt_text)

    # Parse result into string
    result_parse = str_parse.parse(result)
    return result_parse

if __name__=="__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)


