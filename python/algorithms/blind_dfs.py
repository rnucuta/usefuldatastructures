# """
# This is the robot's control interface.
# You should not implement it, or speculate about its implementation
# """
#class Robot:
#    def move(self):
#        """
#        Returns true if the cell in front is open and robot moves into the cell.
#        Returns false if the cell in front is blocked and robot stays in the current cell.
#        :rtype bool
#        """
#
#    def turnLeft(self):
#        """
#        Robot will stay in the same cell after calling turnLeft/turnRight.
#        Each turn will be 90 degrees.
#        :rtype void
#        """
#
#    def turnRight(self):
#        """
#        Robot will stay in the same cell after calling turnLeft/turnRight.
#        Each turn will be 90 degrees.
#        :rtype void
#        """
#
#    def clean(self):
#        """
#        Clean the current cell.
#        :rtype void
#        """

class Solution:
    def cleanRoom(self, robot):
        """
        :type robot: Robot
        :rtype: None
        """
        # up, down, right, left
        moves = [(-1, 0, 0), (1, 0, 1), (0, 1, 2), (0, -1, 3)]
        visited = set([(0, 0)])
        #0 = up
        #1 = down
        #2 = right
        #3 = left
        orientation = 0
        def reorient(curr_or, desired_or):
            nonlocal orientation
            if curr_or == desired_or:
                return
            if curr_or in (0, 1) and desired_or in (0, 1):
                robot.turnLeft()
                robot.turnLeft()
            elif curr_or in (2, 3) and desired_or in (2, 3):
                robot.turnLeft()
                robot.turnLeft()
            elif (curr_or, desired_or) in [(0, 2), (3, 0), (1, 3), (2, 1)]:
                robot.turnRight()
            else:
                robot.turnLeft()
            orientation = desired_or

        def dfs(x, y, parent):
            nonlocal orientation
            robot.clean()
            for dx, dy, new_or in moves:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    # reorient 
                    reorient(orientation, new_or)
                    valid = robot.move()
                    if valid:
                        dfs(nx, ny, (x, y))
            if parent is not None:
                #reorient to go to parent
                for dx, dy, new_or in moves:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) == parent:
                        reorient(orientation, new_or)
                        robot.move()
                        break

        dfs(0, 0, None)