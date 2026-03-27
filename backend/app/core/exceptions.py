class AppException(Exception):
    """项目统一业务异常基类。"""

    def __init__(self, status_code: int, code: str, message: str) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)


class AuthError(AppException):
    """认证失败相关异常，例如 token 无效或密码错误。"""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(status_code=401, code=code, message=message)


class ConflictError(AppException):
    """资源冲突异常，例如用户名重复。"""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(status_code=409, code=code, message=message)
