# why is this function necessary when the python-native round() function exists?
# since Python 3, this function implements banker's rounding:
# round(0.5) == 0, round(1.5) == 2
import decimal


def round_value(value: float) -> float:
    return float(decimal.Decimal(value).quantize(decimal.Decimal('.1'), rounding=decimal.ROUND_HALF_UP))


def round_to_two_decimal_places(value: float) -> float:
    return float(decimal.Decimal(value).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_HALF_UP))