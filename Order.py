from enum import Enum

class OrderBy(Enum):
    by_id = 'id'
    by_name = 'name'
    by_price = 'price'
    by_amount = 'amount'