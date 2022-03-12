class Node:
    def get_id(self):
        """
        Returns a unique identifier for the node (for example, the name, the hash value of the contents, etc.), used to compare two nodes for equality.
        """
        return ""
    def get_neighbors(self):
        """
        Returns all neighbors of a node, and how to reach them. The result is a list Edge objects, each of which contains 3 attributes: target, cost and name, 
        where target is a Node object, cost is a numeric value representing the distance between the two nodes, and name is a string representing the path taken to the neighbor.
        """
        return []
    def __eq__(self, other):
        return self.get_id() == other.get_id()
        
class Edge:
    """
    Abstraction of a graph edge. Has a target (Node that the edge leads to), a cost (numeric) and a name (string), which can be used to print the edge.
    """
    def __init__(self, target, cost, name):
        self.target = target 
        self.cost = cost
        self.name = name

class GeomNode(Node):
    """
    Representation of a finite graph in which all nodes are kept in memory at all times, and stored in the node's neighbors field.
    """
    def __init__(self, name):
        self.name = name
        self.neighbors = []
    def get_neighbors(self):
        return self.neighbors
    def get_id(self):
        return self.name

class InfNode(Node):
    """
    Infinite graph, in which every node represents an integer, and neighbors are generated on demand. Note that Nodes are not cached, i.e. if you
    request the neighbors of node 1, and the neighbors of node 3, both will contain the node 2, but they will be using two distinct objects. 
    """
    def __init__(self, nr):
        self.nr = nr
    def get_neighbors(self):
        result = [Edge(InfNode(self.nr-1),1,("%d - -1 - %d"%(self.nr,self.nr-1))), Edge(InfNode(self.nr+1),1,("%d - +1 - %d"%(self.nr,self.nr+1))), Edge(InfNode(self.nr*2),1,("%d - *2 - %d"%(self.nr,self.nr*2)))]
        if self.nr%2 == 0:
            result.append(Edge(InfNode(self.nr//2),1,("%d - /2 - %d"%(self.nr,self.nr//2))))
        return result
    def get_id(self):
        return self.nr


def make_geom_graph(nodes, edges):
    """
    Given a list of nodes and edges (with distances), creates a dictionary of Node objects 
    representing the graph. Note that the resulting graph is directed, but each edge will be 
    replaced with *two* directed edges (to and from).
    """
    result = {}
    for c in nodes:
        result[c] = GeomNode(c)
    for (a,b,d) in edges:
        result[a].neighbors.append(Edge(result[b], d, "%s - %s"%(a,b)))
        result[b].neighbors.append(Edge(result[a], d, "%s - %s"%(b,a)))
    return result
    
Austria = make_geom_graph(
    ["Graz", "Vienna", "Salzburg", "Innsbruck", "Munich", "Bregenz", "Linz", "Eisenstadt", "Klagenfurt", "Lienz", "Bruck"],
    [("Graz", "Bruck", 55.0),
     ("Graz", "Klagenfurt", 136.0),
     ("Graz", "Vienna", 200.0),
     ("Graz", "Eisenstadt", 173.0),
     ("Bruck", "Klagenfurt", 152.0),
     ("Bruck", "Salzburg", 215.0),
     ("Bruck", "Linz", 195.0),
     ("Bruck", "Vienna", 150.0),
     ("Vienna", "Eisenstadt", 60.0),
     ("Vienna", "Linz", 184.0),
     ("Linz", "Salzburg", 123.0),
     ("Salzburg", "Munich", 145.0),
     ("Salzburg", "Klagenfurt", 223.0),
     ("Klagenfurt", "Lienz", 145.0),
     ("Lienz", "Innsbruck", 180.0),
     ("Munich", "Innsbruck", 151.0),
     ("Munich", "Bregenz", 180.0),
     ("Innsbruck", "Bregenz", 190.0)])
     
AustriaHeuristic = { 
   "Graz":       {"Graz": 0.0,   "Vienna": 180.0, "Eisenstadt": 150.0, "Bruck": 50.0,  "Linz": 225.0, "Salzburg": 250.0, "Klagenfurt": 125.0, "Lienz": 270.0, "Innsbruck": 435.0, "Munich": 375.0, "Bregenz": 450.0},
   "Vienna":     {"Graz": 180.0, "Vienna": 0.0,   "Eisenstadt": 50.0,  "Bruck": 126.0, "Linz": 175.0, "Salzburg": 285.0, "Klagenfurt": 295.0, "Lienz": 400.0, "Innsbruck": 525.0, "Munich": 407.0, "Bregenz": 593.0},
   "Eisenstadt": {"Graz": 150.0, "Vienna": 50.0,  "Eisenstadt": 0.0,   "Bruck": 171.0, "Linz": 221.0, "Salzburg": 328.0, "Klagenfurt": 335.0, "Lienz": 437.0, "Innsbruck": 569.0, "Munich": 446.0, "Bregenz": 630.0},
   "Bruck":      {"Graz": 50.0,  "Vienna": 126.0, "Eisenstadt": 171.0, "Bruck": 0.0,   "Linz": 175.0, "Salzburg": 201.0, "Klagenfurt": 146.0, "Lienz": 287.0, "Innsbruck": 479.0, "Munich": 339.0, "Bregenz": 521.0},
   "Linz":       {"Graz": 225.0, "Vienna": 175.0, "Eisenstadt": 221.0, "Bruck": 175.0, "Linz": 0.0,   "Salzburg": 117.0, "Klagenfurt": 311.0, "Lienz": 443.0, "Innsbruck": 378.0, "Munich": 265.0, "Bregenz": 456.0},
   "Salzburg":   {"Graz": 250.0, "Vienna": 285.0, "Eisenstadt": 328.0, "Bruck": 201.0, "Linz": 117.0, "Salzburg": 0.0,   "Klagenfurt": 201.0, "Lienz": 321.0, "Innsbruck": 265.0, "Munich": 132.0, "Bregenz": 301.0},
   "Klagenfurt": {"Graz": 125.0, "Vienna": 295.0, "Eisenstadt": 335.0, "Bruck": 146.0, "Linz": 311.0, "Salzburg": 201.0, "Klagenfurt": 0.0,   "Lienz": 132.0, "Innsbruck": 301.0, "Munich": 443.0, "Bregenz": 465.0},
   "Lienz":      {"Graz": 270.0, "Vienna": 400.0, "Eisenstadt": 437.0, "Bruck": 287.0, "Linz": 443.0, "Salzburg": 321.0, "Klagenfurt": 132.0, "Lienz": 0.0,   "Innsbruck": 157.0, "Munich": 298.0, "Bregenz": 332.0},
   "Innsbruck":  {"Graz": 435.0, "Vienna": 525.0, "Eisenstadt": 569.0, "Bruck": 479.0, "Linz": 378.0, "Salzburg": 265.0, "Klagenfurt": 301.0, "Lienz": 157.0, "Innsbruck": 0.0,   "Munich": 143.0, "Bregenz": 187.0},
   "Munich":     {"Graz": 375.0, "Vienna": 407.0, "Eisenstadt": 446.0, "Bruck": 339.0, "Linz": 265.0, "Salzburg": 132.0, "Klagenfurt": 443.0, "Lienz": 298.0, "Innsbruck": 143.0, "Munich": 0.0,   "Bregenz": 165.0},
   "Bregenz":    {"Graz": 450.0, "Vienna": 593.0, "Eisenstadt": 630.0, "Bruck": 521.0, "Linz": 456.0, "Salzburg": 301.0, "Klagenfurt": 465.0, "Lienz": 332.0, "Innsbruck": 187.0, "Munich": 165.0, "Bregenz": 0.0}}

VirgoConstellation = make_geom_graph( 
  ["109Virginis", "RijilAlAwwa", "KappaVirginis","TauVirginis", "Syrma", "Heze", "Porrima", "Minelauva", "Vindemiatrix", "Caphir", "Spica", "Zaniah", "Zavijava", "NuVirginis", "OmnicronVirginis"],
  [("109Virginis", "TauVirginis", 80.0),
    ("TauVirginis", "Heze", 131.0),
    ("TauVirginis", "Syrma", 113.0),
    ("RijilAlAwwa", "Syrma", 30.0),
    ("Syrma", "KappaVirginis", 146.0),
    ("KappaVirginis", "Spica", 5.0),
    ("Heze", "Vindemiatrix", 33.0),
    ("Heze", "Spica", 169.0),
    ("Heze", "Minelauva", 113.0),
    ("Spica", "Caphir", 139.0),
    ("Caphir", "Porrima", 339.0),
    ("Minelauva", "Vindemiatrix", 79.0),
    ("Minelauva", "Porrima", 144.0),
    ("Porrima", "OmnicronVirginis", 113.0),
    ("Porrima", "Zaniah", 203.0),
    ("Zaniah", "Zavijava", 205.0),
    ("Zavijava", "NuVirginis", 232.0),
    ("NuVirginis", "OmnicronVirginis", 118.0)])

VirgoHeuristic = {
"109Virginis": {"109Virginis": 0.0, "RijilAlAwwa": 69.0, "KappaVirginis": 126.0, "TauVirginis": 89.0, "Syrma": 36.0, "Heze": 56.0, "Porrima": 91.0, "Minelauva": 69.0, "Vindemiatrix": 19.0, "Caphir": 286.0, "Spica": 132.0, "Zaniah": 135.0, "Zavijava": 93.0, "NuVirginis": 165.0, "OmnicronVirginis": 34.0},
"RijilAlAwwa": {"109Virginis": 69.0, "RijilAlAwwa": 0.0, "KappaVirginis": 195.0, "TauVirginis": 158.0, "Syrma": 33.0, "Heze": 13.0, "Porrima": 22.0, "Minelauva": 138.0, "Vindemiatrix": 50.0, "Caphir": 355.0, "Spica": 201.0, "Zaniah": 204.0, "Zavijava": 24.0, "NuVirginis": 234.0, "OmnicronVirginis": 103.0},
"KappaVirginis": {"109Virginis": 126.0, "RijilAlAwwa": 195.0, "KappaVirginis": 0.0, "TauVirginis": 37.0, "Syrma": 162.0, "Heze": 182.0, "Porrima": 217.0, "Minelauva": 57.0, "Vindemiatrix": 145.0, "Caphir": 160.0, "Spica": 6.0, "Zaniah": 9.0, "Zavijava": 219.0, "NuVirginis": 39.0, "OmnicronVirginis": 92.0},
"TauVirginis": {"109Virginis": 89.0, "RijilAlAwwa": 158.0, "KappaVirginis": 37.0, "TauVirginis": 0.0, "Syrma": 125.0, "Heze": 145.0, "Porrima": 180.0, "Minelauva": 20.0, "Vindemiatrix": 108.0, "Caphir": 197.0, "Spica": 43.0, "Zaniah": 46.0, "Zavijava": 182.0, "NuVirginis": 76.0, "OmnicronVirginis": 55.0},
"Syrma": {"109Virginis": 36.0, "RijilAlAwwa": 33.0, "KappaVirginis": 162.0, "TauVirginis": 125.0, "Syrma": 0.0, "Heze": 20.0, "Porrima": 55.0, "Minelauva": 105.0, "Vindemiatrix": 17.0, "Caphir": 322.0, "Spica": 168.0, "Zaniah": 171.0, "Zavijava": 57.0, "NuVirginis": 201.0, "OmnicronVirginis": 70.0},
"Heze": {"109Virginis": 56.0, "RijilAlAwwa": 13.0, "KappaVirginis": 182.0, "TauVirginis": 145.0, "Syrma": 20.0, "Heze": 0.0, "Porrima": 35.0, "Minelauva": 125.0, "Vindemiatrix": 37.0, "Caphir": 342.0, "Spica": 188.0, "Zaniah": 191.0, "Zavijava": 37.0, "NuVirginis": 221.0, "OmnicronVirginis": 90.0},
"Porrima": {"109Virginis": 91.0, "RijilAlAwwa": 22.0, "KappaVirginis": 217.0, "TauVirginis": 180.0, "Syrma": 55.0, "Heze": 35.0, "Porrima": 0.0, "Minelauva": 160.0, "Vindemiatrix": 72.0, "Caphir": 377.0, "Spica": 223.0, "Zaniah": 226.0, "Zavijava": 2.0, "NuVirginis": 256.0, "OmnicronVirginis": 125.0},
"Minelauva": {"109Virginis": 69.0, "RijilAlAwwa": 138.0, "KappaVirginis": 57.0, "TauVirginis": 20.0, "Syrma": 105.0, "Heze": 125.0, "Porrima": 160.0, "Minelauva": 0.0, "Vindemiatrix": 88.0, "Caphir": 217.0, "Spica": 63.0, "Zaniah": 66.0, "Zavijava": 162.0, "NuVirginis": 96.0, "OmnicronVirginis": 35.0},
"Vindemiatrix": {"109Virginis": 19.0, "RijilAlAwwa": 50.0, "KappaVirginis": 145.0, "TauVirginis": 108.0, "Syrma": 17.0, "Heze": 37.0, "Porrima": 72.0, "Minelauva": 88.0, "Vindemiatrix": 0.0, "Caphir": 305.0, "Spica": 151.0, "Zaniah": 154.0, "Zavijava": 74.0, "NuVirginis": 184.0, "OmnicronVirginis": 53.0},
"Caphir": {"109Virginis": 286.0, "RijilAlAwwa": 355.0, "KappaVirginis": 160.0, "TauVirginis": 197.0, "Syrma": 322.0, "Heze": 342.0, "Porrima": 377.0, "Minelauva": 217.0, "Vindemiatrix": 305.0, "Caphir": 0.0, "Spica": 154.0, "Zaniah": 151.0, "Zavijava": 379.0, "NuVirginis": 121.0, "OmnicronVirginis": 252.0},
"Spica": {"109Virginis": 132.0, "RijilAlAwwa": 201.0, "KappaVirginis": 6.0, "TauVirginis": 43.0, "Syrma": 168.0, "Heze": 188.0, "Porrima": 223.0, "Minelauva": 63.0, "Vindemiatrix": 151.0, "Caphir": 154.0, "Spica": 0.0, "Zaniah": 3.0, "Zavijava": 225.0, "NuVirginis": 33.0, "OmnicronVirginis": 98.0},
"Zaniah": {"109Virginis": 135.0, "RijilAlAwwa": 204.0, "KappaVirginis": 9.0, "TauVirginis": 46.0, "Syrma": 171.0, "Heze": 191.0, "Porrima": 226.0, "Minelauva": 66.0, "Vindemiatrix": 154.0, "Caphir": 151.0, "Spica": 3.0, "Zaniah": 0.0, "Zavijava": 228.0, "NuVirginis": 30.0, "OmnicronVirginis": 101.0},
"Zavijava": {"109Virginis": 93.0, "RijilAlAwwa": 24.0, "KappaVirginis": 219.0, "TauVirginis": 182.0, "Syrma": 57.0, "Heze": 37.0, "Porrima": 2.0, "Minelauva": 162.0, "Vindemiatrix": 74.0, "Caphir": 379.0, "Spica": 225.0, "Zaniah": 228.0, "Zavijava": 0.0, "NuVirginis": 258.0, "OmnicronVirginis": 127.0},
"NuVirginis": {"109Virginis": 165.0, "RijilAlAwwa": 234.0, "KappaVirginis": 39.0, "TauVirginis": 76.0, "Syrma": 201.0, "Heze": 221.0, "Porrima": 256.0, "Minelauva": 96.0, "Vindemiatrix": 184.0, "Caphir": 121.0, "Spica": 33.0, "Zaniah": 30.0, "Zavijava": 258.0, "NuVirginis": 0.0, "OmnicronVirginis": 131.0},
"OmnicronVirginis": {"109Virginis": 34.0, "RijilAlAwwa": 103.0, "KappaVirginis": 92.0, "TauVirginis": 55.0, "Syrma": 70.0, "Heze": 90.0, "Porrima": 125.0, "Minelauva": 35.0, "Vindemiatrix": 53.0, "Caphir": 252.0, "Spica": 98.0, "Zaniah": 101.0, "Zavijava": 127.0, "NuVirginis": 131.0, "OmnicronVirginis": 0.0}
}



