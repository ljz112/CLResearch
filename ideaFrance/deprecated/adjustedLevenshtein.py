# just reusing my CL code lol

# make the del/ins/sub functions you know what to do  

def sub_cost(s, t):
    if s != t:
        if s == "'":
            return 0.5
        return 1
    return 0

def edit_dist(source, target):
    n = len(source)
    m = len(target)
    D = [[-1 for j in range(m + 1)] for i in range(n + 1)]
    D[0][0] = 0
    for i in range(n):
        D[i + 1][0] = D[i][0] + 1
    for j in range(m):
        D[0][j + 1] = D[0][j] + 1
    # recurrence relation
    for i in range(n):
        for j in range(m):
            D[i+1][j+1] = min(D[i+1][j] + 1, D[i][j+1] + 1, D[i][j] + sub_cost(source[i], target[j]))

    return D[n][m]

print(edit_dist("poppin'", "popping"))