from enum import Enum


class OrderStatus(str, Enum):
    ACTIVE = "Active"
    FILLED = "Filled"
    REJECTED = "Rejected"
    CANCELLED = "Cancelled"

class OrderSide(str, Enum):
    BUY = "Buy"
    SELL = "Sell"