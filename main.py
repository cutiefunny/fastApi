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

# 재기동 방법
# git pull origin master
# 1.pkill -9 gunicorn
# 2.cd fastapi
# 3.gunicorn -k uvicorn.workers.UvicornWorker --access-logfile ./gunicorn-access.log main:app --bind
# (gunicorn -k uvicorn.workers.UvicornWorker --access-logfile ./gunicorn-access.log main:app --bind 0.0.0.0:8000 --workers 2 --daemon)