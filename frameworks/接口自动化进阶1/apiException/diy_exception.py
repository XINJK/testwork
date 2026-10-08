

class DatabaseException(Exception):
    def __init__(self, message="数据库连接异常", code=-1):
        self.message = message
        self.code = code
        #super表示调用父类的方法，下面是进行父类的初始化
        super().__init__(message, code)


class GetDataException(Exception):
    def __init__(self, message="数据库查询异常", code=-1):
        self.message = message
        self.code = code
        super().__init__(message, code)


class ExecuteSqlException(Exception):
    def __init__(self, message="数据库修改/删除异常", code=-1):
        self.message = message
        self.code = code
        super().__init__(message, code)
