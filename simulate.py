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


def main(alphas=[], p=25):

    P = int(p)

    configuration  = Configuration(N, M, P, TORUS)
    home = VertexState(is_home=True)

    for x in range(HOME_LOC[0][0], HOME_LOC[0][1]+1):
        for y in range(HOME_LOC[1][0], HOME_LOC[1][1]+1):
            configuration.vertices[(x,y)].state = VertexState(is_home=True)

    tasks = []
    task_locations = set()
    tasks.append(VertexState(is_task=True, demand=1, task_location=tumor_start))
    task_locations.add(tumor_start)
    i = 1
    while i < NUM_TASKS:
        task_location = (randint(0,M-1), randint(0,N-1))
        if task_location in task_locations or configuration.vertices[task_location].state.is_home:
            continue
        neighbor_ct = 0
        for dx in range(-1,1+1):
            for dy in range(-1,1+1):
                if abs(dx) > 0 and abs(dy) > 0:
                    pass
                elif (task_location[0]+dx, task_location[1]+dy) in task_locations:
                    neighbor_ct += 1
        if neighbor_ct == 0:
            continue
        #low density -> higher prob as neighbor_ct lower
        #high density -> lower prob as neighbor_ct higher
        TMR_DNS_mapped = (TMR_DNS - 0.5) * 5
        if random() <= (neighbor_ct / 4)**TMR_DNS_mapped:
            tasks.append(VertexState(is_task=True, demand=1, task_location=task_location))
            task_locations.add(task_location)
            i += 1



    # for i in range(TOTAL_DEMAND-NUM_TASKS):
    #     task_num = randint(0, NUM_TASKS-1)
    #     tasks[task_num].demand += 1
    #     tasks[task_num].residual_demand += 1


    for task_state in tasks:
        configuration.vertices[task_state.task_location].state = task_state


    # Initialize agents
    agent_locations = []
    for i in range(NUM_AGENTS):
        agent_locations.append((randint(HOME_LOC[0][0], HOME_LOC[0][1]), randint(HOME_LOC[1][0], HOME_LOC[1][1])))

    configuration.add_agents(agent_locations)
    if graphics_on:
        vc = ViewController(configuration)
    ct = 0

    runtimes_at_each_alpha = []

    num_drug_visits = 0
    while num_drug_visits <= alphas[-1] * NUM_AGENTS:
        ct+=1
        configuration.transition()
        for a in configuration.agents:
            if configuration.agents[a].state.mode == "D":
                configuration.drug_visits_peragent[a] = 1
        num_drug_visits = sum(list(configuration.drug_visits_peragent.values()))

        for i in range(len(alphas)):
            if num_drug_visits >= NUM_AGENTS * alphas[i] and len(runtimes_at_each_alpha) <= i:
                runtimes_at_each_alpha.append(ct)
                print(ct)

        if graphics_on:
            vc.update()

    # print('\n')


    if graphics_on:
        vc.quit()

    #return ct
    print(f"p:{p}, runtimes:{runtimes_at_each_alpha}")
    return runtimes_at_each_alpha[-1]


if __name__ == "__main__":


    alphas = np.arange(0,.9001,.05)


    main(alphas)


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
