import json
import logging
import os
from functools import wraps

import pandas as pd

from config import DATA_DIR, LOGS_DIR, RESULT_DIR
from src.decorator import create_series, to_json_file


def test_to_json_file() -> None:
    pass
