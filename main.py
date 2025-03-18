from fastapi import FastAPI
import uvicorn
from controllers.slack_integration import router as slack_router

app = FastAPI()

app.include_router(slack_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
