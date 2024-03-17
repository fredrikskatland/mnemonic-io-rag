from langchain.chains.query_constructor.schema import AttributeInfo
from langchain_core.documents import Document

# Qdrant collection name
DEFAULT_COLLECTION_NAME = "mnemonic-io"

# Here is a description of the dataset and metadata attributes. Metadata attributes will
# be used to filter the results of the query beyond the semantic search.
DEFAULT_DOCUMENT_CONTENTS = (
    "Information from the cyber security firm mnemonics web site. Contains information about their services, products, positions and blog posts."
)
DEFAULT_METADATA_FIELD_INFO = [
    AttributeInfo(
        name="title",
        description="The title of the web page",
        type="float",
    ),
    AttributeInfo(
        name="url",
        description="The URL of the web page",
        type="string",
    ),
    AttributeInfo(
        name="category",
        description="The category of the web page, example: 'careers', 'solutions', 'resources', 'company'",
        type="string or list[string]",
        enum = ["careers", "solutions", "resources", "company", "partners", "who-is-mnemonic", "expertise", "research and development", "legal"]
    ),
    AttributeInfo(
        name="subcategory",
        description="The subcategory of the web page, example: 'podcast','blog' ,'open-positions', 'om-mnemonic', 'events-webinars'",
        type="string or list[string]",
        enum = ["podcast", "open-positions", "om-mnemonic", "events-webinars", "blog", "whats-new", "enterprise-security-architecture", "ciso-for-hire"]
    ),
]
