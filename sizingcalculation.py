import math

# Define variables

#################### System
E_heat = 2000  # heat load [W*h]
T_in = 60  # Hot Fluid Temperature 60~65dC, 140~150dF

#################### Fluid
# Fluid Type
mu = 0.011  # viscosity [Pa*s]
c_p = 3344  # specific heat [K*Kg^-1*dC^-1]
rho = 1100  # density [Kg*m^-3]

#################### Soil
T_g = 10  # undisturbed ground temperature dC
k_soil = 0.07  # conductivity [W/(m*K)]

#################### Pipe
########## Pipe Properties
D_i = 0.021  # inner diameter [m]
D_o = 0.026  # outer diameter [m]
k_pipe = 0.14  # conductivity  [W/m*K]

########## Pipe Configuration
d = 2  # pipe buried depth [m]

#################### Heat Pump
V = 1.5  # velocity of fluid [m/s]
EWt = 40  # EWT - entering water temperature

# Resistance
R_e = rho * V * D_i / mu  # Reynolds number    Re<2100 laminar regime; 2100<Re<10000: transitional regime; Re>10000 turbulent regime
P_r = mu * c_p / k_pipe  # Prandtl number
h_w = 0.023 * R_e ** 0.8 * P_r ** 0.3 * k_pipe / D_i  # heat transfer coefficient [W/(m^2*k)]

R_conv = 1 / (3.14159 * D_i * h_w)
R_pipe = math.log(D_o / D_i) / (2 * 3.14159 * k_pipe)
S = 2 * 3.14159 / math.log((2 * d / D_o) + math.sqrt((2 * d / D_o) ** 2 - 1))  # conduction shape factor of the pipe
R_soil = 1 / (S * k_soil)

R_total = R_conv + R_pipe + R_soil

# Length calculation
m_w = rho * V * 3.14159 * (D_i / 2) ** 2
T_out = T_in - E_heat / (m_w * c_p)
theta_w_in = T_in - T_g
theta_w_out = T_out - T_g

L = (m_w * c_p * R_total) * math.log(theta_w_in / theta_w_out)

print("length of pipe:", L)

loop_diameter = 0.75
pitch = 0.4

# Other requirements
# - distance between trenches spaced a minimum of 1.5m to neglect the thermal interference
# - solar radiation affects the earth to a depth of about 9m
