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
        self.last_move = self.pos
        self.direction = 0 # 0 == right, 1 == up, 2 == left, 3 == down
        self.goal = None
        self.frontier = list()
        self.safety_value = defaultdict(lambda:1.0) # float is percentage that the square is safe
        self.traversed = set()
        self.move_list = list()
        self.grabbed = False
        self.x_max = None
        self.y_max = None

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        # all parameters are boolean values

        if self.glitter:
            return self.make_move(Agent.Action.GRAB)

        if self.last_move == Agent.Action.FORWARD:
            self.calculate_safety(stench, breeze)
            if breeze or stench:
                self.search_gold(self.goal[0], self.goal[1])
            
        if len(self.move_list) == 0:
            self.goal = self.frontier.pop()
            self.search_gold(self.goal[0], self.goal[1])

        return self.move_list.pop()[0]
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================

    ############################ HELPER ########################################

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
        danger = 1.0 - self.safety_value[(x, y)]
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


    def make_move(self, move):
        """
        Helper function to update attributes and call methods
        based on the move to make next
        """
        if move == Agent.Action.GRAB:
            self.grabbed = True
            self.goal = (1,1)
            self.escape()
        elif move == Agent.Action.FORWARD:
            if self.direction == 0:
                self.pos = (self.pos[0]+1, self.pos[1])
            elif self.direction == 1:
                self.pos = (self.pos[0], self.pos[1]+1)
            elif self.direction == 2:
                self.pos = (self.pos[0]-1, self.pos[1])
            elif self.direction == 3:
                self.pos = (self.pos[0], self.pos[1]-1)
        elif move == Agent.Action.TURN_LEFT:
            self.direction = (self.direction+1)%4
        elif move == Agent.Action.TURN_RIGHT:
            self.direction = (self.direction-1)%4
        
        self.last_move = move
        
        return move

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
            spaces = self.__get_adj().discard(self.prev_pos)
            for space in spaces:
                if stench:
                    self.safety_value[space] *= 0.33
                if breeze:

                    self.safety_value[space] *= 0.33
    
    def update_frontier(self):
        """
        Updates the frontier with unexpanded spaces and sorts the frontier by the
        minimum distance from the current space to a given spot

        Return:
        None
        """
        for elem in self.__get_adj():
            if elem not in self.traversed:
                self.frontier.append(elem)
            self.safety_value[elem] # Touch the spot
        self.frontier.sort(lambda x: -(self.__min_distance(self.pos[0],self.pos[1],x[0],x[1])))

    def search_gold(self, goal_x, goal_y):
        self.move_list = self.__find_path(self.pos[0], self.pos[1], goal_x, goal_y)

    def escape(self):
        self.move_list = [(agent.Action.CLIMB, 1)]
        self.move_list.extend(self.__find_path(self.pos[0], self.pos[1], 1, 1, self.direction))


    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
