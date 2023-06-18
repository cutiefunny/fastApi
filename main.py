from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pymysql
app = FastAPI()

#cors 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost","http://64.176.42.251"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 연결
db = pymysql.connect(
    host='ec2-52-78-81-178.ap-northeast-2.compute.amazonaws.com', 
    user='root', 
    password='acorns4032', 
    db='gameapi', 
    charset='utf8', 
    port=3306
    )

class User(BaseModel):
    memId: Optional[str] = None
    siteId: Optional[str] = None

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

@app.post("/member")
async def member(user: User):
    args = []
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select * from member where 1=1"
    if user.memId != None:
        sql += """ and memId like CONCAT('%%', %s, '%%')"""
        args.append(user.memId)
    if user.siteId != None:
        sql += """ and siteId like CONCAT('%%', %s, '%%')"""
        args.append(user.siteId)
    cursor.execute(sql, (args))
    result = cursor.fetchall()
    cursor.close()
    return result

@app.post("/getBalance")
async def userYn(user: User):
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select cashAmt from mem_cash where memId = %s and siteId = %s"
    cursor.execute(sql, (user.memId, user.siteId))
    temp_result = cursor.fetchall()
    result = temp_result[0]['cashAmt']
    cursor.close()
    return result

@app.get("/members")
async def member():
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select * from member"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

# 재기동 방법
# git pull origin master
# 1.pkill -9 gunicorn
# 2.cd fastapi
# 3.gunicorn -k uvicorn.workers.UvicornWorker --access-logfile ./gunicorn-access.log main:app --bind
# (gunicorn -k uvicorn.workers.UvicornWorker --access-logfile ./gunicorn-access.log main:app --bind 0.0.0.0:8000 --workers 2 --daemon)