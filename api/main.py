import os
import datetime
import uvicorn
import redis
from fastapi import FastAPI, Body
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from utils.logger import Logs


log = Logs()

app = FastAPI(title='fast-api')

scheduler = None



def job(job_id=None):
    if job_id:
        log.info(f"执行了--{job_id}")
    else:
        log.info("没有定时任务执行!")


@app.on_event('startup')
def init_scheduler():
    """初始化"""
    
    log.info("初始化")

    executor = ThreadPoolExecutor()

    # host = os.environ.get("REDIS_HOST", "redis")
    # port = int(os.environ.get("REDIS_PORT", "6389"))


    # redis_client = redis.Redis(host=host, port=port)
    # log.info("78989878789798789789")
    # log.info(redis_client)
    # redis_client.set('username', 'admin')
    # redis_client.hset('student', 'name', 'luohao')

    # log.info(redis_client.keys('*'))
    # log.info(redis_client.get('username'))


    jobstores = {
        'default' : RedisJobStore(db=0, jobs_key='myfunc', run_times_key='myfunc_time', host="redis_db", port=6379)
    }
    executors = {
        'default': executor,
    }
    job_defaults = {
        'coalesce': True,
        'max_instance': 1
    }

    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    # scheduler.add_job(job, 'interval', seconds=20)
    print("启动调度器...")
    scheduler.start()


@app.post('/add-job')
async def add_job(job_id: str = Body(...)):
    """添加job"""
    log.info(f"添加-{job_id}")
    scheduler.add_job(id=job_id, func=job, args=(job_id,), trigger='interval', seconds=20)
    return {"msg": "success!"}


@app.post('/remove-job')
async def remove_job(job_id: str = Body(..., embed=True)):
    """移除job"""
    log.info(f"移除-{job_id}")
    scheduler.remove_job(job_id)
    return {"msg": "success!"}


@app.post('/pause-job')
async def pause_job(job_id: str = Body(..., embed=True)):
    """暂停job"""
    log.info(f"暂停-{job_id}")
    scheduler.pause_job(job_id)
    return {"msg":"success!"}


@app.post('/resume-job')
async def resume_job(job_id: str = Body(..., embed=True)):
    """恢复job"""
    log.info(f"恢复-{job_id}")
    scheduler.resume_job(job_id)
    return {"msg":"success!"}


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=5006)
