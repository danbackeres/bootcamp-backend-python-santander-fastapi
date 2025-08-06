from fastapi import FastAPI

app = FastAPI(title="Workout API")

if __name__ == 'main':
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8000, log_level="info", reload=True)

@app.get("/")
async def root():
    return {"message": "Hello World"}

