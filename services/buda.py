from requests import get
from typing import List

BASE_URL = 'https://www.buda.com/api/v2'

class BudaEntry:
    def __init__(self, timestamp, amount, price, direction):
        self.timestamp = int(timestamp)
        self.amount = float(amount)
        self.price = float(price)
        self.str_amount = amount
        self.str_price = price
        self.direction = direction
        self.clp_amount = self.amount * self.price
        pass

    def __str__(self) -> str:
        return f'timestamp: {self.timestamp} btc amount: {self.amount}  price: {self.price} direction: {self.direction} '

class BudaApiServices:
    def __init__(self ):
        pass

    def get_markets(self):
        url = f'{BASE_URL}/markets'
        response = get(url)
        return response.json()['markets']


    def get_day_transactions(self, timestamp: int, market_id = 'btc-clp'):
        url = f'{BASE_URL}/markets/{market_id}/trades'
        response = get(url, params={
        'timestamp': timestamp, 
        })
        return response.json()
    
    
    def find_market(self, market_id: str):
        markets = self.get_markets()
        return list(filter(lambda market: market['id'] == market_id, markets))[0]
    
class BudaServices:

    def get_range_transactions(self, start: int, end: int, entries = []) -> any:
        buda_api = BudaApiServices()
        trades = buda_api.get_day_transactions(start)['trades']
        current_entries = trades['entries']
        total_entries = []
        if(int(trades['last_timestamp']) > end):
            total_entries = entries + self.get_range_transactions(trades['last_timestamp'], end, current_entries) 
        else:
            filtered_entries = list(filter(lambda entry: int(entry[0]) >= end, current_entries))
            total_entries = entries + filtered_entries
        return total_entries
    
    def from_entry_to_buda_entry(self, entry: list) -> BudaEntry:
        return BudaEntry(entry[0], entry[1], entry[2], entry[3])
    
    def calc_traded_money(self, entries: List[BudaEntry]) -> float:
        total = 0.0
        for entry in entries:
            total += entry.clp_amount
        return total
    
    def get_btc_transaction_volumen(self, entries: List[BudaEntry]) -> float:
        total = 0.0
        for entry in entries:
            total += entry.amount
        return total
    
    def calc_percentage_augment(self, current_date_transaction, last_year_transaction) -> float:
        return (current_date_transaction - last_year_transaction) / last_year_transaction * 100
    
    def calc_total_lost_comission(self, traded_money, percentage) -> float:
        return (percentage / 100) * traded_money
    