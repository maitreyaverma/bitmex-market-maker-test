import pandas as pd
import sys
import uuid
import os
from market_maker.utils.log import  logger
system=sys.platform
path=""
if "win" in system:
    path="M:/coding/bitmex/market_maker/backtest/data/"
else:
    path="/mnt/m/coding/bitmex/market_maker/backtest/data/"
class DummyBitmex:
    def exit(self):
        return
class DummyExchangeInterface:
    def cancel_all_orders(self):
        return
    def __init__(self,fileName):
        self.symbol="XBTUSD"
        self.tickSize=0.5
        self.position=0
        self.history=self.read_csv(fileName)
        self.update_ticker_and_time()
        self.buy_orders=[]
        self.sell_orders=[]
        self.marginCashBalance= 1000000
        self.multiplicationFactor=10000
        self.marginBalance=self.marginCashBalance

    # {'price': 6747.5, 'orderQty': 40, 'side': 'Buy'}
    def get_position(self):
        return {'currentQty': self.position, 'avgCostPrice': 100, 'avgEntryPrice': 100}
    def get_orders(self):
        orders=[]
        [orders.append(order) for order in self.buy_orders]
        [orders.append(order) for order in self.sell_orders]
        return orders
    def create_bulk_orders(self,orders):
        for order in orders:
            order['orderID'] = uuid.uuid1()
            order['leavesQty'] = 0
            order['cumQty'] = 0
            if order['side']=='Buy':
                self.buy_orders.append(order)
            else:
                self.sell_orders.append(order)
        return
    def cancel_bulk_orders(self,orders):
        buy_cancel_orders=list(filter(lambda  x:x['side']=='Buy',orders))
        sell_cancel_orders=list(filter(lambda  x:x['side']!='Buy',orders))
        [self.buy_orders.remove(x) for x in buy_cancel_orders]
        [self.sell_orders.remove(x) for x in sell_cancel_orders]
        return
    def amend_bulk_orders(self,orders):
        for order in orders:
            if order['side']=='Buy':
                [x.update(order) for x in self.buy_orders if x['orderID']==order['orderID']]
            else:
                [x.update(order) for x in self.sell_orders if x['orderID']==order['orderID']]
        return

    def read_csv(self,fileName):
        full_path=path+fileName
        df=pd.read_csv(full_path)
        df=df[df['symbol']=="XBTUSD"]
        df=df.sort_values('timestamp')
        df['timestamp']=pd.to_datetime(df['timestamp'],format="%Y-%m-%dD%H:%M:%S.%f")
        self.index=0
        self.maxIndex=df.shape[0]
        self.market_open=True
        print("loaded data")
        return df
    def sleep(self,n):
        index=self.index
        time=self.current_time
        while(self.history.iloc[index]['timestamp']-time).total_seconds()<n:
            index=index+1
            self.fill_orders(self.history.iloc[index])
            self.recalculate_margin(self.history.iloc[index]['bidPrice'])
            if index>self.maxIndex-5:
                self.market_open=False
                print("initially margin was " +str(self.marginCashBalance) + ", position was "+str(self.position))
                self.recalculate_margin(self.history.iloc[index]['bidPrice'])
                print("net value is "+str(self.marginBalance))
                return
            if self.marginBalance<=990000:
                self.market_open = False
                print("drawdown to 0")
                print("net value is 0")
                return
        self.index=index
        self.update_ticker_and_time()
    def recalculate_margin(self,price):
        self.marginBalance=self.marginCashBalance-(self.position*self.multiplicationFactor)/price
    def fill_position(self,qty,price,order):
        if self.position==0:
            self.entryPrice=price
            self.entryTime=self.current_time
        else:
            print(str(self.entryTime)+","+str(qty*((1/self.entryPrice)-(1/price))))
        logger.info("Initially margin was: %d, Position was: %d" % (self.marginCashBalance, self.position))
        self.position = qty + self.position
        self.marginCashBalance += (qty *self.multiplicationFactor)/price
        logger.info("Quantity was: %d, Price was: %d" % (qty, price))
        logger.info("Finally margin was: %d, Position was: %d" % (self.marginCashBalance, self.position))
        order['orderQty'] = order['orderQty'] - abs(qty)
    def fill_orders(self, row):
        price_ = row['bidPrice']
        ask_price_ = row['askPrice']
        for i in range(len(self.buy_orders)):
            if self.buy_orders[i]['price']>= price_ and self.buy_orders[i]['orderQty']>0:
                qty=self.buy_orders[i]['orderQty']
                self.fill_position(qty,price_,self.buy_orders[i])
        for i in range(len(self.sell_orders)) :
            if self.sell_orders[i]['price']<= ask_price_ and self.sell_orders[i]['orderQty']>0:
                qty=-1*self.sell_orders[i]['orderQty']
                self.fill_position(qty, ask_price_, self.sell_orders[i])
        [self.buy_orders.remove(order) for order in self.buy_orders if order['orderQty']<=0 ]
        [self.sell_orders.remove(order) for order in self.sell_orders if order['orderQty'] <= 0 ]

    def update_ticker_and_time(self):
        self.ticker, self.current_time = self.get_ticker_and_time(self.history.iloc[self.index])
        self.current_time=self.current_time.replace(microsecond=0)
    def get_ticker_and_time(self,row):
        buy=row['bidPrice']
        sell=row['askPrice']
        mid=(buy+sell)/2
        return ({"buy":buy,"sell":sell,"mid":mid},row['timestamp'])
    def get_current_time(self):
        return self.current_time
    def get_ticker(self):
        return self.ticker
    def check_market_open(self):
        return self.market_open
    def is_open(self):
        return True
    def get_margin(self):
        return {'marginBalance':self.marginCashBalance}
    def get_delta(self):
        return self.get_position()['currentQty']
    def calc_delta(self):
        return {'spot': self.get_delta()}
    def get_highest_buy(self):
        return {'price':self.get_ticker()["buy"]}
    def get_lowest_sell(self):
        return {'price':self.get_ticker()["sell"]}
    def get_instrument(self):
        return {'tickLog':1,'tickSize':0.5,'symbol':'XBTUSD'}

    def check_if_orderbook_empty(self):
        return False
