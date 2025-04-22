# examples\di\data_visualization_api.py
from fastapi import FastAPI
from pydantic import BaseModel
from metagpt.roles.di.data_interpreter import DataInterpreter

app = FastAPI()

class Requirement(BaseModel):
    text: str

@app.post("/data-visualization")
async def data_visualization(requirement: Requirement):
    di = DataInterpreter()
    result = await di.run(requirement.text)
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)