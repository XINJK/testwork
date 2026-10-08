import logging

import allure
import pymysql
import requests

from config.config import *
from utils.database import *


@allure.step("2.发送HTTP请求")
def send_http_request(request_data):
    res = requests.request(**request_data)
    response = {
        "status_code": res.status_code,
        "json_data": res.json(),
        "response_time": res.elapsed.total_seconds() * 1000
    }
    logging.info(f"2.发送HTTP请求，响应文本为：{response}")
    return response


def send_jdbc_request(sql):
    return Database().get_one(sql)
    # conn = pymysql.Connect(
    #     host=DB_HOST,
    #     port=DB_PORT,
    #     database=DB_NAME,
    #     user=DB_USER,
    #     password=DB_PASSWORD,
    #     charset="utf8"
    #     # autocommit=True  # 自动提交，遇到需要回滚的时候记得关闭
    # )
    # cur = conn.cursor()
    # cur.execute(sql)
    # result = cur.fetchone()  # 获取一行结果，如果需要获取全部就用fetchall()
    # cur.close()
    # conn.close()
    # return result[index]
