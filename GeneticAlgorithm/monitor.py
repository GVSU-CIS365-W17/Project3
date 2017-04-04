import krpc
import os

class Monitor:
    this = None

    def __init__(self, connection:krpc.Connection):
        self.__maxAlt = 0
        self.__maxAp = 0
        self.__maxPe = 0
        self.__maxScore = 0
        self.__conn = connection
        self.__textAlt = None
        self.__textAp = None
        self.__textPe = None
        self.__textScore = None
        self.__panel = self.__conn.ui.stock_canvas.add_panel()

    def setMaxAlt(self, alt:int) -> None:
        if alt > self.__maxAlt:
            self.__maxAlt = alt

    def setMaxApoapsis(self, apoapsis:int) -> None:
        if apoapsis > self.__maxAp:
            self.__maxAp = apoapsis

    def setMaxPeriapsis(self, periapsis:int) -> None:
        if periapsis > self.__maxPe:
            self.__maxPe = periapsis

    def setMaxScore(self, score:int, force = False) -> None:
        if score > self.__maxScore or force:
            self.__maxScore = score

    def runUpdate(self) -> None:
        panel1 = self.__conn.ui.stock_canvas.add_panel()
        panel2 = self.__conn.ui.stock_canvas.add_panel()
        panel3 = self.__conn.ui.stock_canvas.add_panel()
        panel4 = self.__conn.ui.stock_canvas.add_panel()
        panel1.rect_transform.position = (-200,210)
        panel2.rect_transform.position = (-200,195)
        panel3.rect_transform.position = (-200,180)
        panel4.rect_transform.position = (-200,165)
        self.__textScore = panel1.add_text("Max Score: " + str(int(self.maxScore)))
        self.__textScore.color = (255,255,255)
        self.__textAp = panel2.add_text("Max Apoapsis: " + str(int(self.maxApoapsis)))
        self.__textAp.color = (255,255,255)
        self.__textPe = panel3.add_text("Max Pereapsis: " + str(int(self.maxPeriapsis)))
        self.__textPe.color = (255,255,255)
        self.__textAlt = panel4.add_text("Max Altitude: " + str(int(self.maxAltitue)))
        self.__textAlt.color = (255,255,255)
        print (self)

    def __str__(self):
        text = "Max Score: " + str(self.maxScore) + os.linesep
        text += "Max Apoapsis: " + str(self.maxApoapsis) + os.linesep
        text += "Max Pereapsis: " + str(self.maxPeriapsis) + os.linesep
        text += "Max Altitude: " + str(self.maxAltitue)
        return text

    @property
    def maxAltitue(self)->int:
        return self.__maxAlt

    @property
    def maxApoapsis(self) -> int:
        return self.__maxAp


    @property
    def maxPeriapsis(self) -> int:
        return self.__maxPe

    @property
    def maxScore(self) -> int:
        return self.__maxScore