from dataclasses import dataclass


@dataclass
class Config:
    app_password: str
    sender: str
    recipients: str


config = Config(
    app_password="",
    sender="",
    recipients="",
)
