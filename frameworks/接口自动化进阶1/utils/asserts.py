import ast
from abc import ABC, abstractmethod

import pytest
import logging

import allure
import jsonpath

from utils.base_assert import MainAssert
from utils.get_keywords import GetKeywords
from utils.send_request import send_jdbc_request


class DataAssert(ABC):
    @abstractmethod
    def http_assert(self, case, res):
        pass


class SingleAssert(DataAssert):
    @allure.step("3.HTTP响应断言")
    def http_assert(self, case, res):
        if case["check"]:
            result = GetKeywords.get_keyword(res, case["check"])
            logging.info(f"3.获取HTTP响应断言：实际结果({result}) , 预期结果({case['expected']})")
            assert result == case["expected"]
        else:
            logging.info(f"3.获取HTTP响应断言：预期结果({case['expected']}) 是否in 响应文本({res.text})")
            assert case["expected"] in str(res)


class MultipleAssert(DataAssert):
    @allure.step("3.HTTP多重响应断言")
    def http_assert(self, case, res):
        if case["check"]:
            MainAssert(case, res).main_assert()
        #     for key, value in ast.literal_eval(case["check"]).items():
        #         result = GetKeywords.get_keyword(res, key)
        #         logging.info(f"3.获取HTTP响应断言：实际结果({result}) , 预期结果({value})")
        #         pytest.assume(result == value)
        # else:
        #     logging.info(f"3.获取HTTP响应断言：预期结果({case['expected']}) 是否in 响应文本({str(res)})")
        #     assert case["expected"] in str(res)


def obj_processor(case):
    try:
        eval(case["check"])
    except:
        return SingleAssert()
    else:
        return MultipleAssert()


def http_assert(case, res):
    obj_processor(case).http_assert(case, res)


class DatabaseAssert(ABC):
    @abstractmethod
    def jdbc_assert(self, case):
        pass


class SingleDatabaseAssert(DatabaseAssert):
    def jdbc_assert(self, case):
        if case["sql_check"] and case["sql_expected"]:
            with allure.step("3.JDBC响应断言"):
                result = send_jdbc_request(case["sql_check"])
                logging.info(f"3.获取JDBC响应断言：实际结果({result}) , 预期结果({case['sql_expected']})")
                assert case["sql_expected"] in str(result)


class MultipleDatabaseAssert(DatabaseAssert):
    def jdbc_assert(self, case):
        if case["sql_check"] and case["sql_expected"]:
            with allure.step("3.JDBC多重响应断言"):
                sql_check = eval(case["sql_check"])
                sql_expected = eval(case["sql_expected"])
                for sql, expected in zip(sql_check, sql_expected):
                    result = send_jdbc_request(sql)
                    logging.info(f"3.获取JDBC多重响应断言：实际结果({result}) , 预期结果({expected})")
                    pytest.assume(expected in str(result))


def sql_processor(case):
    try:
        eval(case["sql_check"]) and eval(case["sql_expected"])
    except:
        return SingleDatabaseAssert()
    else:
        return MultipleDatabaseAssert()


def jdbc_assert(case):
    sql_processor(case).jdbc_assert(case)
