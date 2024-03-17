from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
import sys
import os

pwd = os.getcwd()
sys.path.append(pwd+"\\packages\\retrieval-agent")

from retrieval_agent.chain import agent_executor as retrieval_agent_chain
from self_query_qdrant import chain as self_query_qdrant_chain

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(app, retrieval_agent_chain, path="/retrieval-agent")
add_routes(app, self_query_qdrant_chain, path="/self-query-qdrant")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
