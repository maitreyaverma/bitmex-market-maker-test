from dummy_exchange_interface import DummyExchangeInterface
exchange=DummyExchangeInterface()
print(exchange.symbol)
print(exchange.get_highest_buy())
import sys
print(sys.platform)