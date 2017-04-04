import time
import neat
from ksp import Ksp
from monitor import Monitor
import math


def calc_fitness(vessel, flight):
    # VERTICAL_WEIGHT = 1
    HORIZONTAL_WEIGHT = 0
    ALTITUDE_WEIGHT = 1
    AP_WEIGHT = 0.001
    PE_WEIGHT = 0.0005
    ORBITAL_GOAL = 80000
    ORBIT_WEIGHT = 50
    FUEL_WEIGHT = 1

    velocity = flight.horizontal_speed
    fuel = vessel.mass - vessel.dry_mass
    periapsis = vessel.orbit.periapsis_altitude
    apoapsis = vessel.orbit.apoapsis_altitude

    periapsisDiff = math.fabs(periapsis - ORBITAL_GOAL)
    apoapsisDiff = math.fabs(apoapsis - ORBITAL_GOAL)

    altitude = flight.mean_altitude
    Monitor.this.setMaxAlt(altitude)
    Monitor.this.setMaxPeriapsis(periapsis)
    Monitor.this.setMaxApoapsis(apoapsis)
    if altitude > 70000:
        altitude = 70000
    score = None
    if vessel.situation != vessel.situation.orbiting:
        score = HORIZONTAL_WEIGHT * velocity + ALTITUDE_WEIGHT * altitude - (
            periapsisDiff * PE_WEIGHT + apoapsisDiff * AP_WEIGHT)
        score /= 10000
    else:
        score = ORBIT_WEIGHT + FUEL_WEIGHT * fuel - (periapsisDiff * PE_WEIGHT + apoapsisDiff * AP_WEIGHT)
    Monitor.this.setMaxScore(score)
    return score

def execute(genomes, config):
    for genomeID, genome in genomes:
        net = neat.nn.RecurrentNetwork.create(genome, config)
        Ksp.game.restart()
        time.sleep(5) # need to wait until its loaded
        Ksp.game.launch()
        while Ksp.game.isValidFlight:
            #time.sleep(2)
            Ksp.game.useOutput(net.activate(Ksp.game.getInputs()))
            #kRPC_Examples.GetInfo.print_flight_info()
            #kRPC_Examples.GetInfo.print_vessel_info()
        genome.fitness = calc_fitness(Ksp.game.vessel, Ksp.game.flight)