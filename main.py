from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pymysql
import logging
app = FastAPI()

# 1. logger 생성
logger = logging.getLogger("main")
# 2. logger 레벨 설정
logger.setLevel(logging.DEBUG)
# 3. formatting 설정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 4. handler 설정
# console 출력
stream_hander = logging.StreamHandler()
stream_hander.setFormatter(formatter)
logger.addHandler(stream_hander)
# 파일 출력
file_handler = logging.FileHandler('info.log', mode='w')
logger.addHandler(file_handler)

def log_info(req_body, res_body):
    logging.info(req_body)
    logging.info(res_body)

async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {'type': 'http.request', 'body': body}
    request._receive = receive
    
@app.middleware('http')
async def some_middleware(request: Request, call_next):
    req_body = await request.body()
    await set_body(request, req_body)
    response = await call_next(request)
    
    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk
    
    task = BackgroundTask(log_info, req_body, res_body)
    return Response(content=res_body, status_code=response.status_code, 
        headers=dict(response.headers), media_type=response.media_type, background=task)

#cors 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost","http://64.176.42.251"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 연결
# db = pymysql.connect(
#     host='ec2-3-35-214-62.ap-northeast-2.compute.amazonaws.com', 
#     user='root', 
#     password='acorns4032', 
#     db='gameapi', 
#     charset='utf8', 
#     port=3306
#     )

db = pymysql.connect(
    host='musclecat-rds.cg4uejktsucz.ap-southeast-2.rds.amazonaws.com', 
    user='admin', 
    password='ghks1015!^', 
    db='db_test', 
    charset='utf8', 
    port=3306
    )

class User(BaseModel):
    memId: Optional[str] = None
    siteId: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "github Action"}

@app.get("/test")
async def test():
    return "test github action"

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
    sql = "select * from tb_test"
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