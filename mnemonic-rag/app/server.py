from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
import sys
#sys.path.append(r"C:\Users\fredr\AI\mnemonic-io-rag\mnemonic-rag\packages\retrieval-agent")
from retrieval_agent.chain import agent_executor as retrieval_agent_chain

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(app, retrieval_agent_chain, path="/retrieval-agent")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
