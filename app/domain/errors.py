class DomainError(Exception):
    """Base class for domain-level errors."""


class InvalidStatusError(DomainError):
    def __init__(self, username: str, status: str) -> None:
        super().__init__(
            f"{username} status is {status}: bot will not respond for that message"
        )
        self.username = username
        self.status = status
