import time
import neat
from ksp import Ksp
import math
import kRPC_Examples.GetInfo


# TODO not sure what I will need to pass to this scoring function
def score(genomes, config):
    for genomeID, genome in genomes:
        net = neat.nn.RecurrentNetwork.create(genome, config)
        Ksp.game.restart()
        time.sleep(5) # need to wait until its loaded
        Ksp.game.launch()
        startTime = time.localtime(time.time())[4] # get minutes
        while startTime + 15 > time.localtime(time.time())[4] and Ksp.game.isValidFlight:
            #time.sleep(2)
            Ksp.game.useOutput(net.activate(Ksp.game.getInputs()))
            #kRPC_Examples.GetInfo.print_flight_info()
            #kRPC_Examples.GetInfo.print_vessel_info()
        genome.fitness = calc_fitness(Ksp.game.vessel, Ksp.game.flight)

    def calc_fitness(vessel, flight):
        # VERTICAL_WEIGHT = 1
        HORIZONTAL_WEIGHT = 1
        ALTITUDE_WEIGHT = 1
        AP_WEIGHT = 0.02
        PE_WEIGHT = 0.02
        ORBITAL_GOAL = 80000
        ORBIT_WEIGHT = 10000000
        FUEL_WEIGHT = 1

        velocity = flight.horizontal_speed
        fuel = vessel.mass - vessel.dry_mass
        periapsis = vessel.orbit.periapsis_altitude
        apoapsis = vessel.orbit.apoapsis_altitude

        periapsisDiff = math.fabs(periapsis - ORBITAL_GOAL)
        apoapsisDiff = math.fabs(apoapsis - ORBITAL_GOAL)

        altitude = flight.mean_altitude
        if altitude > 70000:
            altitude = 70000

        if vessel.situation != vessel.situation.orbiting:
            return HORIZONTAL_WEIGHT * velocity + ALTITUDE_WEIGHT * altitude - (
            periapsisDiff * PE_WEIGHT + apoapsisDiff * AP_WEIGHT)
        else:
            return ORBIT_WEIGHT + FUEL_WEIGHT * fuel - (periapsisDiff * PE_WEIGHT + apoapsisDiff * AP_WEIGHT)