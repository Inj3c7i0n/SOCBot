import os
import json
from typing import Callable, TypeVar

from discord.ext.commands import Context

from exceptions import *

T = TypeVar("T")


def is_owner() -> Callable[[T], T]:
    async def predictable(ctx: Context) -> bool:
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/../config.json") as file:
            data = json.load(file)
        if ctx.author.id not in data["owners"]:
            raise UserNotOwner
        return True

    return commands.check(predictable)
    