from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch,RunnableLambda
from pydantic import BaseModel,Field
from typing import Literal
from llm import get_llm

gemini_llm=get_llm()

#schema
class feedback(BaseModel):
    sentiment:Literal['positive','negative']=Field(description="Give the sentiment of the feedback")

pydantic_parse=PydanticOutputParser(pydantic_object=feedback)
str_parse=StrOutputParser()

classify_prompt=PromptTemplate(
    template="Classify the sentiment of the following feedback text into postive or negative \n {feedback} \n {format_instruction}",
    input_variables=['feedback'],
    partial_variables={"format_instruction":pydantic_parse.get_format_instructions()}
)

classify_chain= classify_prompt | gemini_llm | pydantic_parse

positive_prompt = PromptTemplate(
    input_variables=['feedback'],
    template="""
    You are a friendly assistant. 
    Write a short, warm thank-you reply to this positive feedback:

    "{feedback}"
    Keep it concise (1–2 sentences).
    """
    )


negative_prompt = PromptTemplate(
    input_variables=['feedback'],
    template="""
    You are a professional assistant. 
    Write a short, polite, and supportive reply to this negative feedback:

    "{feedback}"
    Keep it concise (1–2 sentences).
    """
    )

feedback_chain=RunnableBranch(
    (lambda x:x.sentiment=="positive",positive_prompt | gemini_llm | str_parse),
    (lambda x:x.sentiment=="negative",negative_prompt | gemini_llm | str_parse),
    RunnableLambda(lambda x:"❌ Could not classify sentiment")
)

main_chain=classify_chain | feedback_chain

def get_feedback(feedback:str):
    result=main_chain.invoke({'feedback':feedback})
    return result
