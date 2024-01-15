from enum import Enum
import os


class MergeCfg(Enum):
    MERGE_API_KEY = 0
    MERGE_ACCOUNT_TOKEN = 1


def get_configuration_value(cfg: MergeCfg) -> str:
    k = cfg.name
    match os.getenv(k):
        case None:
            raise Exception(f"{k} environment variable not found")
        case val:
            return val


def save_token(token: str) -> None:
    with open("token", "w") as f:
        f.write(token)
