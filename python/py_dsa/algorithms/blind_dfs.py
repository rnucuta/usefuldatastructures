from typing import List, Tuple, Union


class Robot:
    def __init__(self, row: int, col: int, room: List[List[int]]):
        """Initial orientation of the robot will be facing up.
        0 represents a wall, 1 represents an empty slot to clean.
        """
        assert 0 <= row < len(room) and 0 <= col < len(room[0]) and room[row][col]
        self.row = row
        self.col = col
        self.m = len(room)
        self.n = len(room[0])
        self.room = room
        self.orientation = 0  # 0 == up, 1 == right, 2 == down, 3 == left
        self.moves = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
        self.not_clean = set(
            [(i, j) for i, row in enumerate(room) for j, cell in enumerate(row) if cell]
        )

    def move(self) -> bool:
        """Returns true if the cell in front is open and robot moves into the cell.
        Returns false if the cell in front is blocked and robot stays in the current cell.
        :rtype: bool
        """
        dr, dc = self.moves[self.orientation]
        nr, nc = self.row + dr, self.col + dc
        if 0 <= nr < self.m and 0 <= nc < self.n and self.room[nr][nc]:
            self.row = nr
            self.col = nc
            return True
        return False

    def turnLeft(self) -> None:
        """Robot will stay in the same cell after calling turnLeft/turnRight.
        Each turn will be 90 degrees.
        :rtype: None
        """
        self.orientation = (self.orientation - 1) % 4

    def turnRight(self) -> None:
        """Robot will stay in the same cell after calling turnLeft/turnRight.
        Each turn will be 90 degrees.
        :rtype: None
        """
        self.orientation = (self.orientation + 1) % 4

    def clean(self) -> None:
        """Clean the current cell.
        :rtype: None
        """
        if (self.row, self.col) in self.not_clean:
            self.not_clean.remove((self.row, self.col))

    def roomIsClean(self) -> bool:
        """Checks if the entire room has been cleaned.
        Returns True if all cells have been cleaned, False otherwise.
        :rtype: bool
        """
        return len(self.not_clean) == 0


def blindDFS(robot: "Robot") -> None:
    """Params:
    :type robot: Robot
    :rtype: None
    """
    # up, down, right, left
    moves = [(-1, 0, 0), (1, 0, 1), (0, 1, 2), (0, -1, 3)]
    visited = set([(0, 0)])
    # 0 = up
    # 1 = down
    # 2 = right
    # 3 = left
    orientation = 0

    def reorient(desired_or: int) -> None:
        """Reorients the robot to face the desired orientation.

        This function adjusts the robot's orientation to match the desired orientation.
        It calculates the difference between the current and desired orientations and performs
        the necessary turns to align the robot with the desired direction.

        :param desired_or: The desired orientation for the robot.
        """
        nonlocal orientation
        if orientation == desired_or:
            return
        if orientation in (0, 1) and desired_or in (0, 1):
            robot.turnLeft()
            robot.turnLeft()
        elif orientation in (2, 3) and desired_or in (2, 3):
            robot.turnLeft()
            robot.turnLeft()
        elif (orientation, desired_or) in [(0, 2), (3, 0), (1, 3), (2, 1)]:
            robot.turnRight()
        else:
            robot.turnLeft()
        orientation = desired_or

    def dfs(x: int, y: int, parent: Union[None, Tuple[int, int]]) -> None:
        """Performs a depth-first search from the given position.

        This function explores the room by performing a depth-first search from
        the current position (x, y). It keeps track of the parent position to ensure
        it can backtrack to the starting point.

        :param x: The x-coordinate of the current position.
        :param y: The y-coordinate of the current position.
        :param parent: The position of the parent node in the search tree.
        """
        nonlocal orientation
        robot.clean()
        for dx, dy, new_or in moves:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                # reorient
                reorient(new_or)
                valid = robot.move()
                if valid:
                    dfs(nx, ny, (x, y))
        if parent is not None:
            # reorient to go to parent
            for dx, dy, new_or in moves:
                nx, ny = x + dx, y + dy
                if (nx, ny) == parent:
                    reorient(new_or)
                    robot.move()
                    break

    dfs(0, 0, None)
