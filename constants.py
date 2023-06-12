INFLUENCE_RADIUS = 1
TORUS = False

#Location Parameters
N = 50
M = 50

#Home Location
HOME_LOC = ((24, 26), (24, 26))

#Tasks and Agents
NUM_AGENTS = 50
K = 0.8
TOTAL_DEMAND = int(NUM_AGENTS*K)
#NUM_TASKS = 4
NUM_TASKS = 30
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
TMR_DST = (min(M, N) / 2) * .75


t = 1
a = 1
b = 1
alpha = 25
p_e = 0.01
p_m = 0.1
p_c = 0.6
f = lambda l : l[0]
k = 4
T = 30
