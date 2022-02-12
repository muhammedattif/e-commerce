from dataclasses import dataclass
from typing import Text
from datetime import date
import operator

class Condition:
    """
    This a class that is made for dynamic if conditions
    """
    OPERATOR_SYMBOLS = {
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,
        '>': operator.gt,
        '>=': operator.ge
    }

    def __init__(self, value1, op, value2):
        self.value1 = value1
        self.op = op
        self.value2 = value2

    def run(self):
        return self.OPERATOR_SYMBOLS[self.op](self.value1, self.value2)


@dataclass
class PromoCodeConfig:
    """A configuration for the Promo code.
    """
    discount_type: Text
    amount: float = None
    percentage: int = None
    max_discount_limit: float = None
    users: list = None
    all_users: bool = False
    code: Text = None
    valid_from: date = date.today()
    valid_until: date = date.today()
    is_active: bool = True
    prefix: str = ""
    max_uses: int = 1
    is_infinite: bool = False
    usage_limit_per_user: int = 1
    user_usage_is_infinite: bool = False
    categories: list = None
    brands: list = None
    conditions: list = None
