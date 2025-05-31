from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    prompt: str

class QueryResponse(BaseModel):
    response: str

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    # Здесь будет логика обращения к агенту
    # Например: response = manager_agent.invoke(request.prompt)
    response = "Заглушка ответа"
    return QueryResponse(response=response)

@app.get("/")
async def root():
    return {"message": "API сервер запущен"}