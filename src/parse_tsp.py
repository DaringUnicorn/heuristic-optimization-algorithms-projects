import math

def load_custom_tsp(filename):
    """
    
    First line = number of cities n.
    Next n lines = coordinates of cities (x, y) as floats.
    
    """
    with open(filename) as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    coords = [tuple(map(float, line.split())) for line in lines[1 : n + 1]]
    return coords

def compute_dist_matrix(coords):
    """

    coords: list of (x, y)    
    returns n x n Euclidean distance matrix. 

    """

    n = len(coords)
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            D[i][j] = math.hypot(dx, dy)
    return D
    

