"""其他工具"""

import datetime
import string
import random
import socket

from app.core.logger import get_logger
from app.core.config import (
    LOGGER_LEVEL,
    LOGGER_COLOR,
)

logger = get_logger(
    level=LOGGER_LEVEL,
    color=LOGGER_COLOR,
)


def generate_datetime_string() -> str:
    """生成日期字符串
    """
    return datetime.datetime.now().strftime(r"%Y%m%d_%H%M%S")


def generate_random_string(
    length: int | None = 8,
    chars: str | None = None,
    include_uppercase: bool | None = True,
    include_lowercase: bool | None = True,
    include_digits: bool | None = True,
    include_special: bool | None = False,
) -> str:
    """
    生成随机字符串
    """
    if chars is not None:
        char_pool = chars
    else:
        char_pool = ""
        if include_uppercase:
            char_pool += string.ascii_uppercase
        if include_lowercase:
            char_pool += string.ascii_lowercase
        if include_digits:
            char_pool += string.digits
        if include_special:
            char_pool += "!@#$%^&*"

    if not char_pool:
        raise ValueError("字符池不能为空")

    return "".join(random.choice(char_pool) for _ in range(length))


def generate_filename(
    include_date: bool | None = True,
    random_str_len: int | None = 0,
) -> str:
    """生成文件名
    """
    if random_str_len > 0:
        random_str = generate_random_string(random_str_len)
        if include_date:
            return generate_datetime_string() + f"_{random_str}"
        return random_str
    
    return generate_datetime_string()


def find_port(port: int) -> int:
    """寻找未被占用的服务器端口
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        if s.connect_ex(("localhost", port)) == 0:
            logger.debug("%s 端口已占用, 寻找新端口", port)
            return find_port(port=port + 1)
        else:
            logger.debug("%s 端口可用", port)
            return port
