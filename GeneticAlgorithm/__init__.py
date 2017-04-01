# attempt to load a pickled resource file to load in the starting population
# If not pickled resource file then just create a new random population
# pass this population to the simulation. This should probably be a named tuple
import krpc
import time
import os
# from . import fitness
# from . import config
# from . import ksp
import neat

print(os.getcwd())
# while True:
#     print("Name: ", vessel.name)
#     parts = vessel.resources
#     print(parts.names)
#     print("Fuel", parts.amount("LiquidFuel"))
#     print("Throttle", vessel.control.throttle)
#     print("Available Thrust", vessel.available_thrust)
#     print("Max Thrust", vessel.max_thrust)
#     print("Velocity", vessel.velocity(kerbin.reference_frame))
#     print("Flight Velocity", flight.velocity)
#     print("Flight Speed", flight.speed)
#     print("Flight vert speed", flight.vertical_speed)
#     print("Flight horizontal speed", flight.horizontal_speed)
#     time.sleep(10)

#for v in conn.space_center.vessels:
#    print("Name: ", v.name)
#    v.control.throttle = 0
#    print("Throttle", v.control.throttle)
#    print("Avalible Thrust", v.available_thrust)
#    print("Max Thrust", v.max_thrust)
#    print("Staging")
#    v.control.activate_next_stage()
#    print("Avalible Thrust", v.available_thrust)
#    print("Max Thrust", v.max_thrust)
#print(conn.space_center.vessels)


def test(x:int):
    print(x)