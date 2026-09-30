class DomainError(Exception):
    def __init__(self, message: str, status: int = 400, code: str = "domain"):
        self.message, self.status, self.code = message, status, code
class Unauthorized(DomainError):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401, "unauthorized")
class NotFound(DomainError):
    def __init__(self, message: str = "Not found"):
        super().__init__(message, 404, "not_found")
class Conflict(DomainError):
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, 409, "conflict")
