from dotenv import load_dotenv
import argparse
import logging
import logging.config
import os
import time

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

# Wait time in minutes
WAIT_TIME_MINS = int(os.environ.get('WAIT_TIME_MINS'))

# If script asked to run in test mode, execute find_and_buy_ps5 in test mode
# Used to test Selenium set up
if args.test_mode:
    find_and_buy_ps5(args.test_mode)
    exit()

logger.info('Starting PS5 buying bot')

# Start looking for PS5
success_flag = False
while not success_flag:
    logger.info('Trying to buy a PS5')

    # Try to buy a PS5
    ps5_bought = find_and_buy_ps5(args.test_mode)

    # If bought, then stop
    if ps5_bought:
        logger.info('*** PS5 successfully bought ***')
        success_flag = True
    else:
        logger.info('PS5 buy unsuccessful')

    # Wait to try again
    time.sleep(WAIT_TIME_MINS*60)

logger.info('PS5 buying bot complete')
