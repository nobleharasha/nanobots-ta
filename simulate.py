graphics_on = True

if graphics_on:
    import pygame
from ViewController import ViewController
from Configuration import Configuration
from constants import *
from math import pi, cos, sin
from random import random, randint, uniform
from VertexState import VertexState
from matplotlib import pyplot as plt
import numpy as np


def main():
    configuration  = Configuration(N, M, TORUS)

    for x in range(INJECT_LOC[0][0], INJECT_LOC[0][1]+1):
        for y in range(INJECT_LOC[1][0], INJECT_LOC[1][1]+1):
            configuration.vertices[(x,y)].state = VertexState(is_home=True)
    configuration.add_cells()

    agent_locations = []
    agent_types = []
    for i in range(NUM_AGENTS):
        if i >= int(PROP_SCOUTS * NUM_AGENTS):
            type = "W"
        else:
            type = "S"
        agent_locations.append((randint(INJECT_LOC[0][0], INJECT_LOC[0][1]), randint(INJECT_LOC[1][0], INJECT_LOC[1][1])))
        agent_types.append(type)
    configuration.add_agents(agent_locations, agent_types)

    if graphics_on:
        vc = ViewController(configuration)

    ct = 0
    num_active_agents = NUM_AGENTS
    while num_active_agents > 0:
        ct+=1
        configuration.transition()

        num_active_agents = len([a for a in configuration.agents if not configuration.agents[a].state.bound])

        if graphics_on:
            vc.update()

    if graphics_on:
        vc.quit()


    num_cancer_tot, num_good_tot = 0, 0
    num_cancer_treated, num_good_treated = 0, 0
    for v in configuration.vertices:
        vertex = configuration.vertices[v]
        treated = vertex.state.chemicals["chemo"] > 0
        for c in vertex.cells:
            if c.state.cancer:
                num_cancer_tot += 1
                if treated:
                    num_cancer_treated += 1
            else:
                num_good_tot += 1
                if treated:
                    num_good_treated += 1

    prop_cancer_treated, prop_good_treated = num_cancer_treated / num_cancer_tot, num_good_treated / num_good_tot
    print(f"cancer cells treated: {prop_cancer_treated}, good cells treated: {prop_good_treated}, runtime: {ct}")
    return (prop_cancer_treated, prop_good_treated, ct)


if __name__ == "__main__":
    main()
