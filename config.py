import os
from dotenv import load_dotenv

from typing import List

load_dotenv()


# Implementation of Config values
class Config:
    token: str = os.getenv("TOKEN")
    prefix: str = os.getenv("PREFIX", "#sudo ")
    report_channel_id: int = int(
        os.getenv("REPORT_CHANNEL_ID", 1076994131286560838)
    )
    mod_role_id: List[int] = [
        int(x) for x in os.getenv("MOD_ROLE_ID", "0").split(",")
    ]
    temp_channel: int = int(os.getenv("TEMP_CHANNEL", "0"))
    role_channel: int = int(os.getenv("ROLE_CHANNEL", "0"))
    log_channel: int = int(os.getenv("LOGS_CHANNEL", "0"))
    error_channel: int = int(os.getenv("ERROR_CHANNEL", "0"))


if __name__ == "__main__":
    print("Loaded Config from main folder.")
