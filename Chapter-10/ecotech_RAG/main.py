from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Body, FastAPI, Request
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import Chroma

from documents import get_context, load_documents
from model import chain


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Chroma(embedding_function=CohereEmbeddings(model="embed-english-v2.0"))
    await load_documents(db)
    yield {"db": db}


app = FastAPI(title="Ecotech AI Assistant", lifespan=lifespan)


@app.post("/message")
async def query_assistant(
    request: Request,
    question: Annotated[str, Body()],
) -> str:
    context = get_context(question, request.state.db)
    response = await chain.ainvoke(
        {
            "question": question,
            "context": context,
        }
    )
    return response
