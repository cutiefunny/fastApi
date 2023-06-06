from fastapi import FastAPI
import pymysql
app = FastAPI()

# DB 연결
db = pymysql.connect(
    host='ec2-52-78-81-178.ap-northeast-2.compute.amazonaws.com', 
    user='root', 
    password='acorns4032', 
    db='gameapi', 
    charset='utf8', 
    port=3306
    )

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

@app.get("/test4")
async def test4():
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select * from mem_cash"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    db.close()
    return result

# 재기동 방법
# git pull origin master
# 1.pkill -9 gunicorn
# 2.cd fastapi
# 3.gunicorn -k uvicorn.workers.UvicornWorker --access-logfile ./gunicorn-access.log main:app --bind
# (gunicorn -k uvicorn.workers.UvicornWorker --access-logfile ./gunicorn-access.log main:app --bind 0.0.0.0:8000 --workers 2 --daemon)