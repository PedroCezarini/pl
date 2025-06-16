from scipy.optimize import linprog

# Objetivo: minimizar o custo total
# Custo: 0.06*x + 0.08*y
custos_unitarios = [0.06, 0.08]  # [custo_red, custo_blue]

# Cafeína total não pode ultrapassar 20g
matriz_restricoes_max = [
    [1, 2]  # x + 2y <= 20
]
vetor_limites_max = [20] 

# Qtd minima de guarana e cafeina
matriz_restricoes_min = [
    [-8, -6],  # 8x + 6y => 48
    [-1, -2]   # 1x + 2y => 12
]
vetor_limites_min = [-48, -12]

# Criando uma matriz juntando as restrições min e max
matriz_total_restricoes = matriz_restricoes_max + matriz_restricoes_min
vetor_total_limites = vetor_limites_max + vetor_limites_min

# Condições de não negatividade
limites_x = (0, None)
limites_y = (0, None)

# Chamando a função linprog com os parametros criados até então e usando método HIGHS em vez do simplex
resultado = linprog(
    c=custos_unitarios,
    A_ub=matriz_total_restricoes,
    b_ub=vetor_total_limites,
    bounds=[limites_x, limites_y],
    method='highs'
)

# Printando os resultados
if resultado.success:
    red_doses, blue_doses = resultado.x
    custo_total = resultado.fun

    print("=== Solução ótima encontrada ===")
    print(f"Doses da solução Red (x): {red_doses:.2f}")
    print(f"Doses da solução Blue (y): {blue_doses:.2f}")
    print(f"Custo total mínimo: R${custo_total:.2f}")
else:
    print("Não foi possível encontrar uma solução viável.")
