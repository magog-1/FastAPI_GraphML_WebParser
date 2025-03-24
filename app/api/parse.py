from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
# from app.services.parse import parse_website_task
from celery.result import AsyncResult
from celery_app import parse_website_task

router = APIRouter()

class ParseRequest(BaseModel):
    url: str
    max_depth: int = 3
    format: str = "graphml"

class ParseStatusResponse(BaseModel):
    status: str
    progress: int = 0
    result: str = None

@router.post("/parse_website")
def start_parse(parse_req: ParseRequest):
    task = parse_website_task.apply_async(args=[parse_req.url, parse_req.max_depth, parse_req.format])
    return {"task_id": task.id}

@router.get("/parse_status", response_model=ParseStatusResponse)
def get_parse_status(task_id: str = Query(...)):
    task_result = AsyncResult(task_id)
    response = ParseStatusResponse(
        status=task_result.status,
        progress=100 if task_result.status == "SUCCESS" else 0,
        result=task_result.result if task_result.status == "SUCCESS" else '-'
    )
    return response