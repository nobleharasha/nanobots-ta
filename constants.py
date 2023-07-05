INFLUENCE_RADIUS = 0

TORUS = True

N = 1
M = 50

INJECT_LOC = ((25,25), (0,0))

NUM_AGENTS = 50
PROP_SCOUTS = 0.6

CELLS_PER_LOC = (5,5)
PROP_CANCER = 0.05  # percent (probability) of total cells in he given environment that are cancerous (maybe later something about favoring clustering to be more realistic, precise)
PROP_MARKED_GOOD = 0.01  # probability that an individual good cell has the "cancer" marker
MARKERS = {"m_ca", "m_sc", "chemo"}

SCOUT_TIME = M * 5
BOT_LIFESPAN = M * 100

P1 = 0.1
P2 = lambda x : min(1, 2*x / NUM_AGENTS)

GAMMA = 10
