import datetime
import logging
import os
from datetime import timedelta
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from config import DATA_DIR, LOGS_DIR
from src.utils import days_translation

# def test_spending_by_weekday() -> None:
#     assert start_of_period == datetime.datetime.strptime('01-01-2021 00:00:00', "%d-%m-%Y %H:%M:%S")
