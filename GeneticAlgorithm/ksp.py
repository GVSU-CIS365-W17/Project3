import krpc
import numpy as np
import time
import math
from monitor import Monitor

class Ksp:
    __game = None
    #TODO add more inputs like mass and fuel left and scale them
    def getInputs(self) -> list:
        val = []
        val.append(self.vessel.control.throttle)
        val.append(self.flight.horizontal_speed/1000)
        val.append(self.flight.vertical_speed/1000)
        heading = self.autoPilot.target_heading + self.autoPilot.heading_error
        val.append(heading/360)
        pitch = self.autoPilot.target_pitch + self.autoPilot.pitch_error
        val.append(pitch/90)
        val.append(self.vessel.thrust/215000)
        val.append(self.vessel.available_thrust/215000)
        val.append(self.vessel.specific_impulse/320)
        val.append(self.flight.g_force) # range should be close to [0-3]
        val.append(self.flight.mean_altitude/150000)
        elevation = self.vessel.position(self.kerbin.reference_frame)
        elevation = np.linalg.norm(np.array(elevation))
        val.append(elevation/150000)
        val.append(self.vessel.orbit.periapsis_altitude/75000)
        val.append(self.vessel.orbit.apoapsis_altitude/150000)
        val.append(self.fuelRemaining(self.vessel)/100)
        return val

    @property
    def game(self):
        return Ksp.__game

    def stage(self):
        if self.__stage < 0:
            return
        self.__stage -= 1
        self.vessel.control.activate_next_stage()

    #TODO Improve this method though it works as is
    @property
    def isValidFlight(self) -> bool:
        brokeApoapsis = lambda x: x > 150000
        brokeFlightPatern = lambda x: x not in [self.vessel.situation.flying, self.vessel.situation.orbiting, self.vessel.situation.sub_orbital]
        brokeSpeed = lambda x: x <= 0
        inFlightRange = lambda x: x > 100 and x < 70000
        outOfFuel = lambda x: self.fuelRemaining(x) == 0
        if brokeApoapsis(self.vessel.orbit.apoapsis_altitude):
            print("exiting for orbit")
            print("apoapsis",self.vessel.orbit.apoapsis_altitude)
            print("periapsis", self.vessel.orbit.periapsis_altitude)
            return False
        if brokeFlightPatern(self.vessel.situation):
            print (self.vessel.situation)
            return False
        if brokeSpeed(self.flight.vertical_speed) and inFlightRange(self.flight.mean_altitude):
            print ("reject for speed")
            return False
        if self.notExploded():
            print ("Exploson occured")
            return False
        if outOfFuel(self.vessel):
            print("Out of Fuel")
            return False
        return True

    def fuelRemaining(self, vessel):
        return min([vessel.resources.amount("LiquidFuel"), vessel.resources.amount("Oxidizer")])

    def notExploded(self) -> bool:
        for part in self.__parts:
            if [c._object_id for c in self.vessel.parts.all].__contains__(part[0]):
                continue
            elif part[1] <= self.__stage:
                return True
        return False

    def restart(self) -> None:
        self.__stage = max(c.decouple_stage for c in self.vessel.parts.all)
        self.conn.space_center.load("ProjectStart")
        return

    def useOutput(self, inputs: list) -> None:
        pitch = inputs[0] - 0.5 * 180
        heading = inputs[1] * 360
        self.autoPilot.target_pitch_and_heading(pitch, heading)
        self.vessel.control.throttle = inputs[2]
        if inputs[3] > 0.5:
            self.stage()

    def launch(self) -> None:
        self.conn.space_center.save ("ProjectStart")
        self.stage()
        self.score = 0
        print (Monitor.this)
        self.launchTime = time.localtime(time.time())
        return

    def __init__(self):
        self.conn = krpc.connect(name="Genetics")
        Monitor.this = Monitor(self.conn)
        print(self.conn.krpc.get_status().version)
        self.kerbin = self.conn.space_center.bodies["Kerbin"]
        print(self.kerbin.name)
        self.vessel = self.conn.space_center.active_vessel
        self.autoPilot = self.vessel.auto_pilot
        self.flight = self.vessel.flight(self.kerbin.reference_frame)
        self.sasEnum = self.vessel.control.sas_mode
        Ksp.__game = self
        self.score = 0
        self.__stage = max(c.decouple_stage for c in self.vessel.parts.all)
        self.__parts = [(c._object_id, c.decouple_stage) for c in self.vessel.parts.all]
        self.launchTime = time.localtime(time.time())
        self.conn.space_center.save("ProjectStart")
