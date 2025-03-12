import math

class Resource:
    def __init__(self, info, lifespan_increase=1):
        self.originalInfo = info

        self.RI = info['RI'] # ID
        self.RA = info['RA'] # Cost
        self.RP = info['RP'] # Maintenance Cost
        self.RW = info['RW'] # Active turns
        self.RM = info['RM'] # Downtime turns
        self.RL = info['RL'] # Lifecycle
        self.RU = info['RU'] # No. powered buildings
        self.RT = info['RT'] # Effect
        if self.RT != "X":
            self.RE = info['RE'] # Effect percentage

        ## apply effect C
        self.RL = math.floor(self.RL * lifespan_increase)

        self.turnsActive = 0
        self.turnsDown = 0
        self.turnsExisted = 0
        self.isActive = True

    def update_turns(self):
        self.turnsExisted += 1
        if self.isActive:
            self.turnsActive += 1
            if self.turnsActive == self.RW:
                self.isActive = False
                self.turnsActive = 0

        else:
            self.turnsDown += 1
            if self.turnsDown == self.RM:
                self.isActive = True
                self.turnsDown = 0
    def get_out_of_life(self):
        return self.turnsExisted == self.RL

    def get_maintenance_cost(self):
        return self.RP

    def get_powered_buildings(self):
        if self.isActive:
            return self.RU
        return 0

    def recreate(self, lifespan_increase=1):
        return Resource(self.originalInfo, lifespan_increase)

    