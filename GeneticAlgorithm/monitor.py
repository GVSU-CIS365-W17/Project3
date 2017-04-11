import krpc
import os

# this class is essentially static and really shouldn't ever exist more than once
class Monitor:
    this = None
    __maxAlt = 0
    __maxAp = 0
    __maxPe = 0
    __maxScore = 0
    
    def __init__(self):
        return

    # set commands check that this is a new max then sets them
    def setMaxAlt(self, alt:int) -> None:
        if alt > Monitor.__maxAlt:
            Monitor.__maxAlt = alt

    def setMaxApoapsis(self, apoapsis:int) -> None:
        if apoapsis > Monitor.__maxAp:
            Monitor.__maxAp = apoapsis

    def setMaxPeriapsis(self, periapsis:int) -> None:
        if periapsis > Monitor.__maxPe or Monitor.__maxPe == 0:
            Monitor.__maxPe = periapsis

    def setMaxScore(self, score:int, force = False) -> None:
        if score > Monitor.__maxScore or force or Monitor.__maxScore == 0:
            Monitor.__maxScore = score

    # used to write onto ksp using krpc.space_center.ui but it caused lag so that got trashed
    def runUpdate(self) -> None:
        print (self)

    def __str__(self):
        text = "Max Score: " + str(self.maxScore) + os.linesep
        text += "Max Apoapsis: " + str(self.maxApoapsis) + os.linesep
        text += "Max Pereapsis: " + str(self.maxPeriapsis) + os.linesep
        text += "Max Altitude: " + str(self.maxAltitue)
        return text

    @property
    def maxAltitue(self)->int:
        return Monitor.__maxAlt

    @property
    def maxApoapsis(self) -> int:
        return Monitor.__maxAp


    @property
    def maxPeriapsis(self) -> int:
        return Monitor.__maxPe

    @property
    def maxScore(self) -> int:
        return Monitor.__maxScore