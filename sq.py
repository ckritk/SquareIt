moves = [(4, 4), (4, 5), (5, 4), (5, 5), (3, 4), (3, 5), (4, 3), (4, 6), (5, 3), (5, 6),
 (6, 4), (6, 5), (3, 3), (3, 6), (6, 3), (6, 6), (2, 4), (2, 5), (4, 2), (4, 7),
 (5, 2), (5, 7), (7, 4), (7, 5), (2, 3), (2, 6), (3, 2), (3, 7), (6, 2), (6, 7),
 (7, 3), (7, 6), (1, 4), (1, 5), (2, 2), (2, 7), (4, 1), (4, 8), (5, 1), (5, 8),
 (7, 2), (7, 7), (8, 4), (8, 5), (1, 3), (1, 6), (3, 1), (3, 8), (6, 1), (6, 8),
 (8, 3), (8, 6), (1, 2), (1, 7), (2, 1), (2, 8), (7, 1), (7, 8), (8, 2), (8, 7),
 (0, 4), (0, 5), (4, 0), (4, 9), (5, 0), (5, 9), (9, 4), (9, 5), (0, 3), (0, 6),
 (3, 0), (3, 9), (6, 0), (6, 9), (9, 3), (9, 6), (1, 1), (1, 8), (8, 1), (8, 8),
 (0, 2), (0, 7), (2, 0), (2, 9), (7, 0), (7, 9), (9, 2), (9, 7), (0, 1), (0, 8),
 (1, 0), (1, 9), (8, 0), (8, 9), (9, 1), (9, 8), (0, 0), (0, 9), (9, 0), (9, 9)]

SIZE = 10
WEIGHTS = [[0 for i in range(SIZE)] for j in range(SIZE)]

import itertools
import math

def count_4pt_squares(grid, target_value):
    n = len(grid)
    count = 0

    target_points = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == target_value]
    
    def is_square(p1, p2, p3, p4):
        dists = sorted([dist(p1, p2), dist(p1, p3), dist(p1, p4), 
                        dist(p2, p3), dist(p2, p4), dist(p3, p4)])
        return dists[0] == dists[1] == dists[2] == dists[3] > 0 and dists[4] == dists[5]

    def dist(p1, p2):
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    for p1, p2, p3, p4 in itertools.combinations(target_points, 4):
        if is_square(p1, p2, p3, p4):
            count += 1

    return count


def count_3pt_squares(grid, target_value):
    n = len(grid)
    count = 0

    target_points = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == target_value]
    zero_points = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == 0]

    def is_square(p1, p2, p3, p4):
        dists = sorted([dist(p1, p2), dist(p1, p3), dist(p1, p4), 
                        dist(p2, p3), dist(p2, p4), dist(p3, p4)])
        return dists[0] == dists[1] == dists[2] == dists[3] > 0 and dists[4] == dists[5]

    def dist(p1, p2):
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    for zero_point in zero_points:
        for p1, p2, p3 in itertools.combinations(target_points, 3):
            if is_square(zero_point, p1, p2, p3):
                count += 1

    return count

def find_3pt_square_zeros_with_given_pt(grid, target_value, given_point):
    n = len(grid)
    zero_in_squares = []

    target_points = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == target_value and (i, j) != given_point]
    zero_points = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == 0]

    def is_square(p1, p2, p3, p4):
        dists = sorted([dist(p1, p2), dist(p1, p3), dist(p1, p4), 
                        dist(p2, p3), dist(p2, p4), dist(p3, p4)])
        return dists[0] == dists[1] == dists[2] == dists[3] > 0 and dists[4] == dists[5]

    def dist(p1, p2):
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    for zero_point in zero_points:
        for p1, p2 in itertools.combinations(target_points, 2):
            if is_square(zero_point, given_point, p1, p2):
                zero_in_squares.append(zero_point)
                break  

    return zero_in_squares

def find_2ptSq_zero_pairs_with_given(grid, target_value, given_point):
    n = len(grid)
    zero_in_squares = []

    target_points = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == target_value and (i, j) != given_point]
    zero_points = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == 0]

    def is_square(p1, p2, p3, p4):
        dists = sorted([dist(p1, p2), dist(p1, p3), dist(p1, p4), 
                        dist(p2, p3), dist(p2, p4), dist(p3, p4)])
        return dists[0] == dists[1] == dists[2] == dists[3] > 0 and dists[4] == dists[5]

    def dist(p1, p2):
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    for target_point in target_points:
        for zero1, zero2 in itertools.combinations(zero_points, 2):
            if is_square(given_point, target_point, zero1, zero2):
                zero_in_squares.extend([zero1, zero2])
                break 

    return zero_in_squares

def find_3pt_square_zeros(grid, target_value):
    n = len(grid)
    zero_in_squares = []

    target_points = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == target_value]
    zero_points = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == 0]

    def is_square(p1, p2, p3, p4):
        dists = sorted([dist(p1, p2), dist(p1, p3), dist(p1, p4), 
                        dist(p2, p3), dist(p2, p4), dist(p3, p4)])
        return dists[0] == dists[1] == dists[2] == dists[3] > 0 and dists[4] == dists[5]

    def dist(p1, p2):
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    for zero_point in zero_points:
        for p1, p2, p3 in itertools.combinations(target_points, 3):
            if is_square(zero_point, p1, p2, p3):
                zero_in_squares.append(zero_point)
                break  

    return zero_in_squares


def adjust_weights_for_point(point, player, grid):
    global WEIGHTS

    increment = 1
    
    rows, cols = SIZE, SIZE
    x1, y1 = point

    WEIGHTS[x1][y1] = float('-inf')

    """if player == 1:
        zeros = find_3pt_square_zeros_with_given_pt(grid, player, point)
        for xx,yy in zeros:
            WEIGHTS[xx][yy] += 2
    else:
        zeros = find_3pt_square_zeros(grid, player)
        for xx,yy in zeros:
            WEIGHTS[xx][yy] += 2

    zeros = find_2ptSq_zero_pairs_with_given(grid, player, point)
    for xx,yy in zeros:
        WEIGHTS[xx][yy] += 1"""

    def is_in_grid(x, y):
        return 0 <= x < rows and 0 <= y < cols

    for x2 in range(rows):
        for y2 in range(cols):
            if (x1, y1) == (x2, y2):
                continue 

            dx = x2 - x1
            dy = y2 - y1

            x3, y3 = x2 - dy, y2 + dx
            x4, y4 = x1 - dy, y1 + dx

            if is_in_grid(x3, y3) and is_in_grid(x4, y4):
                WEIGHTS[x2][y2] += increment
                WEIGHTS[x3][y3] += increment
                WEIGHTS[x4][y4] += increment

            x3, y3 = x2 + dy, y2 - dx
            x4, y4 = x1 + dy, y1 - dx

            if is_in_grid(x3, y3) and is_in_grid(x4, y4):
                WEIGHTS[x2][y2] += increment
                WEIGHTS[x3][y3] += increment
                WEIGHTS[x4][y4] += increment

def get_points(n):
    global WEIGHTS  

    #zeros = find_3pt_square_zeros_with_given_pt(grid, player, point)
    points_with_weights = [
        ((x, y), WEIGHTS[x][y]) 
        for x in range(len(WEIGHTS)) 
        for y in range(len(WEIGHTS[0])) 
        if WEIGHTS[x][y] != float('-inf')
    ]

    sorted_points = sorted(points_with_weights, key=lambda item: item[1], reverse=True)
    top_n_points = [point for point, weight in sorted_points[:min(n, len(sorted_points))]]
    return top_n_points



