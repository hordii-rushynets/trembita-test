import logging
import sys
import time
from datetime import datetime

from apps.static_report.services import TsNAPStaticReportService
from apps.static_report.utils import get_current_quarter, get_current_year
from database import *
from settings import *

if __name__ == '__main__':
    logging.basicConfig(filename='./trembita.log',
                        filemode='a',
                        level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    start_time = time.time()
    start_timestamp = datetime.now()
    logging.info(f"Task started at {start_timestamp.strftime('%Y-%m-%d %H:%M:%S')} \n")

    db.Base.metadata.create_all(db.engine)

    year = get_current_year()
    quarter = get_current_quarter()

    TsNAPStaticReportService().create_or_update(year, quarter)

    end_time = time.time()
    end_timestamp = datetime.now()
    total_duration = end_time - start_time

    logging.info(f"Task ended at {end_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
    logging.info(f"Total execution time: {total_duration:.2f} seconds\n")
