# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis, Vinh Truong, Brian Chou
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
from collections import defaultdict, namedtuple
import heapq

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        self.pos = (1,1)
        self.direction = 0 # 0 == right, 1 == up, 2 == left, 3 == down
        self.frontier = list()
        self.record = defaultdict(lambda:1.0) # float is percentage that the square is safe
        self.traversed = set()
        self.move_list = list()
        self.grabbed = False
        self.x_max = None
        self.y_max = None
        self.wumpus_shot = False
        self.last_move = None

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        # all parameters are boolean values
        if self.grabbed:
            return self.escape()

        if self.last_move == Agent.Action.FORWARD:
            self.calculate_safety(stench, breeze)

        if len(self.move_list) == 0:
            goal = self.frontier.pop()
            self.move_list = self.__find_path(self.pos[0], self.pos[1], goal[0], goal[1])


        return self.move_list.pop()[0]
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================

    ############################ HELPER ########################################

    def __recordMove(self):
        self.record[self.pos]
        for move in self.__get_adj():
            self.record[move]

    def __get_adj(self):
        result = set()
        x, y = self.pos
        if self.pos[0] > 1:
            result.add(x-1,y)
        if self.pos[1] > 1:
            result.add(x,y-1)
        if self.x_max and self.pos[0] < self.x_max:
            result.add(x+1,y)
        if self.y_max and self.pos[1] < self.y_max:
            result.add(x,y+1)

        return result

    def __calculate_cost(self, x, y):
        danger = 1.0 - self.record[(x, y)]
        danger *= 1000
        return danger

    def __min_distance(self, x1, y1, x2, y2, facing):
        """
        Hueristic function to estimate the cost from start (x1, y1) to goal (x2, y2)
        Similar to Manhattan distance

        Keyword arguments:
        x1: x value of start coordinate
        y1: y value of start coordinate
        x2: x value of goal coordinate
        y2: y value of goal coordinate

        Return:
        int value of estimated cost to reach goal from start
        """
        if x1 == x2 and y1 == y2:
            return 0

        dx = x2 - x1
        dy = y2 - y1
        if facing%2==0:
            xdir, ydir = (facing-1)*(-1), 0
        else:
            xdir, ydir = 0, (facing-2)*(-1)

        if dx != xdir*abs(dx) and dy != ydir*abs(dy):
            return 1 + dx + dy
        return dx + dy

    def __find_path(self, x1, y1, x2, y2, facing):
        """
        Uses A* search algorithm to find any valid path while avoiding
        risky moves

        Keywork arguments:
        x1, y1: x and y coordinates of START position
        x2, y2: x and y coordinates of GOAL position
        facing: an integer from [0,3] which dictates the direction of agent

        Returns:
        A list of Agent.Actions to get from START to GOAL with lowest cost

        IMPORTANT: The returned list is in REVERSE order, so use pop() to get
        the actual order of operations
        """
        Node = namedtuple("Node", ["f", "cost", "x", "y", "direction", "parent", "action"])
        record = []
        search = []
        search.append(Node(self.__min_distance(x1, y1, x2, y2, facing), 0, x1, y1, facing, None, None))
        while len(search) != 0:
            expand = heapq.heappop(search)

            record.append(expand) # add parent index
            # index of parent for all expanded nodes is len(record) - 1

            heapq.heappush(search,
                Node(self.__min_distance(expand.x, expand.y, x2, y2, (expand.direction+1)%4)+expand.cost+1,
                expand.cost+1,
                expand.x,
                expand.y,
                (expand.direction+1)%4,
                len(record)-1,
                Agent.Action.TURN_LEFT)
            )
            heapq.heappush(search,
                Node(self.__min_distance(expand.x, expand.y, x2, y2, (expand.direction-1)%4)+expand.cost+1,
                expand.cost+1,
                expand.x,
                expand.y,
                (expand.direction-1)%4,
                len(record)-1,
                Agent.Action.TURN_RIGHT)
            )

            if expand.direction == 0:
                new_x, new_y = expand.x+1, expand.y
            elif expand.direction == 1:
                new_x, new_y = expand.x, expand.y+1
            elif expand.direction == 2:
                new_x, new_y = expand.x-1, expand.y
            elif expand.direction == 3:
                new_x, new_y = expand.x, expand.y-1

            if new_x == x2 and new_y == y2:
                record.append(Node(self.__calculate_cost(new_x, new_y)+expand.cost+1,
                    self.__calculate_cost(new_x, new_y)+expand.cost+1,
                    new_x,
                    new_y,
                    expand.direction,
                    len(record)-1,
                    Agent.Action.FORWARD)
                )
                break

            heapq.heappush(search,
                Node(self.__min_distance(new_x, new_y, x2, y2, expand.direction)+self.__calculate_cost(new_x, new_y)+expand.cost+1,
                self.__calculate_cost(new_x, new_y)+expand.cost+1,
                new_x,
                new_y,
                expand.direction,
                len(record)-1,
                Agent.Action.FORWARD)
            )

        parent = record[-1].parent
        result = [(record[-1].action, record[-1].cost)]
        while parent != None:
            result.append((record[parent].action, record[parent].cost))
            parent = record[parent].parent
        result.pop()

        return result

    ############################ MOVEMENT ######################################

    def calculate_safety(self, stench, breeze):
        """
        Will primitively calculate the danger of each space traveled based
        on the stench and breeze values and change the record table accordingly

        Keywork arguments:
        stench - True if stench, else False
        breeze - True if breeze, else False

        Return:
        None
        """
        if stench or breeze:
            spaces = self.__get_adj().remove(self.prev_pos)
            for space in spaces:
                if stench:
                    self.record[space] *= 0.33
                if breeze:
                    self.record[space] *= 0.33

    def update_frontier(self):
        """
        Updates the frontier with unexpanded spaces and sorts the frontier by the
        minimum distance from the current space to a given spot

        Return:
        None
        """
        for elem in self.__get_adj():
            if elem not in self.record.keys():
                self.frontier.append(elem)
            self.record[elem] # Touch the spot
        self.frontier.sort(lambda x: -(self.__min_distance(self.pos[0],self.pos[1],x[0],x[1])))

    def search_gold(self, stench, breeze, glitter, bump, scream):
        # if the space is 'safe', then there's no breeze or stench
        if self.last_move == Agent.Action.FORWARD:
            if self.pos[0] not in self.record.keys() or self.pos[1] not in self.record[self.pos[0]]:
                self.calculate_safety(stench, breeze)
            self.__recordMove(self.pos[0], self.pos[1])

    def escape(self):
        self.move_list = [(agent.Action.CLIMB, 1)]
        self.move_list.extend(self.__find_path(self.pos[0], self.pos[1], 1, 1, self.direction))


    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
