from decimal import ROUND_HALF_UP, Decimal

ZERO = Decimal(0)
PERCENTAGE_BASE = Decimal(100)
MIN_PERCENTAGE = Decimal(0)
MAX_PERCENTAGE = Decimal(100)

# Índice de desempeño que indica que se avanza exactamente según lo planificado.
ON_TARGET_INDEX = Decimal(1)

MONEY_PRECISION = Decimal("0.01")
INDEX_PRECISION = Decimal("0.0001")
ROUNDING_MODE = ROUND_HALF_UP
