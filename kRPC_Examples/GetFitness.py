import krpc
import os
import time
import math

# VERTICAL_WEIGHT = 1
HORIZONTAL_WEIGHT = 0
ALTITUDE_WEIGHT = 1
AP_WEIGHT = 0.02
PE_WEIGHT = 0.02
ORBITAL_GOAL = 80000
ORBIT_WEIGHT = 50
FUEL_WEIGHT = 1


def calc_fitness(vessel):
    flight = vessel.flight(conn.space_center.bodies["Kerbin"].reference_frame)
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
        return (HORIZONTAL_WEIGHT * velocity + ALTITUDE_WEIGHT * altitude - (periapsisDiff * PE_WEIGHT + apoapsisDiff * AP_WEIGHT))/10000
    else:
        return ORBIT_WEIGHT + FUEL_WEIGHT * fuel - (periapsisDiff * PE_WEIGHT + apoapsisDiff * AP_WEIGHT)

conn = krpc.connect(name='Fitness script')
vessel = conn.space_center.active_vessel

flight = vessel.flight(conn.space_center.bodies["Kerbin"].reference_frame)

while True:
    # os.system('cls' if os.name == 'nt' else 'clear')

    print(calc_fitness(vessel))

    time.sleep(5)