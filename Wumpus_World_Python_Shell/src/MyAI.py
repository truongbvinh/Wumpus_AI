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
        self.record = defaultdict(float) # float is percentage that the square is safe
        self.pos = (1,1)
        self.direction = 0 # 0 == right, 1 == up, 2 == left, 3 == down
        self.frontier = set()
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



        return Agent.Action.CLIMB
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def recordMove(self, x, y):
        record[x].add(y)
    
    def get_adj(self):
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
    
    def calculate_danger(self):
        spaces = self.get_adj()


    def search_gold(self, stench, breeze, glitter, bump, scream):
        # if the space is 'safe', then there's no breeze or stench
        if self.last_move == Agent.Action.FORWARD:
            if self.pos[0] not in self.record.keys() or self.pos[1] not in self.record[self.pos[0]]:
                self.calculate_danger
            self.recordMove(self.pos[0], self.pos[1])

    def escape(self, stench, breeze, glitter, bump, scream):
        pass




    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
