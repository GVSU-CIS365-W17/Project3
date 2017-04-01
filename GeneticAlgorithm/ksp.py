import krpc

class Ksp:
    __game = None
    #TODO implement and return all the values you need
    def getInputs(self) -> list:
        return [0,0,0]

    @property
    def game(self):
        return Ksp.__game

    #TODO this method should return false if it is crashed or done.
    @property
    def isValidFlight(self) -> bool:
        return True

    #TODO return to launchpad probably should use quick save or a save that we revert back to
    def restart(self) -> None:
        return

    #TODO based on its conditions it will return a socre
    @property
    def getFinalScore(self) -> int:
        return 0

    #TODO use the input to control ship
    def useOutput(self, inputs: list) -> None:
        return

    #TODO first thing we do in this launch
    def launch(self) -> None:
        return

    def __init__(self):
        self.conn = krpc.connect(name="Genetics")
        print(self.conn.krpc.get_status().version)
        self.kerbin = self.conn.space_center.bodies["Kerbin"]
        print(self.kerbin.name)
        self.vessel = self.conn.space_center.active_vessel
        self.autoPilot = self.vessel.auto_pilot
        self.flight = self.vessel.flight(self.kerbin.reference_frame)
        self.sasEnum = self.vessel.control.sas_mode
        Ksp.__game = self
        #TODO save game for start point