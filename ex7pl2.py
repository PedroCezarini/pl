from scipy.optimize import linprog

# Objetivo: minimizar o custo total
# Custo: 0.06*x + 0.08*y
custos_unitarios = [0.06, 0.08]  # [custo_red, custo_blue]

# --------- Restrições ---------

# Restrição de cafeína total (máxima)
matriz_restricoes_max = [
    [1, 2]  # x + 2y <= 20
]
vetor_limites_max = [20]

# Restrições de quantidade mínima (convertidas para ≤)
matriz_restricoes_min = [
    [-8, -6],  # 8x + 6y >= 48 → -8x -6y <= -48
    [-1, -2]   # x + 2y >= 12 → -x -2y <= -12
]
vetor_limites_min = [-48, -12]

# Combinando todas as restrições (max + min)
matriz_total_restricoes = matriz_restricoes_max + matriz_restricoes_min
vetor_total_limites = vetor_limites_max + vetor_limites_min

# Limites das variáveis (x ≥ 0, y ≥ 0)
limites_x = (0, None)
limites_y = (0, None)

# ---------- DEBUG/EXPLICAÇÃO ----------

print("=== MODELO DO PROBLEMA ===")
print(f"Função objetivo: minimizar {custos_unitarios[0]}*x + {custos_unitarios[1]}*y")
print("\nRestrições (formato A_ub * [x, y] ≤ b_ub):")

for i, (a, b) in enumerate(zip(matriz_total_restricoes, vetor_total_limites), 1):
    print(f"{i}. {a[0]}*x + {a[1]}*y <= {b}")

print("\nLimites das variáveis:")
print(f"x: {limites_x}")
print(f"y: {limites_y}")
print("\nIniciando otimização...\n")

# ---------- CHAMANDO O SOLVER ----------

resultado = linprog(
    c=custos_unitarios,
    A_ub=matriz_total_restricoes,
    b_ub=vetor_total_limites,
    bounds=[limites_x, limites_y],
    method='highs'
)

# ---------- RESULTADO ----------

if resultado.success:
    red_doses, blue_doses = resultado.x
    custo_total = resultado.fun

    print("=== SOLUÇÃO ÓTIMA ENCONTRADA ===")
    print(f"Doses da solução Red (x): {red_doses:.2f}")
    print(f"Doses da solução Blue (y): {blue_doses:.2f}")
    print(f"Custo total mínimo: R${custo_total:.2f}")
else:
    print("❌ Não foi possível encontrar uma solução viável.")
    print("Mensagem do solver:", resultado.message)
