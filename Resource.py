from read_file import read_file

class Resource():
    def __init__(self, info):
        self.RI = info['RI'] # ID
        self.RA = info['RA'] # Cost
        self.RP = info['RP'] # Maintenance Cost
        self.RW = info['RW'] # Active turns
        self.RM = info['RM'] # Downtime turns
        self.RL = info['RL'] # Lifecycle
        self.RU = info['RU'] # No. powered buildings
        self.RT = info['RT'] # Effect
        self.RE = info['RE'] # Effect percentage
        self.turnsActive = 0
        self.turnsDown = 0
        self.isActive = True

    def updateTurns(self):
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
        


    