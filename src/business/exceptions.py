class BusinessError(RuntimeError):
    """Generic error raised by Business Layer."""

    def __init__(self, detail: str, code: int = 400) -> None:
        self.detail = detail
        self.code = code
        super().__init__(detail)
