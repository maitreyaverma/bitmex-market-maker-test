from __future__ import absolute_import
import sys
from market_maker.utils import log, constants, errors, math

# Used for reloading the bot - saves modified times of key files
import os
watched_files_mtimes = []
import logging
from market_maker.utils.log import  logger
#
# Helpers
#
from market_maker.market_maker import OrderManager
from market_maker.backtest.dummy_exchange_interface import DummyExchangeInterface

fileName=sys.argv[2]
def run():
    logger.info('BitMEX Market Maker Version: %s\n' % constants.VERSION)
    exchange=DummyExchangeInterface(fileName)
    om = OrderManager(exchange,[])
    try:
        om.run_loop()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
# exchange=DummyExchangeInterface()
# print(exchange.get_ticker())
# exchange.sleep(1)
# print(exchange.get_ticker())
# for i in range(10):
#     exchange.sleep(3)
run()