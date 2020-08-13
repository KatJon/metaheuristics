import math

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from random import (
    random,
    randint,
    shuffle,
)

data = [
    ('DW', 17.02, 51.07), # Wrocław                 17°02'E        51°07'N
    ('OP', 17.56, 50.40), # Opole                   17°56'E        50°40'N
    ('SK', 19.00, 50.15), # Katowice                19°00'E        50°15'N
    ('KR', 19.57, 50.03), # Kraków                  19°57'E        50°03'N
    ('RZ', 22.01, 50.03), # Rzeszów                 22°01'E        50°03'N
    ('FZ', 15.30, 51.56), # Zielona Góra            15°30'E        51°56'N
    ('FG', 15.14, 52.44), # Gorzów Wielkopolski     15°14'E        52°44'N
    ('PO', 16.55, 52.25), # Poznań                  16°55'E        52°25'N
    ('EL', 19.28, 51.47), # Łódź                    19°28'E        51°47'N
    ('TK', 20.37, 50.53), # Kielce                  20°37'E        50°53'N
    ('WA', 21.02, 52.12), # Warszawa                21°02'E        52°12'N
    ('LU', 22.34, 51.14), # Lublin                  22°34'E        51°14'N
    ('ZS', 14.34, 53.26), # Szczecin                14°34'E        53°26'N
    ('CB', 18.00, 53.07), # Bydgoszcz               18°00'E        53°07'N
    ('CT', 18.37, 53.02), # Toruń                   18°37'E        53°02'N
    ('GD', 18.38, 54.22), # Gdańsk                  18°38'E        54°22'N
    ('NO', 20.30, 53.47), # Olsztyn                 20°30'E        53°47'N
    ('BI', 23.10, 53.08), # Białystok               23°10'E        53°08'N
]

cities = [(x,y) for (_,x,y) in data]

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

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

Tmax = 100
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

    ax4.plot([])

ani = animation.FuncAnimation(fig, animate, interval=10)

plt.show()
