import logging
from market_maker.settings import settings


def setup_custom_logger(name, log_level=settings.LOG_LEVEL):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    logging.basicConfig(filename="newfile.log", level=logging.INFO, format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger
def get_logger():
    logging.basicConfig(filename="newfile.log", level=logging.INFO, format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    # logger = setup_custom_logger('root')
    logger = logging.getLogger()
    return logger

# logger=setup_custom_logger('root')
logger=get_logger()