graphics_on = True

if graphics_on:
    import pygame
    from ViewController import ViewController
from Configuration import Configuration
from constants import *
from math import pi, cos, sin
from random import random, randint, uniform
from VertexState import VertexState
import multiprocessing as mp
from matplotlib import pyplot as plt


def main():
    configuration  = Configuration(N, M, TORUS)
    home = VertexState(is_home=True)

    for x in range(HOME_LOC[0][0], HOME_LOC[0][1]+1):
        for y in range(HOME_LOC[1][0], HOME_LOC[1][1]+1):
            configuration.vertices[(x,y)].state = VertexState(is_home=True)

    tasks = []
    task_locations = set()
    home_center = (HOME_LOC[0][0] + int((HOME_LOC[1][0] - HOME_LOC[0][0]) / 2), HOME_LOC[0][1] + int((HOME_LOC[1][1] - HOME_LOC[0][1]) / 2))
    ang = uniform(0, 2*pi)
    tumor_start = (int(home_center[0] + cos(ang)*TMR_DST), int(home_center[1] + sin(ang)*TMR_DST))
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
    tot_rd = NUM_TASKS
    residual_demand_over_time = []
    while tot_rd > 0:
        ct+=1
        configuration.transition()
        if graphics_on:
            vc.update()
        tot_rd = 0
        for task in tasks:
            tot_rd += task.residual_demand
        residual_demand_over_time.append(tot_rd)
    #(len(residual_demand_over_time))
    print(ct)

    # plt.plot(residual_demand_over_time)
    # plt.savefig("residual_demand_over_time.pdf")



    if graphics_on:
        vc.quit()


if __name__ == "__main__":
    main()
