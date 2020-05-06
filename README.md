# Backtesting bitmex market maker
[Bitmex Market Maker](https://github.com/BitMEX/sample-market-maker) gives the code to apply market making strategy on bitmex.
The core of it lies in market_maker.backtest.dummy_exchange_interface which I have created.
Have added the provision to backtest it. Just have to replace actual exchange with 
```python
from market_maker.backtest.dummy_exchange_interface import DummyExchangeInterface
```
Combined.sh fetches data from [bitmex historical data](https://public.bitmex.com/) if data has not been previously downloaded and runs the backtest for each day.
The result for each day is stored in results/ folder.

processData.sh can be used to combined those results into a csv file result.csv. 
This is a very crude approach but with minimal amount of efforts am able to test the system. The best part is, just have to change the exchange from dummy to live and it can go to live.
##Results
The results were as they were expected to be. This does not turn out to be profitable. I personally am not very sure about market making. On forums, it was written that it is profitable but lacks in risk management. Just wanted to check if it is indeed profitable.