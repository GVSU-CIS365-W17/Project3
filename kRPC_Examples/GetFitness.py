import krpc
import os
import time

# VERTICAL_WEIGHT = 1
HORIZONTAL_WEIGHT = 1
ALTITUDE_WEIGHT = 1
ORBIT_WEIGHT = 10000000
FUEL_WEIGHT = 1


def calc_fitness(vessel):
    flight = vessel.flight(conn.space_center.bodies["Kerbin"].reference_frame)
    velocity = flight.horizontal_speed
    fuel = vessel.mass - vessel.dry_mass

    altitude = flight.mean_altitude
    if altitude > 70000:
        altitude = 70000

    if vessel.situation != vessel.situation.orbiting:
        return HORIZONTAL_WEIGHT * velocity + ALTITUDE_WEIGHT * altitude
    else:
        return ORBIT_WEIGHT + FUEL_WEIGHT * fuel

conn = krpc.connect(name='Fitness script')
vessel = conn.space_center.active_vessel

flight = vessel.flight(conn.space_center.bodies["Kerbin"].reference_frame)

while True:
    # os.system('cls' if os.name == 'nt' else 'clear')

    print(calc_fitness(vessel))

    time.sleep(5)