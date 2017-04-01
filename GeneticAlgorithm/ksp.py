import krpc
import numpy as np
import time

class Ksp:
    __game = None
    #TODO implement and return all the values you need
    def getInputs(self) -> list:
        val = []
        val.append(self.vessel.control.throttle)
        val.append(self.flight.horizontal_speed)
        val.append(self.flight.vertical_speed)
        val.append(self.autoPilot.target_heading)
        val.append(self.autoPilot.target_pitch)
        val.append(self.vessel.thrust)
        val.append(self.vessel.available_thrust)
        val.append(self.vessel.specific_impulse)
        val.append(self.flight.g_force)
        val.append(self.flight.mean_altitude)
        elevation = self.vessel.position(self.kerbin.reference_frame)
        elevation = np.linalg.norm(np.array(elevation))
        val.append(elevation)
        return val

    @property
    def game(self):
        return Ksp.__game

    #TODO this method should return false if it is crashed or done.
    @property
    def isValidFlight(self) -> bool:
        if (self.vessel.orbit.periapsis_altitude > 75000 or self.vessel.orbit.apoapsis_altitude > 150000):
            print("exiting for orbit")
            print("apoapsis",self.vessel.orbit.apoapsis_altitude)
            print("periapsis", self.vessel.orbit.periapsis_altitude)
            self.score = self.getFinalScore
            return False
        if self.vessel.situation not in [self.vessel.situation.flying, self.vessel.situation.orbiting, self.vessel.situation.sub_orbital]:
            print (self.vessel.situation)
            self.score = self.getFinalScore
            return False
        return True

    #TODO return to launchpad probably should use quick save or a save that we revert back to
    def restart(self) -> None:
        self.conn.space_center.load("ProjectStart")
        return

    #TODO based on its conditions it will return a socre
    @property
    def getFinalScore(self) -> int:
        score = 0
        runTime = time.localtime(time.time())[5] - self.launchTime[5]
        score += runTime/ (15*60) # persentage of runtime used should probably use curve that returns best value for 10 minutes
        if self.vessel.situation == self.vessel.situation.orbiting:
            score += 50
        if self.vessel.situation == self.vessel.situation.sub_orbital:
            score += 10
        if self.vessel.situation == self.vessel.situation.flying:
            score += 1
        if self.vessel.situation not in [self.vessel.situation.flying, self.vessel.situation.orbiting, self.vessel.situation.sub_orbital]:
            return 0
        #TODO add some other stuff to score with
        return score

    #TODO use the input to control ship
    def useOutput(self, inputs: list) -> None:
        pitch = self.autoPilot.target_pitch + (inputs[0] * 2 if inputs[0] > 0.5 else -inputs[0] * 2)
        heading = self.autoPilot.target_heading + (inputs[1] * 2 if inputs[1] > 0.5 else -inputs[1] * 2)
        self.autoPilot.target_pitch_and_heading(pitch, heading)
        self.vessel.control.throttle = inputs[2]
        if inputs[3] > 0.5:
            self.vessel.control.activate_next_stage

    #TODO first thing we do in this launch
    def launch(self) -> None:
        self.vessel.control.activate_next_stage()
        self.launchTime = time.localtime(time.time())
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
        self.score = 0
        self.launchTime = time.localtime(time.time())
        #TODO save game for start point
        self.conn.space_center.save("ProjectStart")