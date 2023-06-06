from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    return "test"

@app.get("/test2")
async def test2():
    return "test2"

@app.get("/test3")
async def test3():
    return "test3"