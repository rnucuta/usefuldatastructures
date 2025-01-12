import unittest
from py_dsa.algorithms import blindDFS, Robot
from random import randint

class TestBlindDfs(unittest.TestCase):
    def test_dfs1(self):
        room = [[1,1,1,1,1,0,1,1],[1,1,1,1,1,0,1,1],[1,0,1,1,1,1,1,1],[0,0,0,1,0,0,0,0],[1,1,1,1,1,1,1,1]]
        row = 1
        col = 3
        robot = Robot(row, col, room)
        blindDFS(robot)
        self.assertTrue(robot.roomIsClean())

    def test_dfs2(self):
        room = [[1]]
        row = 0
        col = 0
        robot = Robot(row, col, room)
        blindDFS(robot)
        self.assertTrue(robot.roomIsClean())

    # have to generate possible test cases
    # TODO: could check if possible with DSJ?
    # def test_dfs3(self):
    #     m, n = 100, 200
    #     room = [[randint(0, 1) for _ in range(n)] for _ in range(m)]
    #     while (row := randint(0, m - 1), col := randint(0, n - 1)) and room[row][col] != 1:
    #         pass  # Keep searching until a valid position is found
    #     robot = Robot(row, col, room)
    #     blindDFS(robot)
    #     self.assertTrue(robot.roomIsClean())

    # def test_dfs4(self):
    #     m, n = 100, 200
    #     room = [[randint(0, 1) for _ in range(n)] for _ in range(m)]
    #     while (row := randint(0, m - 1), col := randint(0, n - 1)) and room[row][col] != 1:
    #         pass  # Keep searching until a valid position is found
    #     robot = Robot(row, col, room)
    #     blindDFS(robot)
    #     self.assertTrue(robot.roomIsClean())

if __name__ == '__main__':
    unittest.main()
