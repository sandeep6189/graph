import csv
import time

def make_link(G,node1,node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2]= {}
    (G[node2])[node1] = 1
    return G

connections = [('a','g'),('b','h'),('a','d'),('d','g'),('c','g'),('b','c'),('f','e'),('f','q'),('q','b')]

G ={}
for (x,y) in connections: make_link(G,x,y)
print G #gives me the graph which tells me how nodes are connected to what

#Traversal ...

def mark_component(G,node,marked):
    marked[node] = True
    total_marked = 1
    for neighbor in G[node]:
        if neighbor not in marked:
            total_marked +=mark_component(G,neighbor,marked)
    return total_marked

def list_component_sizes(G):
    marked = {}
    for node in G.keys():
        if node not in marked:
            print "Component containing",node,": ",mark_component(G,node,marked)
    print marked
#list_component_sizes(G)

def read_graph(filename):
    #read an undirected graph in csv
    tsv = csv.reader(open(filename),delimiter='\t')
    G = {}
    for (node1,node2) in tsv: make)_link(G,node1,node2)
    return G

#read the marvel comics graph
marvelG = read_graph("uniq_edges.tsv")

def path(G,v1,v2):
    distance_frm_start = {}
    open_list = [v1]
    #to get the path 
    distance_frm_start[v1] = [v1]
    while len(open_list)>0:
        current = open_list[0]
        del open_list[0]
        for neighbor in G[current].keys():
            if neighbor not in distance_frm_start:
                distance_frm_start[neighbor]=distance_frm_start[current] + [neighbor]
                if neighbor == v2: return distance_frm_start[v2]
                open_list.append(neighbor)
    return False

def centrality(G,v):
    distance_from_start = {}
    open_list = [v]
    distance_from_start[v] = 0
    while len(open_list)>0:
        current = open_list[0]
        del open_list[0]
        for neighbor in G[current].keys():
            if neighbor not in distance_from_start:
                distance_from_start[neighbor] = distance_from_start[current] + 1
                open_list.append(neighbor)
    return (sum(distance_from_start.values()+0.0)/len(distance_from_start))
                

def make_link(G, node1, node2, r_or_g):
    # modified make_link to apply
    # a color to the edge instead of just 1
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = r_or_g
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = r_or_g
    return G

def get_children(S, root, parent):
    """returns the children from following the
    green edges"""
    return [n for n, e in S[root].items()
            if ((not n == parent) and
                (e == 'green'))]

def get_children_all(S, root, parent):
    """returns the children from following
    green edges and the children from following
    red edges"""
    green = []
    red = []
    for n, e in S[root].items():
        if n == parent:
            continue
        if e == 'green':
            green.append(n)
        if e == 'red':
            red.append(n)
    return green, red

#################

def create_rooted_spanning_tree(G, root):
    # use DFS from the root to add edges and nodes
    # to the tree.  The first time we see a node
    # the edge is green, but after that its red
    open_list = [root]
    S = {root:{}}
    while len(open_list) > 0:
        node = open_list.pop()
        neighbors = G[node]
        for n in neighbors:
            if n not in S:
                # we haven't seen this node, so
                # need to use a green edge to connect
                # it
                make_link(S, node, n, 'green')
                open_list.append(n)
            else:
                # we have seen this node,
                # but, first make sure that 
                # don't already have the edge
                # in S
                if node not in S[n]:
                    make_link(S, node, n, 'red')
    return S

##################

def _post_order(S, root, parent, val, po):
    children = get_children(S, root, parent)    
    for c in children:
        val = _post_order(S, c, root, val, po)
    po[root] = val
    return val + 1

def post_order(S, root):
    po = {}
    _post_order(S, root, None, 1, po)
    return po


##################

def _number_descendants(S, root, parent, nd):
    # number of descendants is the 
    # sum of the number of descendants of a nodes
    # children plus one
    children = get_children(S, root, parent)
    nd_val = 1
    for c in children:
        # recursively calculate the number of descendants
        # for the children
        nd_val += _number_descendants(S, c, root, nd)
    nd[root] = nd_val
    return nd_val

def number_of_descendants(S, root):
    nd = {}
    _number_descendants(S, root, None, nd)
    return nd
