import logging

import jsonpath


class GetKeywords:
    @staticmethod
    def get_keyword(data, name, index=0):

        try:
            result = jsonpath.jsonpath(data, f"$..{name}")[index]
        except Exception as e:
            result = False
        if result is False:
            logging.error(f"jsonpath提取失败，原本提取的元数据是{data}，提取的值是{name}")
        else:
            return result

    @staticmethod
    def get_keywords(data, name):

        try:
            result = jsonpath.jsonpath(data, f"$..{name}")
        except Exception as e:
            result = False
        if result is False:
            logging.error(f"jsonpath提取失败，原本提取的元数据是{data}，提取的值是{name}")
        else:
            return result
