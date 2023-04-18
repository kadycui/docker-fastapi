#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    :   2023/02/21 09:35:17
@Auth    :   KadyCui 
@File    :   logger.py
@Desc    :   None
"""
import os
from pathlib import Path
import datetime
from loguru import logger


class Logs:
    __instance = None
    # 文件名称，按天创建
    DATE = datetime.datetime.now().strftime('%Y-%m-%d')

    # 项目路径下创建log目录保存日志文件
    logpath = Path(__file__).parents[1].resolve() / 'logs'  # 拼接指定路径
    # 判断目录是否存在，不存在则创建新的目录
    if not os.path.isdir(logpath):
        os.makedirs(logpath)

    

    logger.add(
        sink='%s/%s.log' % (logpath, DATE),   # 指定文件
        format="{time:YYYY-MM-DD HH:mm:ss}  | {level}> {elapsed}  | {message}",  # 日志格式
        encoding='utf-8',
        level="DEBUG",
        rotation='00:00',  # 每天 0 点创建一个新日志文件
        retention="7 days",  # 定时自动清理文件
        backtrace=True,  # 回溯
        diagnose=True,   # 诊断
        enqueue=True,   # 异步写入
        # rotation="5kb",  # 切割，设置文件大小，rotation="12:00"，rotation="1 week"
        # filter="my_module"  # 过滤模块
        # compression="zip"   # 文件压缩
    )

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Logs, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def info(self, msg, *args, **kwargs):
        return logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        return logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        return logger.exception(msg, *args, exc_info=True, **kwargs)
