import time

import ntcore

from settings import *


class Comms:
    '''Handles communication between the program and network tables'''
    def __init__(self) -> None:
        instance = ntcore.NetworkTableInstance.getDefault()
        instance.startClient4(identity="Dashboard")

        self.networkTable = instance.getTable(key="Dashboard")

        if REAL:
            instance.setServerTeam(team=1155, port=5810)
            instance.startDSClient()
        else:
            instance.setServer(server_name="localhost")

        # Entry for the target branch to score on
        self.targetBranch = self.networkTable.getEntry(key="branch")
        self.targetBranch.setString(value="")

        # Entry for the target level to score on
        self.targetLevel = self.networkTable.getEntry(key="level")
        self.targetLevel.setInteger(value=0)

        # Entry for the status of the connection
        self.isConnected = self.networkTable.getEntry(key="robotConnected")
        self.isConnected.setBoolean(value=True)

        # Entry for the robot's alliance
        self.blueAlliance = self.networkTable.getEntry(key="blueAlliance")
        self.blueAlliance.setBoolean(value=True)

        # Entry for whether to score processor or not
        self.scoringProcessor = self.networkTable.getEntry(key="processor")
        self.scoringProcessor.setBoolean(value=False)

        # Entry for the closest branch
        self.closestBranch = self.networkTable.getEntry(key="closestBranch")
        self.closestBranch.setString(value="")

        # Tracks update ticks
        self.tick = self.networkTable.getEntry(key="tick")
        self.tick.setInteger(value=0)

    def update(self) -> None:
        '''Meant to be called periodically'''
        time.sleep(0.02)
        self.tick.setInteger(value=self.tick.getInteger(defaultValue=0) + 1)
        
    def setBranch(self, branch:str) -> None:
        self.targetBranch.setString(branch)

    def setLevel(self, level:int) -> None:
        self.targetLevel.setInteger(level)

    def getNearest(self) -> str:
        return self.closestBranch.getString("")
        
    def getIsConnected(self) -> bool:
        return self.isConnected.getBoolean(False)
    
    def getBlueAlliance(self) -> bool:
        return self.blueAlliance.getBoolean(True)
    