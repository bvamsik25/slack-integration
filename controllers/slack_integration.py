from fastapi import APIRouter, Request
from services import slack_integration as slack_integration_service

router = APIRouter()


@router.get("/live")
async def hi():
    return 'Hi, im running!'


@router.get("/send-blockkit")
async def send_blockkit():
    response = slack_integration_service.send_homepage()
    return response.json()


@router.post("/slack/interactions")
async def slack_interactions(request: Request):
    payload = await request.json()
    return await slack_integration_service.slack_interaction(payload)
