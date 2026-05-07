import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# ======================================================
# PROGRAMMATION LINEAIRE : GESTION DES DECHETS URBAINS
# ======================================================
# Max Z = 120x + 90y
# Contraintes :
# x + y <= 150
# 50x + 30y <= 6000
# 2x + y <= 160
# x >= 0, y >= 0

# ------------------------------------------------------
# 1. Définition du problème
# ------------------------------------------------------
c = [-120, -90]  # Maximisation => minimiser l'opposé

A = [
    [1, 1],
    [50, 30],
    [2, 1]
]

b = [150, 6000, 160]

bounds = [(0, None), (0, None)]

# Résolution avec Simplexe moderne (HiGHS)
result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

x_opt, y_opt = result.x
z_opt = -result.fun

print("===== SOLUTION OPTIMALE =====")
print(f"Procédé A (x) : {x_opt:.2f} tonnes")
print(f"Procédé B (y) : {y_opt:.2f} tonnes")
print(f"Efficacité maximale Z : {z_opt:.2f}")

# ------------------------------------------------------
# 2. GRAPHIQUE 1 : Région réalisable
# ------------------------------------------------------
x = np.linspace(0, 160, 500)

c1 = 150 - x
c2 = (6000 - 50 * x) / 30
c3 = 160 - 2 * x

plt.figure(figsize=(10, 8))
plt.plot(x, c1, label='x + y ≤ 150')
plt.plot(x, c2, label='50x + 30y ≤ 6000')
plt.plot(x, c3, label='2x + y ≤ 160')

# Zone réalisable
y_feasible = np.minimum.reduce([c1, c2, c3])
y_feasible = np.maximum(y_feasible, 0)

plt.fill_between(x, y_feasible, where=(y_feasible >= 0), alpha=0.3)

# Solution optimale
plt.scatter(x_opt, y_opt, color='red', s=120, label='Solution optimale')
plt.annotate(f'({x_opt:.0f}, {y_opt:.0f})', (x_opt, y_opt))

plt.xlim(0, 160)
plt.ylim(0, 160)
plt.xlabel('Procédé A (x)')
plt.ylabel('Procédé B (y)')
plt.title('Graphique 1 : Région Réalisable')
plt.legend()
plt.grid(True)
plt.show()

# ------------------------------------------------------
# 3. GRAPHIQUE 2 : Convergence du simplexe
# ------------------------------------------------------
# Parcours pédagogique des sommets
points = np.array([
    [0, 0],
    [80, 0],
    [10, 140]
])

z_values = [120 * p[0] + 90 * p[1] for p in points]

plt.figure(figsize=(10, 6))
plt.plot(range(len(z_values)), z_values, marker='o')

for i, val in enumerate(z_values):
    plt.annotate(f'{val}', (i, val))

plt.xticks(range(len(z_values)), ['Origine', 'Sommet B', 'Optimum C'])
plt.ylabel('Valeur de Z')
plt.xlabel('Itérations')
plt.title('Graphique 2 : Convergence du Simplexe')
plt.grid(True)
plt.show()

# ------------------------------------------------------
# 4. GRAPHIQUE 3 : Utilisation des ressources
# ------------------------------------------------------
resources_used = [
    x_opt + y_opt,
    50 * x_opt + 30 * y_opt,
    2 * x_opt + y_opt
]

resources_limits = [150, 6000, 160]
labels = ['Capacité', 'Budget', 'Logistique']

x_pos = np.arange(len(labels))
width = 0.35

plt.figure(figsize=(10, 6))
plt.bar(x_pos - width / 2, resources_used, width, label='Utilisé')
plt.bar(x_pos + width / 2, resources_limits, width, label='Disponible')

plt.xticks(x_pos, labels)
plt.ylabel('Quantité')
plt.title('Graphique 3 : Utilisation des Ressources')
plt.legend()
plt.grid(axis='y')
plt.show()

# ------------------------------------------------------
# 5. GRAPHIQUE 4 : Prix marginaux / Dualité
# ------------------------------------------------------
shadow_prices = result.ineqlin.marginals

plt.figure(figsize=(10, 6))
plt.bar(labels, shadow_prices)
plt.ylabel('Prix marginal')
plt.xlabel('Contraintes')
plt.title('Graphique 4 : Prix Marginaux / Dualité')
plt.grid(axis='y')
plt.show()

# ------------------------------------------------------
# 6. Résumé final
# ------------------------------------------------------
print("\n===== PRIX MARGINAUX =====")
for label, price in zip(labels, shadow_prices):
    print(f"{label} : {price:.4f}")

print("\n===== FIN DU PROGRAMME =====")
