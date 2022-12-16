#!/usr/bin/env python3
import fileinput
from typing import List

def visibility_mask(tree_line: List[int]) -> List[bool]:
    mask = []
    tallest_tree = -1
    for tree in tree_line:
        if tree > tallest_tree:
            mask.append(True)
            tallest_tree = tree
        else:
            mask.append(False)
    return mask

def visible_trees(trees: List[List[int]]) -> List[List[bool]]:
    # by rows
    visible_trees = []

    # left to right
    for tree_line in trees:
        visible_trees.append(visibility_mask(tree_line))

    # right to left
    temp_visible_trees = []
    for (tree_line, visible_tree_line) in zip(trees, visible_trees):
        temp_visible_trees.append([x or y for x, y in zip(reversed(visibility_mask(reversed(tree_line))), visible_tree_line)])
    visible_trees = temp_visible_trees

    # by columns
    trees = [list(tree_line) for tree_line in zip(*trees)]
    visible_trees = [list(tree_line) for tree_line in zip(*visible_trees)]

    # top to bottom
    temp_visible_trees = []
    for (tree_line, visible_tree_line) in zip(trees, visible_trees):
        temp_visible_trees.append([x or y for x, y in zip(visibility_mask(tree_line), visible_tree_line)])
    visible_trees = temp_visible_trees

    # bottom to up
    temp_visible_trees = []
    for (tree_line, visible_tree_line) in zip(trees, visible_trees):
        temp_visible_trees.append([x or y for x, y in zip(reversed(visibility_mask(reversed(tree_line))), visible_tree_line)])
    visible_trees = temp_visible_trees

    # final transpose
    return [list(tree_line) for tree_line in zip(*visible_trees)]

def scenic_score(trees: List[List[int]]) -> List[List[int]]:
    def tree_score(trees: List[List[int]], x: int, y: int) -> int:
        tree_height = trees[y][x]

        # looking up
        up_score = 0
        for i in range(y - 1, -1, -1):
            up_score += 1
            if trees[i][x] >= tree_height:
                break

        # looking down
        down_score = 0
        for i in range(y + 1, len(trees), 1):
            down_score += 1
            if trees[i][x] >= tree_height:
                break

        # looking left
        left_score = 0
        for i in range(x - 1, -1, -1):
            left_score += 1
            if trees[y][i] >= tree_height:
                break

        # looking right
        right_score = 0
        for i in range(x + 1, len(trees[y]), 1):
            right_score += 1
            if trees[y][i] >= tree_height:
                break

        return up_score * down_score * left_score * right_score

    # initialize scores to 0
    scores = [[0 for _ in row] for row in trees]

    for y in range(1, len(trees) - 1):
        for x in range(1, len(trees[y]) - 1):
            scores[y][x] = tree_score(trees, x, y)
    return scores

if __name__ == '__main__':
    test_trees = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]
    assert sum(tree for tree_line in visible_trees(test_trees) for tree in tree_line) == 21

    trees = []
    for tree_line in fileinput.input():
        trees.append([int(tree) for tree in tree_line.strip()])

    outside_visible_trees = sum(tree for tree_line in visible_trees(trees) for tree in tree_line)
    print(f"Visible trees from the outside: {outside_visible_trees}")
    
    assert max(score for score_line in scenic_score(test_trees) for score in score_line) == 8

    max_scenic_score = max(score for score_line in scenic_score(trees) for score in score_line)
    print(f"Max scenic score: {max_scenic_score}")
