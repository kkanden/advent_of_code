import numpy as np
from itertools import product

with open("input.txt", "r") as f:
    text: np.ndarray = np.array([list(line.strip()) for line in f])

directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def count_xmas(grid: np.ndarray, word: str = "XMAS"):
    nrow, ncol = grid.shape
    word_len: int = len(word)
    count: int = 0

    def is_within_bound(x, y, dx, dy):
        return (
            0 <= x + (word_len - 1) * dx < nrow and 0 <= y + (word_len - 1) * dy < ncol
        )

    for i, j in product(range(nrow), range(ncol)):
        if grid[i, j] != word[0]:
            continue
        for dx, dy in directions:
            if not is_within_bound(i, j, dx, dy):
                continue
            word_extracted: str = "".join(
                grid[i + k * dx, j + k * dy] for k in range(word_len)
            )
            if word_extracted == word:
                count += 1
    return count


print(count_xmas(text))


######
def count_x_mas(grid: np.ndarray, word: str = "MAS"):
    assert len(word) % 2 == 1
    nrow, ncol = grid.shape
    count: int = 0

    def can_make_square(i, j):
        return 1 <= i < nrow - 1 and 1 <= j < ncol - 1

    for i, j in product(range(nrow), range(ncol)):
        if grid[i, j] != word[len(word) // 2]:
            continue
        if not can_make_square(i, j):
            continue
        word_diag_right = "".join(np.diag(grid[(i - 1) : (i + 2), (j - 1) : (j + 2)]))
        word_diag_left = "".join(
            np.diag(np.fliplr(grid[(i - 1) : (i + 2), (j - 1) : (j + 2)]))
        )

        if (word_diag_right == word or word_diag_right[::-1] == word) and (
            word_diag_left == word or word_diag_left[::-1] == word
        ):
            count += 1

    return count


print(count_x_mas(text, "XXXx"))
