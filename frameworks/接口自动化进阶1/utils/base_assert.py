import ast
import logging

from utils.get_keywords import GetKeywords
import pytest


class BaseAssert:

    @staticmethod
    def status_code_assert(result, status_code):
        res = GetKeywords().get_keyword(result, "status_code")
        return res == status_code

    @staticmethod
    def code_assert(result, code):
        res = GetKeywords().get_keyword(result, "code")
        return res == code

    @staticmethod
    def str_assert(check_name, result):
        return check_name in str(result)

    @staticmethod
    def type_assert(check_name, expected_type):
        return isinstance(check_name, expected_type)

    @staticmethod
    def time_assert(response_time, expected_time):
        return response_time <= expected_time


class MainAssert(BaseAssert):
    def __init__(self, case, result):
        # self.__base = BaseAssert()
        self.__case = case
        self.__result = result

    def main_assert(self):
        for key, value in eval(self.__case["check"]).items():
            if key == "status_code":
                logging.info(f"3、HTTP多重响应断言内容（status_code）：预期结果{value}--实际结果{self.__result}")
                pytest.assume(self.status_code_assert(self.__result, value))
            if key == "code":
                logging.info(f"3、HTTP多重响应断言内容（code）：预期结果{value}--实际结果{self.__result}")
                pytest.assume(self.code_assert(self.__result, value))
            if key == "str":
                for v in value:
                    logging.info(f"3、HTTP多重响应断言内容（str）：预期结果{v}--实际结果{self.__result}")
                    pytest.assume(self.str_assert(v, self.__result))
            if key == "type":
                for v in value:
                    check_name = v.get("check_name")
                    expected_type = v.get("expected_type")
                    index = v.get("index")
                    if index == "all":
                        res_list = GetKeywords.get_keywords(self.__result, check_name)
                        for res in res_list:
                            logging.info(f"3、HTTP多重响应断言内容（type）：预期结果{expected_type}--实际结果{res}")
                            pytest.assume(self.type_assert(res, expected_type))
                    if isinstance(index, int):
                        res = GetKeywords.get_keyword(self.__result, check_name, index)
                        logging.info(f"3、HTTP多重响应断言内容（type）：预期结果{expected_type}--实际结果{res}")
                        pytest.assume(self.type_assert(res, expected_type))
            if key == "time":
                response_time = GetKeywords.get_keyword(self.__result, "response_time")
                logging.info(f"3、HTTP多重响应断言内容（time）：预期结果{value}--实际结果{response_time}")
                pytest.assume(self.time_assert(response_time, value))

