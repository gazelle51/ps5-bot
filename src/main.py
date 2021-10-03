from datetime import datetime
from dotenv import load_dotenv
import argparse
import logging
import logging.config

from bigw.ps5 import find_and_buy_ps5

# Load environment variables
load_dotenv()

# Load logger
logging.config.fileConfig('./src/logger.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# Load arguments
parser = argparse.ArgumentParser(description='Check for a PS5 in stock at Big W and buy it if it\'s in stock.')
parser.add_argument('--test', dest='test_mode', action='store_const', const=True, default=False,
                    help='run in test mode to test Selenium set up (default: do not run in test mode)')
args = parser.parse_args()

# If script asked to run in test mode, execute find_and_buy_ps5 in test mode
# Used to test Selenium set up
if args.test_mode:
    find_and_buy_ps5(args.test_mode)
    exit()
