# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.indexes import SQLRecordManager, index as langchain_index
from langchain_core.documents import Document

from qdrant_client import QdrantClient

import json
import os

class MnemonicscraperPipeline:
    def __init__(self):

        self.embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
        
         # Set up a vector store to store your vectors and metadata
        self.url = "https://63c46998-a66f-476a-92b0-39675fe642cc.us-east4-0.gcp.cloud.qdrant.io:6333"
        self.api_key = os.environ['QDRANT_MNEMONIC']
        
        self.client = QdrantClient(
            url=self.url,
            api_key= self.api_key,
        )

        self.collection_name = "mnemonic-io"

        self.vectorstore = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embedding_function,
        )

        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item
    
    def close_spider(self, spider):
        results = self._index_batch(self.items)
        print(results)
    
    def _index_batch(self, items):

        namespace = f"qdrant/{self.collection_name}"
        record_manager = SQLRecordManager(
            namespace, db_url="sqlite:///record_manager_cache.sql"
        )
        record_manager.create_schema()

        page_content = []
        metadatas = []

        for i in self.items:
            content = f'{i.get("title","")} \n\n {i.get("ingress","")} \n\n {i.get("content","")} \n\n {i["url"]}'
            metadata = {
                "title": i.get("title",""),
                "url": i.get("url",""),
                "category": i.get("category",""),
                "subcategory": i.get("subcategory",""),
            }
            page_content.append(content)
            metadatas.append(metadata)

        docs = [Document(page_content=content, metadata=metadata) for content, metadata in zip(page_content, metadatas)]

        results =langchain_index(
            docs,
            record_manager,
            self.vectorstore,
            cleanup="incremental",
            source_id_key="url"
        )
        return results
        
