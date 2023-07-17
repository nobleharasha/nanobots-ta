graphics_on = True

if graphics_on:
    import pygame
from ViewController import ViewController, tumor_start
from Configuration import Configuration
from constants import *
from math import pi, cos, sin, ceil
from random import random, randint, uniform
from VertexState import VertexState
import multiprocessing as mp
from matplotlib import pyplot as plt
import numpy as np
from geo_utils import l2_distance


def main():

    configuration  = Configuration(N, M, P, TORUS)
    configuration.vertices[(int(M / 2), int(N / 2))].state.cancer = True

    # Initialize agents
    agent_locations = []
    for i in range(NUM_AGENTS):
        agent_locations.append((0, 0))

    configuration.add_agents(agent_locations)
    if graphics_on:
        vc = ViewController(configuration)
    ct = 0
    #while configuration.vertices[(int(M / 2), int(N / 2))].state.num_bound <= NUM_AGENTS:


    dispersion_vals = []
    while ct <= 1000:
        ct+=1
        configuration.transition()

        dispersion = 0
        for x in range(M):
            for y in range(N):
                dispersion += len(configuration.vertices[(x,y)].agents) * l2_distance(x, y, int(M / 2), int(N / 2))
        dispersion_vals.append(dispersion)

        if graphics_on:
            vc.update()

    if graphics_on:
        vc.quit()

    # fuel_to_visits = {}
    # fuel_to_visits_avg = {}
    # for i in [0,4,8]:
    #     fuel_to_visits[i] = [0,0]
    #     fuel_to_visits_avg[i] = 0
    #
    # for x in range(M):
    #     for y in range(N):
    #         vertex = configuration.vertices[(x,y)]
    #         fuel = vertex.state.fuel
    #         fuel_to_visits[fuel][0] += vertex.state.visits
    #         fuel_to_visits[fuel][1] += 1
    #
    #
    # for i in fuel_to_visits_avg:
    #     fuel_to_visits_avg[i] = fuel_to_visits[i][0] / fuel_to_visits[i][1]
    #
    # return fuel_to_visits_avg

    return dispersion_vals


if __name__ == "__main__":



    print(main())


    # p = math.ceil(math.pi * 25)
    # runtimes = []
    # for _ in range(20):
    #     runtimes.append(main(alphas, p))
    # print(runtimes)


    # x = []
    # y = []

    # file = open("MARK_16_06_data.txt", "w")
    #
    # alphas = np.arange(0,.9001,.05)
    # ps = np.arange(10,50.001,5)
    # runtimes = []
    # for p in ps:
    #     tmp = []
    #     for _ in range(10):
    #         out = main(alphas, p)[-1]
    #         file.write(str(out) + ", ")
    #         tmp.append(out)
    #     file.write("\n")
    #     runtimes.append(tmp)
    # print(runtimes)
    # file.close()



    # f2 = open("RW_16_06_data.txt", "w")
    # alphas = np.arange(0,.9001,.05)
    # runtimes = []
    # for _ in range(10):
    #     out = main(alphas)[-1]
    #     f2.write(str(out) + ", ")
    #     runtimes.append(out)
    # print(runtimes)
    # f2.close()


    #runtimes = [ [1,29,120,136,144,162,204,227,234,289,296,319,359,387,420,422,495,560,744,1183,1192], [1,24,83,104,111,159,186,222,224,247,283,307,313,330,455,490,633,711,734,784,1217],[1,33,56,62,67,88,101,107,113,128,132,140,146,170,242,401,439,615,831,865,1153],[1,28,55,84,106,139,156,172,181,231,239,273,361,367,415,440,505,599,733,911,1036],[1,117,156,180,200,209,246,249,259,342,345,401,704,716,735,769,812,1104,1126,1222,1781],[1,44,82,132,160,192,202,289,295,336,347,368,384,387,468,513,549,587,676,792,1195],[1,59,69,85,94,117,121,137,180,190,205,223,288,315,446,455,469,527,596,805,829],[1,32,48,66,156,188,212,236,251,301,310,399,414,494,517,524,544,685,850,978,1571],[1,23,63,85,89,181,221,226,261,279,302,337,380,416,450,468,589,632,835,913,1118],[1,46,54,73,73,145,177,185,189,206,239,305,326,334,359,364,425,611,666,848,1463] ]

    # for i in range(len(runtimes[0])):
    #     tmp = []
    #     for j in range(len(runtimes)):
    #         tmp.append(runtimes[j][i])
    #     x.append(alphas[i])
    #     y.append(sum(tmp)  / len(tmp))
    #
    #
    # print(x, y)
    #
    # fig, ax = plt.subplots()
    # ax.plot(y, x)
    #
    # plt.xlabel('# Rounds')
    # plt.ylabel('% Agents That Have Vistied Tumor')
    # #plt.title('Effect of Task Density on Average (Propagator) Messages Sent')
    # plt.savefig("TEST4_alphasvruntimes_10trials.pdf", dpi=300, bbox_inches='tight', pad_inches=0)
    # plt.show()


    #print(f"Avg: {sum(runtimes) / len(runtimes)}")
