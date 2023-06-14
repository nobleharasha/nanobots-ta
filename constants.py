INFLUENCE_RADIUS = 1
TORUS = False

#Location Parameters
N = 50
M = 50

#Home Location
HOME_LOC = ((24, 26), (24, 26))

#Tasks and Agents
NUM_AGENTS = 30
K = 0.8
TOTAL_DEMAND = int(NUM_AGENTS*K)
#NUM_TASKS = 4
NUM_TASKS = 15
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



TMR_DNS = .4
TMR_DST = (min(M, N) / 2) * .7


T = 10

ALPHA = 0.5

EPSILON = 0.05

p_m = 0.05
p_m_beacons = 0.025
