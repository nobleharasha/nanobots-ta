from constants import N, M, HOME_LOC

def create_tumor(size, dist):
    home_center = (int((HOME_LOC[1][0] - HOME_LOC[0][0]) / 2), int((HOME_LOC[1][1] - HOME_LOC[0][1]) / 2))
    density = 1

    i = 0
    while i < size:
