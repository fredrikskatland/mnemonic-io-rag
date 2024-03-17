import os
from typing import List, Optional

from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers import SelfQueryRetriever
from langchain_community.llms import BaseLLM
from langchain_community.llms.openai import OpenAI
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_core.documents import Document #, StrOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.embeddings import Embeddings
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from qdrant_client import QdrantClient
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from self_query_qdrant import defaults, helper, prompts


class Query(BaseModel):
    __root__: str


def create_chain(
    llm: Optional[BaseLLM] = None,
    embeddings: Optional[Embeddings] = None,
    document_contents: str = defaults.DEFAULT_DOCUMENT_CONTENTS,
    metadata_field_info: List[AttributeInfo] = defaults.DEFAULT_METADATA_FIELD_INFO,
    collection_name: str = defaults.DEFAULT_COLLECTION_NAME,
):
    """
    Create a chain that can be used to query a Qdrant vector store with a self-querying
    capability. By default, this chain will use the OpenAI LLM and OpenAIEmbeddings, and
    work with the default document contents and metadata field info. You can override
    these defaults by passing in your own values.
    :param llm: an LLM to use for generating text
    :param embeddings: an Embeddings to use for generating queries
    :param document_contents: a description of the document set
    :param metadata_field_info: list of metadata attributes
    :param collection_name: name of the Qdrant collection to use
    :return:
    """
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    llm = ChatOpenAI(model="gpt-4-0125-preview")

    llm = llm or OpenAI()
    embeddings = embedding_function or OpenAIEmbeddings()

    # Set up a vector store to store your vectors and metadata

    url = "https://63c46998-a66f-476a-92b0-39675fe642cc.us-east4-0.gcp.cloud.qdrant.io:6333"
    api_key = os.environ['QDRANT_MNEMONIC']

    client = QdrantClient(
        url=url,
        api_key=api_key,
    )
    vectorstore = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
    )

    # Set up a retriever to query your vector store with self-querying capabilities
    retriever = SelfQueryRetriever.from_llm(
        llm, vectorstore, document_contents, metadata_field_info, verbose=True
    )

    context = RunnableParallel(
        context=retriever | helper.combine_documents,
        query=RunnablePassthrough(),
    )
    pipeline = context | prompts.LLM_CONTEXT_PROMPT | llm | StrOutputParser()
    return pipeline.with_types(input_type=Query)

# Create the default chain
chain = create_chain()
