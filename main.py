from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def root():
    return "test"

@app.get("/test2")
async def root():
    return "test2"