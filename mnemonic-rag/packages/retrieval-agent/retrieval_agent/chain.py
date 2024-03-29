import os
from typing import List, Tuple
import json


from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field


from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.retrievers.multi_query import MultiQueryRetriever

from langchain.schema import Document

from qdrant_client import QdrantClient

# load data from json (from scraper, moved to app)
with open("./packages/retrieval-agent/data/output.json") as json_file:
    data = json.load(json_file)

# Create documents suitable for retrieval

page_content = []
metadatas = []

for i in data:
    content = f'{i["title"]} \n\n {i["ingress"]} \n\n {i["content"]} \n\n {i["url"]}'
    metadata = {
        "title": i["title"],
        "source": i["url"],
        "category": i["category"],
        "subcategory": i["subcategory"],
    }
    page_content.append(content)
    metadatas.append(metadata)
    
# Prepare for embedding and indexing
docs = [Document(page_content=content, metadata=metadata) for content, metadata in zip(page_content, metadatas)]

embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="gpt-4-0125-preview")

url = "https://63c46998-a66f-476a-92b0-39675fe642cc.us-east4-0.gcp.cloud.qdrant.io:6333"
api_key = os.environ['QDRANT_MNEMONIC']

client = QdrantClient(
    url=url,
    api_key= api_key,
)

collection_name = "mnemonic-io"

vectorstore = Qdrant(
    client=client,
    collection_name=collection_name,
    embeddings=embedding_function,
)

#mnemonic_db = Chroma.from_documents(docs, embedding_function)

mnemonicRetriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(), llm=llm
)

description = (
    "A retriever for content on mnemonic.io. mnemonic is a cybersecurity company which publish content related to their field."
    "Useful for when you need to answer questions mnemonic, cyber security, or related topics."
    "Input should be a search query."
    "If it isn't clearly stated you can assume that the question is about mnemonic content."
    "If the answer is not satisfactory, you can ask for more information."
    "Do not provide answers that are not grounded in the search tool results."
)

# Create the tool
mnemonic_tool = create_retriever_tool(mnemonicRetriever, "mnemonic_search", description)
tools = [mnemonic_tool]
assistant_system_message = """You are the helpful mnemonic web page navigator assistant. \
Lookup relevant information as needed with you tools."""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", assistant_system_message),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])


def _format_chat_history(chat_history: List[Tuple[str, str]]):
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer


agent = (
    {
        "input": lambda x: x["input"],
        "chat_history": lambda x: _format_chat_history(x["chat_history"]),
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)


class AgentInput(BaseModel):
    input: str
    chat_history: List[Tuple[str, str]] = Field(
        ..., extra={"widget": {"type": "chat", "input": "input", "output": "output"}}
    )


agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True).with_types(
    input_type=AgentInput
)
