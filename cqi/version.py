from typing import Tuple


version: str = '0.1.5'
version_info: Tuple[int, int, int] = tuple([int(d) for d in version.split("-")[0].split(".")])
