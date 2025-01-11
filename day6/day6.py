from typing import NamedTuple
import numpy as np
from dataclasses import dataclass
from enum import IntEnum, auto


class Direction(IntEnum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


class Point(NamedTuple):
    row: int
    col: int


@dataclass
class Guard:
    position: Point
    direction: Direction

    def rotate(self):
        self.direction = Direction(self.direction % 4 + 1)
        return self


@dataclass
class Map:
    guard: Guard
    dim: Point
    obstacles: list[Point]
    hit_obstacles: list[Point]
    guard_visited_positions: list[Point]
    guard_directions: list[Direction]

    def move_guard(self):
        guard_row, guard_col = self.guard.position
        direction = self.guard.direction
        self.guard_directions.append(direction)
        match direction:
            case Direction.UP:
                obstacle_list = [
                    row
                    for row, col in self.obstacles
                    if col == guard_col and row < guard_row
                ]
                nearest_obstacle = max(obstacle_list) if len(obstacle_list) else 0
                self.hit_obstacles.append(Point(row=nearest_obstacle, col=guard_col))
                self.guard.position = Point(row=nearest_obstacle + 1, col=guard_col)
                self.guard_visited_positions.extend(
                    Point(row, guard_col)
                    for row in range(
                        nearest_obstacle + 1 * bool(nearest_obstacle), guard_row
                    )
                )
            case Direction.DOWN:
                obstacle_list = [
                    row
                    for row, col in self.obstacles
                    if col == guard_col and row > guard_row
                ]
                nearest_obstacle = (
                    min(obstacle_list) if len(obstacle_list) else self.dim.row
                )
                self.hit_obstacles.append(Point(row=nearest_obstacle, col=guard_col))
                self.guard.position = Point(row=nearest_obstacle - 1, col=guard_col)
                self.guard_visited_positions.extend(
                    Point(row, guard_col) for row in range(guard_row, nearest_obstacle)
                )
            case Direction.RIGHT:
                obstacle_list = [
                    col
                    for row, col in self.obstacles
                    if col > guard_col and row == guard_row
                ]
                nearest_obstacle = (
                    min(obstacle_list) if len(obstacle_list) else self.dim.col
                )
                self.hit_obstacles.append(Point(row=guard_row, col=nearest_obstacle))
                self.guard.position = Point(row=guard_row, col=nearest_obstacle - 1)
                self.guard_visited_positions.extend(
                    Point(guard_row, col) for col in range(guard_col, nearest_obstacle)
                )
            case Direction.LEFT:
                obstacle_list = [
                    col
                    for row, col in self.obstacles
                    if col < guard_col and row == guard_row
                ]
                nearest_obstacle = max(obstacle_list) if len(obstacle_list) else 0
                self.hit_obstacles.append(Point(row=guard_row, col=nearest_obstacle))
                self.guard.position = Point(row=guard_row, col=nearest_obstacle + 1)
                self.guard_visited_positions.extend(
                    Point(guard_row, col)
                    for col in range(
                        nearest_obstacle + 1 * bool(nearest_obstacle), guard_col
                    )
                )

        self.guard.rotate()
        return len(obstacle_list) > 0


def where_guard(map_var: np.ndarray) -> Point:
    nrow, ncol = map_var.shape
    for i in range(nrow):
        for j in range(ncol):
            if map_var[i, j] in ("^", ">", "v", "<"):
                return Point(row=i, col=j)
    raise ValueError("Map does not contain a guard")


def where_faces(guard: str) -> Direction:
    match guard:
        case "^":
            return Direction.UP
        case ">":
            return Direction.RIGHT
        case "v":
            return Direction.DOWN
        case "<":
            return Direction.LEFT
        case _:
            raise ValueError("Input is not guard")


def where_obstacles(map_var: np.ndarray) -> list[Point]:
    obstacle_coord: list[Point] = []
    nrow, ncol = map_var.shape
    for i in range(nrow):
        for j in range(ncol):
            if map_var[i, j] == "#":
                obstacle_coord.append(Point(i, j))
    return obstacle_coord


def create_map(map_var: np.ndarray) -> Map:
    guard_row, guard_col = where_guard(map_var)
    guard_initial_direction: Direction = where_faces(map_var[guard_row, guard_col])
    guard = Guard(Point(guard_row, guard_col), guard_initial_direction)
    obstacles = where_obstacles(map_var)
    map_object = Map(
        guard=guard,
        dim=Point(*map_var.shape),
        obstacles=obstacles,
        hit_obstacles=[],
        guard_visited_positions=[Point(guard_row, guard_col)],
        guard_directions=[guard_initial_direction],
    )

    return map_object


def run_map(map_var: np.ndarray):
    map: Map = create_map(map_var)
    is_not_outside_map = True

    while is_not_outside_map:
        is_not_outside_map = map.move_guard()

    map.hit_obstacles.append(map.guard.position)

    return map


def can_make_loop(first: Point, last: Point, initial_direction: Direction, dim: Point):
    match initial_direction:
        case Direction.UP:
            return last.col < first.col and not first.col == 0
        case Direction.DOWN:
            return last.col > first.col and not first.col == dim.col
        case Direction.RIGHT:
            return last.row < first.row and not last.row == 0
        case Direction.LEFT:
            return last.row > first.row and not last.row == dim.row


def insert_obstacle(
    first: Point, last: Point, initial_direction: Direction, dim: Point
):
    if not can_make_loop(first, last, initial_direction, dim):
        return None

    match initial_direction:
        case Direction.UP:
            return Point(row=last.row, col=first.col - 1)
        case Direction.DOWN:
            return Point(row=last.row, col=first.col + 1)
        case Direction.RIGHT:
            return Point(row=last.row - 1, col=first.col)
        case Direction.LEFT:
            return Point(row=last.row + 1, col=first.col)


def part1_solution():
    with open("input.txt", "r") as f:
        guard_map: np.ndarray = np.array([list(line.strip()) for line in f])

    map = run_map(guard_map)

    return len(set(map.guard_visited_positions))


def part2_solution():
    with open("input.txt", "r") as f:
        guard_map: np.ndarray = np.array([list(line.strip()) for line in f])

    map = run_map(guard_map)
    hit_obstacles = map.hit_obstacles
    guard_directions = map.guard_directions
    extra_obstacles: list[Point] = []

    for i, (first, direction) in enumerate(zip(hit_obstacles, guard_directions)):
        if i + 3 > len(hit_obstacles) - 1:
            break
        last = hit_obstacles[i + 3]
        extra_obstacles.append(insert_obstacle(first, last, direction, map.dim))

    return len(set(extra_obstacles)) + 1


if __name__ == "__main__":
    # print(part1_solution())

    print(part2_solution())
