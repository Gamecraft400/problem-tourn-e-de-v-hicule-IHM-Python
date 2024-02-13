import networkx as nx
import matplotlib.pyplot as plt
from docplex.mp.model import Model 

 # Données
D = 1
C = 10
V = 4
Qmax = 100

demande = [60, 18, 26, 15, 44, 32, 20, 10, 27, 11]
Distij = [
    [0, 2.7, 4.6, 2.8, 3, 3.3, 3.1, 2.7, 5.1, 3.9, 4.7],
    [2.7, 0, 3.1, 0.8, 1.8, 2.5, 4.2, 1.4, 3.6, 2.5, 3],
    [4.6, 3.1, 0, 3.3, 4.4, 1.7, 6.8, 4.1, 1.3, 1.7, 1.4],
    [2.8, 0.8, 3.3, 0, 1.9, 2, 4, 1.5, 3.8, 2.8, 3.2],
    [3, 1.8, 4.4, 1.9, 0, 3.4, 2.6, 0.5, 4.7, 4.7, 4.1],
    [3.3, 2.5, 1.7, 2, 3.4, 0, 5.8, 3, 1.8, 0.5, 2.6],
    [3.1, 4.2, 6.8, 4, 2.6, 5.8, 0, 3, 7.4, 6.1, 7.6],
    [2.7, 1.4, 4.1, 1.5, 0.5, 3, 3, 0, 4.6, 3.7, 4.3],
    [5.1, 3.6, 1.3, 3.8, 4.7, 1.8, 7.4, 4.6, 0, 1.4, 2.8],
    [3.9, 2.5, 1.7, 2.8, 4.7, 0.5, 6.1, 3.7, 1.4, 0, 2.8],
    [4.7, 3, 1.4, 3.2, 4.1, 2.6, 7.6, 4.3, 2.8, 2.8, 0]
]

# Création du modèle
model = Model(name='VRP')

# Ensembles
clients = range(1, C + D + 1)
vehicles = range(1, V + 1)

# Variables de décision
x = model.binary_var_cube(clients, clients, vehicles, name=lambda keys: f'x_{keys[0]}_{keys[1]}_{keys[2]}')
u = model.integer_var_dict(clients, lb=0, ub=Qmax, name=lambda i: f'u_{i}')
nbre = model.integer_var(lb=0, ub=V, name='nbre')
Qaprestour = model.integer_var_dict(vehicles, lb=0, ub=Qmax, name=lambda k: f'Qaprestour_{k}')

# Fonction objective
model.minimize(model.sum(Distij[i-1][j-1] * x[i, j, k] for i in clients for j in clients for k in vehicles))

# Contraintes
for j in clients:
    if j > 1:
        model.add_constraint(model.sum(x[i, j, k] for i in clients for k in vehicles) == 1)

for k in vehicles:
    for j in clients:
        model.add_constraint(model.sum(x[i, j, k] for i in clients) == model.sum(x[j, i, k] for i in clients))

for k in vehicles:
    for i in clients:
        for j in clients[1:]:
            model.add_constraint(demande[j-2] * x[i, j, k] <= Qmax)

for i in clients:
    if i != 1:
        model.add_constraint(demande[i-2] <= u[i])
        model.add_constraint(u[i] <= Qmax)

for i in clients:
    for k in vehicles:
        model.add_constraint(x[i, i, k] == 0)

for i in clients:
    for j in clients:
        for k in vehicles:
            if i != j and i != 1 and j != 1:
                model.add_constraint(u[j] - u[i] >= demande[j-2] - Qmax * (1 - x[i, j, k]))

for k in vehicles:
    model.add_constraint(Qaprestour[k] == Qmax - model.sum(demande[j-2] * x[i, j, k] for i in clients for j in clients[1:]))
    model.add_constraint(nbre == model.sum(Qaprestour[k] <= Qmax - 1 for k in vehicles))

# Résolution du modèle
model.solve()

# Affichage des résultats
print('Valeur optimale :', model.objective_value)
print('Véhicules utilisés :', model.solution.get_value(nbre))
for k in vehicles:
    print(f"Quantité restante du véhicule {k} : {model.solution.get_value(Qaprestour[k])}")

# Extraction des valeurs de solution pour x
solution_x = {(i, j, k): model.solution.get_value(x[i, j, k]) for i in clients for j in clients for k in vehicles}

# Création d'un graphe orienté
G = nx.DiGraph()

# Définir la taille de la figure
plt.figure(figsize=(15, 8))

# Positions des clients
positions_clients = {
    1: (0,0),
    2: (-15, 6),
    3: (10, -1),
    4: (-4, 6),
    5: (2, -11),
    6: (10, 6),
    7: (8, -5),
    8: (-10, -10),
    9: (18, 2),
    10: (18, 6),
    11: (-20, 4)
}
# Liste de couleurs pour trajets des véhicules
colors = ['blue','red' ,'green']

# Ajout des nœuds clients avec les positions basées sur la solution
for client, pos in positions_clients.items():
    G.add_node(client, pos=pos)

# Ajout des arcs avec un poids représentant la demande du client
for (i, j, k), valeur in solution_x.items():
    if valeur > 0.5:  # On considère uniquement les arcs avec un flux significatif
        G.add_edge(i, j, weight=demande[j-2])

# Tracé du graphe
pos = nx.get_node_attributes(G, 'pos')

# Nœuds
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')

# Arcs avec flèches
for (i, j, k), valeur in solution_x.items():
    if valeur > 0.5:
        edge = [(i, j)]
        edge_labels = {(i, j): str(demande[j-2])}
        nx.draw_networkx_edges(G, pos, edgelist=edge, connectionstyle=f"arc3,rad=0.1", arrows=True, width=2.0, edge_color=colors[k-1], alpha=1)
        if j != 1:
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', alpha=0.7, bbox=dict(facecolor='none', edgecolor='none'))

# Étiquettes des nœuds (numéro du client)
node_labels = {node: str(node) for node in G.nodes}
nx.draw_networkx_labels(G, pos, labels=node_labels)

# Valeur de la solution optimale avec une décimale
optimal_value = round(model.objective_value, 1)

# Afficher le graphique
plt.title('Solution du Problème de Routage de Véhicules')
plt.legend([f'Solution optimale : {optimal_value}'], bbox_to_anchor=(0.1, 0.5), fancybox=True, shadow=True)
plt.axis('off')
plt.show()