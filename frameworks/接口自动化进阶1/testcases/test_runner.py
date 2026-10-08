import ast
import logging
import pytest
from jinja2 import Template
from utils.allure_utils import allure_init
from utils.asserts import *
from utils.case_analyse import case_analyse
from utils.excel_utils import read_excel
from utils.extractor import json_extractor, jdbc_extractor
from utils.send_request import send_http_request, send_jdbc_request
from utils.data_preprocessor import *
from utils.get_keywords import *


class TestRunner:

    data = read_excel()     #读取excel中的数据存入data

    all = {}                #定义全局变量all空字典存储提取后的全局变量

    @pytest.mark.parametrize("case", data)   #使用parametrize参数化装饰器来一段一段提取测试用例进行测试
    def test_case(self, case):

        all = self.all          #建立全局变量与局部变量的关系，引用全局变量all来将提取的数据用于后续渲染case

        case = eval(Template(str(case)).render(all))     #利用all的值来渲染case，将render中的all值塞进template中字符串内占位符里
                                                            #便于引用token、user_id等动态值
        #allure初始化
        allure_init(case)
        logging.info(f"0.用例ID：{case['id']} 模块：{case['feature']} 场景：{case['story']} 标题：{case['title']}")
        # 解析数据
        request_data = case_analyse(case)
        res = send_http_request(request_data)      #进行请求
        # print(res.json())                         #以字典形式获取返回json
        #设置断言--HTTP断言
        http_assert(case, res)
        # try:
        #    eval(case["check"])
        # except:
        #     http_assert(case, res)
        # else:
        #     http_asserts(case, res)
        #设置数据库断言
        jdbc_assert(case)
        #提取
        #JSON提取
        json_extractor(case, all, res)
        #数据库提取
        jdbc_extractor(case, all)
