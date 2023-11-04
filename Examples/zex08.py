import numpy as np
from scipy.special import erfc
from scipy.integrate import dblquad
from numba import njit


@njit(parallel=True)
def calculate_gs(N_ring, t_series):
    R = 1  # m
    pitch = 0.2  # m
    alpha = 1e-6  # m2/s
    h = 2  # m

    gs_series = np.zeros(len(t_series))

    for idx, t in enumerate(t_series):
        gs = 0.0
        for i in range(1, N_ring + 1):
            for j in range(1, N_ring + 1):
                if i != j:
                    gs += integrate(N_ring, pitch, R, alpha, h, t, i, j)

        gs_series[idx] = gs

    return gs_series


@njit
def integrate(N_ring, pitch, R, alpha, h, t, i, j):
    result = 0.0

    for w in np.linspace(0, 2 * np.pi, 100):
        for phi in np.linspace(0, 2 * np.pi, 100):
            result += fun(w, phi, N_ring, pitch, R, alpha, h, t, i, j)

    return result * (2 * np.pi) ** 2 / (100 ** 2)


@njit
def fun(w, phi, N_ring, pitch, R, alpha, h, t, i, j):
    d = np.sqrt((pitch * (i - j) + R * (np.cos(phi) - np.cos(w))) ** 2 +
                (R * (np.sin(phi) - np.sin(w))) ** 2)

    result = (erfc(d / (2 * np.sqrt(alpha * t))) / d -
              erfc(np.sqrt(d ** 2 + 4 * h ** 2) / (2 * np.sqrt(alpha * t))) /
              np.sqrt(d ** 2 + 4 * h ** 2))

    return result


# Set parameters
N_ring = 5
t_series = np.arange(10000, 3e7 + 1, 1e6)

# Calculate gs_series
gs_series = calculate_gs(N_ring, t_series)

# Set print options
np.set_printoptions(precision=6)
print(gs_series)