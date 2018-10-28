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
from collections import defaultdict

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        self.grabbed = False
        self.wumpus_shot = False
        self.record = defaultdict(lambda:1.0) # float is percentage that the square is safe
        self.pos = (1,1)
        self.prev_pos = (1,1)
        self.direction = 0 # 0 == right, 1 == up, 2 == left, 3 == down
        self.frontier = list()
        self.x_max = None
        self.y_max = None
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
            return self.escape(stench, breeze, glitter, bump, scream)

        if self.last_move = Agent.Action.FORWARD:
            self.calculate_safety(stench, breeze)
        
        if self.


        return Agent.Action.CLIMB
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
    
    def __min_distance(self, x1, y1, x2, y2):
        """
        Hueristic function to estimate the cost from start (x1, y1) to goal (x2, y2)

        Keyword arguments:
        x1: x value of start coordinate
        y1: y value of start coordinate
        x2: x value of goal coordinate
        y2: y value of goal coordinate

        Return:
        int value of estimated cost to reach goal from start
        """
        dx = x2 - x1
        dy = y2 - y1
        if self.direction%2==0:
            xdir, ydir = self.direction-1, 0
        else:
            xdir, ydir = 0, (self.direction-2)*(-1)
        
        if dx/abs(dx) != xdir and dy/abs(dy) != ydir:
            return 1 + dx + dy
        return dx + dy
    
    def __find_path(self, x1, y1, x2, y2):
        """
        Uses A* search algorithm to find any valid path while avoiding
        risky moves
        """
        pass
    
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
        self.frontier.sort(lambda x: self.__min_distance(self.pos[0],self.pos[1],x[0],x[1]))

    def search_gold(self, stench, breeze, glitter, bump, scream):
        # if the space is 'safe', then there's no breeze or stench
        if self.last_move == Agent.Action.FORWARD:
            if self.pos[0] not in self.record.keys() or self.pos[1] not in self.record[self.pos[0]]:
                self.calculate_safety(stench, breeze)
            self.__recordMove(self.pos[0], self.pos[1])

    def escape(self, stench, breeze, glitter, bump, scream):
        pass


    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
