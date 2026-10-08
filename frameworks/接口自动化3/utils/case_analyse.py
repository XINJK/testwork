import logging

import allure

from config.config import *


@allure.step("1.解析请求数据")
def case_analyse(case):
    method = case["method"]
    url = BASE_URL + case["path"]
    params = eval(case["params"]) if isinstance(case["params"], str) else None
    data = eval(case["data"]) if isinstance(case["data"], str) else None
    json = eval(case["json"]) if isinstance(case["json"], str) else None
    headers = eval(case["headers"]) if isinstance(case["headers"], str) else None
    files = eval(case["files"]) if isinstance(case["files"], str) else None

    # 存进请求数据data中
    request_data = {
        "method": method,
        "url": url,
        "params": params,
        "data": data,
        "json": json,
        "headers": headers,
        "files": files
    }
    logging.info(f"1.解析请求数据，请求数据为：{request_data}")
    allure.attach(f"{request_data}", name="解析数据结果")
    return request_data
