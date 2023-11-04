import numpy as np
from scipy.special import erfc
from scipy.integrate import dblquad
import matplotlib.pyplot as plt
import time

# N_ring_series = np.array([2, 3, 5])
# N_ring = 20
# R = 1  # m
# pitch: np.float16 = 0.2  # m

N_ring =20
R = 0.76  # m
pitch: np.float16 = 0.4  # m

# alpha = 1e-6  # m2/s
t_series = np.arange(0.01, 3, 0.1)  #consider alpha
t_1 = int(1e6)
h = 1.5  # m

def sqrt_float16(x):
    return np.sqrt(x).astype(np.float16)

def erfc_float16(x):
    return erfc(x).astype(np.float16)

def cos_float16(x):
    return np.cos(x).astype(np.float16)

def sin_float16(x):
    return np.sin(x).astype(np.float16)

def quadself(f, a, b, c, d, nx, ny):
    # Function to approximate the double integral
    dx: np.float16 = (b - a) / nx
    dy: np.float16 = (d - c) / ny

    integral_sum: np.float16 = 0.0

    for i in range(nx):
        x = a + (i + 0.5) * dx

        for j in range(ny):
            y = c + (j + 0.5) * dy
            integral_sum += f(x, y)

    integral_sum *= dx * dy

    return integral_sum

start_time = time.time()

# gs_series = []
# for N_ring in N_ring_series:
gs_series = []
for t in t_series:
    gs: np.float16 = 0
    for i in range(1, N_ring + 1):
        for j in range(1, N_ring + 1):
            if i != j:
                def d(w: np.float16, phi: np.float16):
                    return sqrt_float16((pitch * (i - j) + R * (cos_float16(phi) - cos_float16(w)))**2 +
                               (R * (sin_float16(phi) - sin_float16(w)))**2)

                def fun(w: np.float16, phi: np.float16):
                    return erfc_float16(d(w, phi) / (2 * sqrt_float16(t))) / d(w, phi) - erfc_float16(sqrt_float16(d(w, phi)**2 + 4 * h**2) / (2 * sqrt_float16(t))) / sqrt_float16(d(w, phi)**2 + 4 * h**2)

                # b, _ = dblquad(fun, 0, 2 * np.pi, lambda phi: 0, lambda phi: 2 * np.pi, epsabs=1e-2, epsrel=1e-2)
                b = quadself(fun, 0, 2 * np.pi, 0, 2 * np.pi, 10, 10)
                # print(b)
                gs += np.float16(b)

    print(f"gs: {gs}")
    gs_series.append(gs)

end_time = time.time()
elapsed_time = end_time - start_time

print("Elapsed time: {:.2f}".format(elapsed_time))

plt.plot(t_series, gs_series)
plt.show()