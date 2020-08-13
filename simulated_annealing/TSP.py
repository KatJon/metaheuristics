import math

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from random import (
    random,
    randint, 
    choice,
    shuffle,
)

cities = [(randint(0,100), randint(0,100)) for _ in range(40)]

fig = plt.figure()
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

solution = [i for i,_ in enumerate(cities)]
history = []
temp = []

shuffle(solution)

def solution_graph(sol):
    G = nx.Graph()

    for (u,v) in zip(sol, sol[1:]):
        G.add_edge(u, v)

    G.add_edge(sol[-1], sol[0])

    return G

def dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def cost(sol):
    c = 0
    for (u,v) in zip(sol, sol[1:]):
        c += dist(cities[u],cities[v])

    c += dist(cities[sol[-1]], cities[sol[0]])

    return c

Tmax = 1000
Tmin = 1
Factor = 0.99

Cost = cost(solution)

T = Tmax

def anneal():
    global T
    global Cost
    T = T * Factor

    for _ in range(500):
        a = randint(0, len(solution) - 1)
        b = randint(0, len(solution) - 1)

        solution[a],solution[b] = solution[b],solution[a]

        C1 = cost(solution)

        if C1 < Cost:
            Cost = C1
        else:
            x = random()

            if x < math.exp((Cost - C1) / T):
                Cost = C1
            else:
                solution[a],solution[b] = solution[b],solution[a]
    return Cost

def animate(i):
    c = anneal()

    G = solution_graph(solution)

    ax1.clear()
    nx.draw_networkx(G, cities, ax=ax1,
        with_labels=False,
        node_size=50)

    history.append(c)
    print(i, c)

    ax2.clear()
    ax2.plot(history)

    temp.append(T)

    ax3.clear()
    ax3.plot(temp)

ani = animation.FuncAnimation(fig, animate, interval=10)

plt.show()
