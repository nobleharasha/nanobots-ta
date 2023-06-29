import math

INFLUENCE_RADIUS = 1
TORUS = True

#Location Parameters
N = 50
M = 50

#Home Location
HOME_LOC = ((25, 25), (25, 25))

#Tasks and Agents
NUM_AGENTS = 50
K = 0.8
TOTAL_DEMAND = int(NUM_AGENTS*K)
#NUM_TASKS = 4
NUM_TASKS = 1
EXPECTED_DEMAND_PER_TASK = TOTAL_DEMAND/NUM_TASKS
assert(NUM_TASKS >= 1)
assert(EXPECTED_DEMAND_PER_TASK >= 1)

#General Constants
INF = 1000000000

#TAHH
L = 1/100

#Levy Flight Constants
levy_loc = 10
levy_cap = 1/L



TMR_DNS = .5
TMR_DST = (min(M, N) / 2) * (2/3)


MARKER_DEATH = 1000




T = 10
P = math.ceil(math.pi * 25)

ALPHA = 0.5

EPSILON = 0.05

p_m = 0.05
p_m_markers = 0.025
