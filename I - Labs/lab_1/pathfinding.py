import graph
import queue

PARENT = 0
EDGE = 1
MAX_DEPTH = 13

def default_heuristic(n):
    """
    Default heuristic for A*. Do not change, rename or remove!
    """
    return 0

def visited(node, visited_nodes):
    return node.get_id() in visited_nodes

def get_path_and_distance(visited_nodes, start, goal):
    path = []
    distance = 0
    parent_id = 0
    target_id = goal.get_id()
    current_edge = None
    
    while True:
        parent_id = visited_nodes[target_id][PARENT]
        current_edge = visited_nodes[target_id][EDGE]
        path.append(current_edge)
        distance += current_edge.cost
        if parent_id == start.get_id() :
            return path, distance
        else:
            target_id = parent_id

def bfs(start, goal):
    """
    Breadth-First search algorithm. The function is passed a start graph.Node object and a goal predicate.
    
    The start node can produce neighbors as needed, see graph.py for details.
    
    The goal is represented as a function, that is passed a node, and returns True if that node is a goal node, otherwise False. 
    
    The function should return a 4-tuple (path,distance,visited,expanded):
        - path is a sequence of graph.Edge objects that have to be traversed to reach a goal state from the start
        - distance is the sum of costs of all edges in the path 
        - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
        - expanded is the total number of nodes that were expanded, i.e. removed from the frontier to add their neighbors
    """  
    # Inicializacion de la frontera con el nodo inicial.
    frontier = queue.Queue()
    frontier.put(start)
    
    # Inicialización del diccionario de nodos visitados. 
    # Llave: Id del nodo visitado. 
    # Valor: Tupla que contiene en [0] Id del nodo de origen y en [1] la arista a través de las cual se visitó dicho nodo.
    visited_nodes = {}
    visited_nodes[start.get_id()] = None

    # Numero de nodos expandidos.
    expanded_nodes_count = 0
    
    # Ultimo nodo visitado.
    last_node_visited = start

    while not goal(last_node_visited):
       last_node_visited = expand_node_bfs(frontier, visited_nodes, goal)
       expanded_nodes_count = expanded_nodes_count + 1
    
    path, distance = get_path_and_distance(visited_nodes, start, last_node_visited)
    path.reverse()

    return path, distance, len(visited_nodes), expanded_nodes_count

def expand_node_bfs(frontier, visited_nodes, goal):
    node_to_expand = frontier.get()
    neighborhood = node_to_expand.get_neighbors()
    
    for edge in neighborhood:
       node_to_visite = edge.target
       if not visited(node_to_visite, visited_nodes):
           frontier.put(node_to_visite)
           visited_nodes[node_to_visite.get_id()] = [node_to_expand.get_id(), edge]
           if goal(node_to_visite): # Para evitar seguir visitando los nodos vecinos cuando ya se tiene el objetivo en la frontera.
                return node_to_visite
    return node_to_visite

    
def dfs(start, goal):
    """
    Depth-First search algorithm. The function is passed a start graph.Node object, a heuristic function, and a goal predicate.
    
    The start node can produce neighbors as needed, see graph.py for details.
    
    The goal is represented as a function, that is passed a node, and returns True if that node is a goal node, otherwise False. 
    
    The function should return a 4-tuple (path,distance,visited,expanded):
        - path is a sequence of graph.Edge objects that have to be traversed to reach a goal state from the start
        - distance is the sum of costs of all edges in the path 
        - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
        - expanded is the total number of nodes that were expanded, i.e. removed from the frontier to add their neighbors
    """
     # Inicializacion de la frontera con el nodo inicial.
    frontier = queue.LifoQueue()
    frontier.put(start)
    
    # Inicialización del diccionario de nodos visitados. 
    # Llave: Id del nodo visitado. 
    # Valor: Tupla que contiene en [0] Id del nodo de origen y en [1] la arista a través de las cual se visitó dicho nodo.
    visited_nodes = {}
    visited_nodes[start.get_id()] = None

    # Inicialización del diccionario de profundidad de los nodos.
    # Llave: Id del nodo. 
    # Valor: Pronfundidad del nodo asociado.
    # Se utiliza más que todo para los grafos infinitos, para establecer un tope de profundidad de búsqueda y si no desviarse por otra dirección.
    depth_of = {}
    depth_of[start.get_id()] = 0

    # Numero de nodos expandidos.
    expanded_nodes_count = 0
    
    # Ultimo nodo visitado.
    last_node_visited = start

    while not goal(last_node_visited):
       last_node_visited = expand_node_dfs(frontier, visited_nodes, goal, depth_of)
       expanded_nodes_count = expanded_nodes_count + 1
    
    path, distance = get_path_and_distance(visited_nodes, start, last_node_visited)
    path.reverse()

    return path, distance, len(visited_nodes), expanded_nodes_count


def expand_node_dfs(frontier, visited_nodes, goal, depth_of):
    node_to_expand = frontier.get()
    neighborhood = node_to_expand.get_neighbors()
    set_depth_of(neighborhood, node_to_expand.get_id(), depth_of)
   
    if depth_of[node_to_expand.get_id()] <= MAX_DEPTH:
        for edge in neighborhood:
           node_to_visite = edge.target
           if not visited(node_to_visite, visited_nodes):
               frontier.put(node_to_visite)
               visited_nodes[node_to_visite.get_id()] = [node_to_expand.get_id(), edge]
               if goal(node_to_visite):
                    return node_to_visite

    return node_to_expand

def set_depth_of(neighborhood, parent_id, depth_of):
    neighborhood_depth = depth_of[parent_id] + 1 
    for edge in neighborhood:
        node_id = edge.target.get_id() 
        depth_of[node_id] = neighborhood_depth


def greedy(start, heuristic, goal):
    """
    Greedy search algorithm. The function is passed a start graph.Node object, a heuristic function, and a goal predicate.
    
    The start node can produce neighbors as needed, see graph.py for details.
    
    The heuristic is a function that takes a node as a parameter and returns an estimate for how far that node is from the goal.    
    
    The goal is also represented as a function, that is passed a node, and returns True if that node is a goal node, otherwise False. 
    
    The function should return a 4-tuple (path,distance,visited,expanded):
        - path is a sequence of graph.Edge objects that have to be traversed to reach a goal state from the start
        - distance is the sum of costs of all edges in the path 
        - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
        - expanded is the total number of nodes that were expanded, i.e. removed from the frontier to add their neighbors
    """
    # Inicializacion de la frontera con el nodo inicial.
    # La cantidad de nodos visitados se incluye como segundo campo de la tupla para que la cola tenga un segundo criterio de priorización en los casos que habían dos nodos con misma prioridad, de lo contrario daba errores, porque no sabía 
    # comparar objetos de tipo GeomNode.
    frontier = queue.PriorityQueue()
    frontier.put( (heuristic(start), 0, start) ) 
    
    # Inicialización del diccionario de nodos visitados. 
    # Llave: Id del nodo visitado. 
    # Valor: Tupla que contiene en [0] Id del nodo de origen y en [1] la arista a través de las cual se visitó dicho nodo.
    visited_nodes = {}
    visited_nodes[start.get_id()] = None

    # Numero de nodos expandidos.
    expanded_nodes_count = 0
    
    # Ultimo nodo visitado.
    last_node_visited = start

    while not goal(last_node_visited):
       last_node_visited = expand_node_greedy(frontier, visited_nodes, goal, heuristic)
       expanded_nodes_count = expanded_nodes_count + 1
    
    path, distance = get_path_and_distance(visited_nodes, start, last_node_visited)
    path.reverse()

    return path, distance, len(visited_nodes), expanded_nodes_count

def expand_node_greedy(frontier, visited_nodes, goal, heuristic):
    node_to_expand = frontier.get()[2]
    neighborhood = node_to_expand.get_neighbors()
    for edge in neighborhood:
       node_to_visite = edge.target
       if not visited(node_to_visite, visited_nodes):
           frontier.put( (heuristic(node_to_visite), len(visited_nodes), node_to_visite) )
           visited_nodes[node_to_visite.get_id()] = [node_to_expand.get_id(), edge]
           if goal(node_to_visite):
                return node_to_visite
    return node_to_visite

def astar(start, heuristic, goal):
    """
    A* search algorithm. The function is passed a start graph.Node object, a heuristic function, and a goal predicate.
    
    The start node can produce neighbors as needed, see graph.py for details.
    
    The heuristic is a function that takes a node as a parameter and returns an estimate for how far that node is from the goal.    
    
    The goal is also represented as a function, that is passed a node, and returns True if that node is a goal node, otherwise False. 
    
    The function should return a 4-tuple (path,distance,visited,expanded):
        - path is a sequence of graph.Edge objects that have to be traversed to reach a goal state from the start
        - distance is the sum of costs of all edges in the path 
        - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
        - expanded is the total number of nodes that were expanded, i.e. removed from the frontier to add their neighbors
    """
    
    # Inicialización del diccionario de nodos visitados. 
    # Llave: Id del nodo visitado. 
    # Valor: Tupla que contiene en [0] Id del nodo de origen y en [1] la arista a través de las cual se visitó dicho nodo.
    visited_nodes = {}
    visited_nodes[start.get_id()] = None

    # Inicialización del diccionario de distancias respecto al nodo de inicio. 
    # Llave: Id del nodo destino.
    # Valor: Distancia entre el  nodo de inicio y el nodo destino.
    distance_from_start = {}
    distance_from_start[start.get_id()] = 0

    # Inicializacion de la frontera con el nodo inicial.
    # La cantidad de nodos visitados se incluye como segundo campo de la tupla para que la cola tenga un segundo criterio de priorización en los casos que habían dos nodos con misma prioridad, de lo contrario daba errores, porque no sabía 
    # comparar objetos de tipo GeomNode.
    frontier = queue.PriorityQueue()
    frontier.put( (heuristic(start) + distance_from_start[start.get_id()], 0, start) )

    # Numero de nodos expandidos.
    expanded_nodes_count = 0
    
    # Ultimo nodo visitado.
    last_node_visited = start

    while not goal(last_node_visited):
       last_node_visited = expand_node_astar(frontier, visited_nodes, goal, heuristic, distance_from_start)
       expanded_nodes_count = expanded_nodes_count + 1
    
    path, distance = get_path_and_distance(visited_nodes, start, last_node_visited)
    path.reverse()

    return path, distance, len(visited_nodes), expanded_nodes_count

def expand_node_astar(frontier, visited_nodes, goal, heuristic, distance_from_start):
    node_to_expand = frontier.get()[2]
    neighborhood = node_to_expand.get_neighbors()
    if goal(node_to_expand) :  # El algoritmo termina hasta que el nodo objetivo sea la primera entrega de la frontera.
        return node_to_expand
    
    for edge in neighborhood:
       node_to_visite = edge.target
       if not visited(node_to_visite, visited_nodes):
           distance_from_start[node_to_visite.get_id()] = distance_from_start[node_to_expand.get_id()] +  edge.cost
           frontier.put( (heuristic(node_to_visite) + distance_from_start[node_to_visite.get_id()] , len(visited_nodes), node_to_visite) )
           visited_nodes[node_to_visite.get_id()] = [node_to_expand.get_id(), edge]
          
    return node_to_visite

def run_all(name, start, heuristic, goal):
    print("running test", name)
    print("Breadth-First Search")
    result = bfs(start, goal)
    print_path(result)
    
    print("\nDepth-First Search")
    result = dfs(start, goal)
    print_path(result)
    
    print("\nGreedy Search (default heuristic)")
    result = greedy(start, default_heuristic, goal)
    print_path(result)
    
    print("\nGreedy Search")
    result = greedy(start, heuristic, goal)
    print_path(result)
    
    print("\nA* Search (default heuristic)")
    result = astar(start, default_heuristic, goal)
    print_path(result)
    
    print("\nA* Search")
    result = astar(start, heuristic, goal)
    print_path(result)
    
    print("\n\n")

def print_path(result):
    (path,cost,visited_cnt,expanded_cnt) = result
    print("visited nodes:", visited_cnt, "expanded nodes:",expanded_cnt)
    if path:
        print("Path found with cost", cost)
        for n in path:
            print(n.name)
    else:
        print("No path found")
    print("\n")

def main():
    """
    You are free (and encouraged) to change this function to add more test cases.
    
    You are provided with three test cases:
        - pathfinding in Austria, using the map shown in class. This is a relatively small graph, but it comes with an admissible heuristic. Below astar is called using that heuristic, 
          as well as with the default heuristic (which always returns 0). If you implement A* correctly, you should see a small difference in the number of visited/expanded nodes between the two heuristics.
        - pathfinding on an infinite graph, where each node corresponds to a natural number, which is connected to its predecessor, successor and twice its value, as well as half its value, if the number is even.
          e.g. 16 is connected to 15, 17, 32, and 8. The problem given is to find a path from 1 to 2050, for example by doubling the number until 2048 is reached and then adding 1 twice. There is also a heuristic 
          provided for this problem, but it is not admissible (think about why), but it should result in a path being found almost instantaneously. On the other hand, if the default heuristic is used, the search process 
          will take a noticeable amount (a couple of seconds).
        - pathfinding on the same infinite graph, but with infinitely many goal nodes. Each node corresponding to a number greater 1000 that is congruent to 63 mod 123 is a valid goal node. As before, a non-admissible
          heuristic is provided, which greatly accelerates the search process. 
    """
    target = "Bregenz"
    def atheuristic(n):
        return graph.AustriaHeuristic[target][n.get_id()]
    def atgoal(n):
        return n.get_id() == target

    run_all("Austria", graph.Austria["Eisenstadt"], atheuristic, atgoal)
    
    
    target = 2050
    def infheuristic(n):
        return abs(n.get_id() - target)
    def infgoal(n):
       return n.get_id() == target
    
    run_all("Infinite Graph (simple)", graph.InfNode(1), infheuristic, infgoal)
    

    def multiheuristic(n):
        return abs(n.get_id()%123 - 63)
    def multigoal(n):
        return n.get_id() > 1000 and n.get_id()%123 == 63
    
    run_all("Infinite Graph (simple)", graph.InfNode(1), multiheuristic, multigoal)

    target = "KappaVirginis"
    def virgoHeuristic(n):
        return graph.VirgoHeuristic[target][n.get_id()]

    run_all("NuVirginis",graph.VirgoConstellation["NuVirginis"], virgoHeuristic, atgoal)

if __name__ == "__main__":
    main()