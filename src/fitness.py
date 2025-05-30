def fitness(pi, dist_matrix):
    """
    
    pi: list of city indices [0..n-1]
    dist_matrix: 2D list of distances (output of compute_dist_matrix)
    returns: total tour length (float)
    
    """

    total = 0.0
    n = len(pi)
    for i in range(n - 1):
        total += dist_matrix[pi[i]][pi[i+1]]

    total += dist_matrix[pi[-1]][pi[0]]
    return total


