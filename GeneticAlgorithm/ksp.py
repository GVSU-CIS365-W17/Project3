import krpc
import numpy as np
import time
import math
from monitor import Monitor
import pyautogui
from multiprocessing import Process, Queue

class Ksp:
    # class variables
    __game = None
    __revertPosition = (796, 536)
    __launchPad = (1257, 388)
    __gtShip = (885, 526)
    __quitToMM = (929, 607)
    __resumeSaved = (678, 458)
    __ai2 = (755, 409)
    __load = (1001, 763)
    __leaveAnyway = (965, 545)

    # stores the game process
    APP = None

    # clicks in the given location on ksp
    @staticmethod
    def click(tup):
        Ksp.bringToFront()
        pyautogui.click(tup[0],tup[1])
    
    # brings ksp to the front
    @staticmethod
    def bringToFront():
        pyautogui.getWindow("Kerbal Space Program").restore()
        pyautogui.getWindow("Kerbal Space Program").set_foreground()
    
    # gets all the inputs for the ANN
    def getInputs(self) -> list:
        val = []
        val.append(self.vessel.control.throttle)
        val.append(self.flight.horizontal_speed/1000)
        val.append(self.flight.vertical_speed/1000)
        val.append(self.flight.heading/360)
        val.append(self.flight.pitch/90)
        val.append(self.flight.roll/180)
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
        val.append(self.control.current_stage)
        val.append(self.flight.atmosphere_density)  # no scale
        val.append(self.flight.dynamic_pressure/10000)  # 10000 scale
        val.append(self.flight.static_pressure/10000)  # 10000 scale
        val.append(self.flight.aerodynamic_force[0]/10)  # 10 scale list of 3
        val.append(self.flight.aerodynamic_force[1] / 10)  # 10 scale list of 3
        val.append(self.flight.aerodynamic_force[2] / 10)  # 10 scale list of 3
        val.append(self.flight.angle_of_attack/90)  # 90 scale
        val.append(self.flight.sideslip_angle/90)  # 90 scale
        val.append(self.vessel.moment_of_inertia[0]/10000)  # 10000 scale list of 3
        val.append(self.vessel.moment_of_inertia[1] / 10000)  # 10000 scale list of 3
        val.append(self.vessel.moment_of_inertia[2] / 10000)  # 10000 scale list of 3
        # val.append(self.vessel.available_torque[0][0]/10000)  # 10000 scale two lists of 3
        # val.append(self.vessel.available_torque[0][1]/10000)  # 10000 scale two lists of 3
        # val.append(self.vessel.available_torque[0][2]/10000)  # 10000 scale two lists of 3
        # val.append(self.vessel.available_torque[1][0]/10000)  # 10000 scale two lists of 3
        # val.append(self.vessel.available_torque[1][1]/10000)  # 10000 scale two lists of 3
        # val.append(self.vessel.available_torque[1][2]/10000)  # 10000 scale two lists of 3
        frame = self.conn.space_center.bodies["Kerbin"].reference_frame
        val.append(self.vessel.rotation(frame)[0])  # no scale list of 3
        val.append(self.vessel.rotation(frame)[1])  # no scale list of 3
        val.append(self.vessel.rotation(frame)[2])  # no scale list of 3
        val.append(self.vessel.direction(frame)[0])  # no scale list of 3
        val.append(self.vessel.direction(frame)[1])  # no scale list of 3
        val.append(self.vessel.direction(frame)[2])  # no scale list of 3
        # val.append(self.vessel.angular_velocity(frame)[0])  # no scale list of 3
        # val.append(self.vessel.angular_velocity(frame)[1])  # no scale list of 3
        # val.append(self.vessel.angular_velocity(frame)[2])  # no scale list of 3
#       for thing in val:
#            print (thing)
#        print("end")
        return val

    # gives this somewhat of the ability to be a singleton
    @property
    def game(self):
        return Ksp.__game

    # wraps the staging command so that way it can only stage when its appropriate
    def stage(self):
        if self.control.current_stage < 0 or self.vessel.available_thrust > 0:
            return
        self.__stage -= 1
        self.control.activate_next_stage()

    # stores the previous failure info
    death = None

    # checks to see if this is a valid flight
    @property
    def isValidFlight(self) -> bool:
        # don't ask me why I used lambdas here honestly just made it easier to understand the if statements
        brokeApoapsis = lambda x: x > 400000
        brokeFlightPatern = lambda x: x not in [self.vessel.situation.flying, self.vessel.situation.orbiting, self.vessel.situation.sub_orbital, self.vessel.situation.pre_launch]
        brokeSpeed = lambda x: x <= 0
        inFlightRange = lambda x: x > 80 and x < 70000
        outOfTime = lambda x: x >= 15*60
        outOfFuel = lambda x: self.fuelRemaining(x) == 0
        if brokeApoapsis(self.vessel.orbit.apoapsis_altitude):
            print("exiting for orbit")
            print("apoapsis",self.vessel.orbit.apoapsis_altitude)
            print("periapsis", self.vessel.orbit.periapsis_altitude)
            Ksp.death = "exiting for orbit"
            return False

        # needed to check the throttle to make sure we didn't just hit the supports on the way up and get back a landed value
        if brokeFlightPatern(self.vessel.situation) and self.control.throttle < 0.5:
            print ("Vessel not in correct flight situation:", self.vessel.situation)
            Ksp.death = "Vessel not in correct flight situation: " + str(self.vessel.situation)
            return False
        if brokeSpeed(self.flight.vertical_speed) and inFlightRange(self.flight.mean_altitude):
            print ("reject for speed")
            Ksp.death = "reject for speed"
            return False
        if self.flight.mean_altitude < 76:
            print ("Altitude: ", self.flight.mean_altitude)
            print ("reject for altitude")
            Ksp.death = "reject for altitude"
            return False
        if self.notExploded():
            print ("Exploson occured")
            Ksp.death = "Exploson occured"
            return False
        if outOfFuel(self.vessel):
            print("Out of Fuel")
            Ksp.death = "Out of Fuel"
            return False
        if outOfTime(self.vessel.met):
            print(self.vessel.met*60)
            print("Out of time")
            Ksp.death = "Out of time"
            return False
        return True

    # gets the remaining burnable fuel of the vessel
    def fuelRemaining(self, vessel):
        return min([vessel.resources.amount("LiquidFuel"), vessel.resources.amount("Oxidizer")])

    # technically gets if the craft has lost any parts that it shouldn't have given the current stage
    def notExploded(self) -> bool:
        for part in self.__parts:
            if [c._object_id for c in self.vessel.parts.all].__contains__(part[0]):
                continue
            elif part[1] <= self.__stage:
                return True
        return False

    # reloads the game and reconnects to krpc because sometimes it will loose connection when saving and loading
    def restart(self) -> None:
        self.__stage = self.__maxStage
        self.load()
        self.reconnect()
        return

    # quits to the Main Menu then reloads the actual save does more than just loading
    def reloadGame(self):
        Ksp.bringToFront()
        self.conn.close()
        self.conn = None
        time.sleep(0.05)
        pyautogui.press("esc")
        print ("Quitting To Main Menu")
        Ksp.click(Ksp.__quitToMM)
        time.sleep(1)
        Ksp.click(Ksp.__leaveAnyway)
        time.sleep(15)
        print("Resuming Save")
        Ksp.click(Ksp.__resumeSaved)
        time.sleep(2)
        Ksp.click(Ksp.__ai2)
        time.sleep(1)
        print("loading AI2")
        Ksp.click(Ksp.__load)
        q = Queue()

        # interestingly enough sometimes it will fail to get back into the game correctly and if that
        # happens then it will hang this allows me to test the connection and not get stuck
        p = Process(target=Ksp.testConnection, args=(q,))
        p.start()
        p.join(10)

        # if the process is alive then the process is hanging and I didn't reload the game so we need to exit or
        # we could just click through again but I wouldn't know what screen I was on
        if p.is_alive():
            print("Failed to reconnect to krpc")
            raise Exception("Failed to connect")
        time.sleep(0.5)
        Ksp.goToLaunchPad()
        self.reconnect()

    # clicks on the launch pad and goes to the ship on the launch pad because there should always be on there
    # if there isn't then this will fail and it will suck would need to be able to find out if there was one on the
    # pad but sadly krpc doesn't really work unless you are in a flight even though it says it does
    @staticmethod
    def goToLaunchPad():
        print("clicking launch pad")
        Ksp.click(Ksp.__launchPad)
        time.sleep(1)
        print("clicking go to ship")
        Ksp.click(Ksp.__gtShip)
        time.sleep(1)
        
    # reconnects to krpc and gets all the appropriate values
    def reconnect(self):
        gameSceen = self.tryToConnect()
        if gameSceen is None:
            raise Exception("Could not connect")
            return
        self.kerbin = self.conn.space_center.bodies["Kerbin"]
        self.vessel = self.conn.space_center.active_vessel
        self.control = self.vessel.control
        self.flight = self.vessel.flight(self.kerbin.reference_frame)
        self.score = 0
        
    # tests if it can connect and if it can then it puts true into the process Queue
    @staticmethod
    def testConnection(q):
        krpc.connect(name="Test")
        q.put(True)
        
    # trys to connect to krpc if it fails more than 5 times it explodes
    def tryToConnect(self):
        for i in range(5):
            #print("Attempting to connect try:", i)
            try:
                if self.conn is not None:
                    self.conn.close()
                self.conn = krpc.connect(name="Genetics")
                break
            except:
                self.conn = None
        if self.conn is None:
            return False
        return self.conn.krpc.current_game_scene

    # reverts the flight, previously used but seems to cause issues with krpc connections
    def revertFlight(self):
        pyautogui.getWindow("Kerbal Space Program").restore()
        pyautogui.getWindow("Kerbal Space Program").set_foreground()
        time.sleep(0.05)
        pyautogui.press("esc")
        time.sleep(0.5)
        pyautogui.click(x = self.__revertPosition[0], y = self.__revertPosition[1], clicks = 2, interval = 2)

    # uses the output from the neural network
    def useOutput(self, inputs: list) -> None:
        self.control.pitch = (inputs[0] - 0.5) * 2
        self.control.yaw = (inputs[1] - 0.5) *2
        self.control.throttle = inputs[2]
        self.stage()

    # saves the game on the launch pad then launches it, should probably check that it is in preflight before saving
    def launch(self) -> None:
        self.save()
        self.__stage -= 1
        self.control.activate_next_stage()
        self.score = 0
        self.control.sas = True
        self.control.sas_mode = self.control.sas_mode.stability_assist
        self.__parts = [(c._object_id, c.decouple_stage) for c in self.vessel.parts.all]
        self.__maxStage = self.__stage
        print(Monitor.this)
        #Monitor.this.runUpdate()
        return

    # wraps the save command
    def save(self): 
        self.conn.space_center.save("ProjectStart")

    # wraps the load command
    def load(self): 
        self.conn.space_center.load("ProjectStart")
        
    def __init__(self):
        # allows you to get pyautogui to stop if need be
        pyautogui.FAILSAFE = False
        self.conn = None
        self.tryToConnect()
        self.save()
        Monitor.this = Monitor()
        print(self.conn.krpc.get_status().version)
        self.kerbin = self.conn.space_center.bodies["Kerbin"]
        print(self.kerbin.name)
        self.vessel = self.conn.space_center.active_vessel
        self.control = self.vessel.control
        self.flight = self.vessel.flight(self.kerbin.reference_frame)
        self.sasEnum = self.vessel.control.sas_mode
        Ksp.__game = self
        self.score = 0

        # gets the current stage max decoupled stage for all parts connected different from current stage potentially
        self.__stage = max(c.decouple_stage for c in self.vessel.parts.all)
        self.__maxStage = self.__stage

        # stores a list of tuples of all the parts ids and decoupled stages
        self.__parts = [(c._object_id, c.decouple_stage) for c in self.vessel.parts.all]