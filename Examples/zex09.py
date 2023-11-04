import numpy as np
from scipy.special import erfc
from scipy.integrate import quad
from decimal import *
getcontext().prec = 4

R = 1  # m
pitch = 0.2  # m
alpha = 1e-6  # m2/s
h = 2  # m
a = [2.33434, 6]

print(h/Decimal(alpha))