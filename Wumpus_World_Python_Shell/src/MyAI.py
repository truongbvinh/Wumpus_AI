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

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        self.grabbed = False
        self.wumpus_shot = False
        self.record = dict()
        self.pos = [1, 1]
        self.direction = 0 # 0 == right, 1 == up, 2 == left, 3 == down

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
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
        if row in self.record.keys():
            record[x] = set(y)
        else:
            record[x].add(y)

    def escape(self, stench, breeze, glitter, bump, scream):
        pass



    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
