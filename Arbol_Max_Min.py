# kruskal_simulador.py
# Simulador de Árbol de Mínimo y Máximo coste con Kruskal
# Muestra paso a paso en consola y, si hay librerías, dibuja el resultado.

# =============================
# 1. Intentar importar librerías gráficas (opcional)
# =============================
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    HAY_GRAFICOS = True
except ImportError:
    HAY_GRAFICOS = False

# =============================
# 2. Estructura Union-Find (Disjoint Set)
# =============================
class UnionFind:
    def __init__(self, elementos):
        # Cada nodo es su propio padre al inicio
        self.parent = {x: x for x in elementos}
        self.rank = {x: 0 for x in elementos}

    def find(self, x):
        # Búsqueda con compresión de caminos
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # Unión por rango
        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False  # ya están conectados

        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True

# =============================
# 3. Implementación de Kruskal (mínimo / máximo)
# =============================
def kruskal(aristas, tipo="min"):
    """
    aristas: lista de tuplas (u, v, peso)
    tipo: "min" para árbol de mínimo coste, "max" para máximo coste
    """
    # Sacar el conjunto de nodos
    nodos = set()
    for u, v, w in aristas:
        nodos.add(u)
        nodos.add(v)

    print("\n====================================")
    if tipo == "min":
        print(" SIMULACIÓN KRUSKAL - ÁRBOL DE MÍNIMO COSTE")
    else:
        print(" SIMULACIÓN KRUSKAL - ÁRBOL DE MÁXIMO COSTE")
    print("====================================\n")

    print("Nodos detectados en el grafo:", nodos)

    # Ordenar aristas
    if tipo == "min":
        aristas_ordenadas = sorted(aristas, key=lambda x: x[2])  # ascendente
    else:
        aristas_ordenadas = sorted(aristas, key=lambda x: x[2], reverse=True)  # descendente

    print("\nAristas ordenadas (u, v, peso):")
    for e in aristas_ordenadas:
        print("  ", e)

    # Inicializar Union-Find
    uf = UnionFind(nodos)
    arbol = []
    coste_total = 0

    print("\nEstado inicial de componentes:")
    print_componentes(uf, nodos)

    # Recorrido de aristas
    for (u, v, w) in aristas_ordenadas:
        print("\n---------------------------------")
        print(f"Probando arista: ({u}, {v}, {w})")
        ru = uf.find(u)
        rv = uf.find(v)
        print(f"  Raíz de {u}: {ru}")
        print(f"  Raíz de {v}: {rv}")

        if ru != rv:
            print("  ✅ No forma ciclo. SE ACEPTA esta arista.")
            uf.union(u, v)
            arbol.append((u, v, w))
            coste_total += w
        else:
            print("  ❌ Forma ciclo. SE RECHAZA esta arista.")

        print("\n  Componentes después de esta arista:")
        print_componentes(uf, nodos)

    print("\n====================================")
    print(" ARISTA(S) SELECCIONADAS EN EL ÁRBOL")
    print("====================================")
    for (u, v, w) in arbol:
        print(f"  ({u}, {v}) con peso {w}")

    print("\nCoste total del árbol:", coste_total)
    print("Número de aristas en el árbol:", len(arbol))
    print("Número de nodos:", len(nodos))

    return arbol, coste_total

def print_componentes(uf, nodos):
    # Construir componentes a partir de las raíces
    comp = {}
    for n in nodos:
        r = uf.find(n)
        if r not in comp:
            comp[r] = []
        comp[r].append(n)

    for i, (raiz, lista) in enumerate(comp.items(), start=1):
        print(f"  Componente {i} (raíz {raiz}): {lista}")

# =============================
# 4. Función para dibujar el grafo y el árbol
# =============================
def dibujar_grafo(aristas, arbol, titulo):
    if not HAY_GRAFICOS:
        print("\n[AVISO] No se encontraron 'networkx' o 'matplotlib'.")
        print("        Instálalos si quieres los gráficos: pip install networkx matplotlib")
        return

    # Crear grafo completo
    G = nx.Graph()
    for (u, v, w) in aristas:
        G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)  # layout bonito

    pesos = nx.get_edge_attributes(G, 'weight')

    plt.figure()
    plt.title(titulo)

    # Dibujar aristas normales
    nx.draw_networkx_edges(G, pos, width=1)
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Dibujar etiquetas de pesos
    nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, font_size=8)

    # Resaltar aristas del árbol
    if arbol:
        G_tree = nx.Graph()
        for (u, v, w) in arbol:
            G_tree.add_edge(u, v)
        nx.draw_networkx_edges(G_tree, pos, width=3)

    plt.axis("off")
    plt.show()

# =============================
# 5. Entrada de datos: grafo de ejemplo o manual
# =============================
def grafo_ejemplo():
    # Puedes modificar este grafo como quieras
    # Formato: (u, v, peso)
    return [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 5),
        ("B", "D", 10),
        ("C", "D", 3),
        ("C", "E", 4),
        ("D", "E", 11),
        ("D", "F", 2),
        ("E", "F", 1),
    ]

def grafo_manual():
    print("\n=== Captura manual del grafo ===")
    n_aristas = int(input("¿Cuántas aristas tendrá el grafo? "))
    aristas = []
    print("Introduce cada arista como: nodo_origen nodo_destino peso")
    print("Ejemplo: A B 4")
    for i in range(n_aristas):
        linea = input(f"Arista {i+1}: ")
        partes = linea.split()
        if len(partes) != 3:
            print("  Formato incorrecto, vuelve a intentarlo.")
            return grafo_manual()
        u, v, w = partes[0], partes[1], float(partes[2])
        aristas.append((u, v, w))
    return aristas

# =============================
# 6. Menú principal
# =============================
def main():
    print("==============================================")
    print(" SIMULADOR ÁRBOL DE MÍNIMO / MÁXIMO COSTE (KRUSKAL)")
    print("==============================================\n")

    print("¿Cómo quieres definir el grafo?")
    print("  1) Usar grafo de ejemplo")
    print("  2) Capturar grafo manualmente")
    opcion_grafo = input("Elige una opción (1/2): ")

    if opcion_grafo == "1":
        aristas = grafo_ejemplo()
    else:
        aristas = grafo_manual()

    print("\n¿Qué tipo de árbol quieres calcular?")
    print("  1) Árbol de MÍNIMO coste")
    print("  2) Árbol de MÁXIMO coste")
    print("  3) AMBOS")
    opcion_tipo = input("Elige una opción (1/2/3): ")

    if opcion_tipo == "1":
        arbol_min, coste_min = kruskal(aristas, tipo="min")
        dibujar_grafo(aristas, arbol_min, "Árbol de MÍNIMO coste (Kruskal)")
    elif opcion_tipo == "2":
        arbol_max, coste_max = kruskal(aristas, tipo="max")
        dibujar_grafo(aristas, arbol_max, "Árbol de MÁXIMO coste (Kruskal)")
    else:
        # Ambos
        arbol_min, coste_min = kruskal(aristas, tipo="min")
        dibujar_grafo(aristas, arbol_min, "Árbol de MÍNIMO coste (Kruskal)")

        arbol_max, coste_max = kruskal(aristas, tipo="max")
        dibujar_grafo(aristas, arbol_max, "Árbol de MÁXIMO coste (Kruskal)")

if __name__ == "__main__":
    main()
1