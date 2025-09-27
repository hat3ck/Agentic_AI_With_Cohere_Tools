from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app import database
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/api/llm",
    tags=["llm"],
    responses={404: {"description": "Not found"}},
)
@router.get(
        "/chat",
        summary="Chat Endpoint",
        description="A simple chat endpoint that sends and receives messages from Cohere's API.",
        response_description="The response from the chat endpoint.",
        )
async def chat_endpoint(message: str = Query(..., min_length=1, max_length=1000), db_session: Session = Depends(database.get_db)):
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    chat_service = ChatService(db_session)
    response = await chat_service.send_message(message)
    return {"response": response}

@router.get(
        "/prompts",
        summary="Get All Prompts",
        description="Fetch all LLM prompts from the database.",
        response_description="A list of LLM prompts.",
        )
async def get_all_prompts(db_session: Session = Depends(database.get_db)):
    chat_service = ChatService(db_session)
    prompts = await chat_service.get_all_prompts()
    return {"prompts": prompts}

@router.get(
        "/chat_with_tools",
        summary="Chat with Tools Endpoint",
        description="A chat endpoint that utilizes external tools like Wikipedia to enhance responses.",
        response_description="The response from the chat endpoint with tools.",
        )
async def chat_with_tools_endpoint(message: str = Query(..., min_length=1, max_length=1000), db_session: Session = Depends(database.get_db)):
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    chat_service = ChatService(db_session)
    response = await chat_service.chat_with_tools(message)
    return {"response": response}