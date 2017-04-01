import krpc
import os
import time
from io import StringIO

def print_vessel_info(vessel, indent='\t'):
    left_col = 30
    # indent = '\t'

    print(indent, repr('Name: ').ljust(left_col), repr(vessel.name))
    print(indent, repr('Type: ').ljust(left_col), repr(vessel.type))
    print(indent, repr('Situation: ').ljust(left_col), repr(vessel.situation))
    print(indent, repr('Recoverable: ').ljust(left_col), repr(vessel.recoverable))
    print(indent, repr('MET: ').ljust(left_col), repr(vessel.met))
    print(indent, repr('Biome: ').ljust(left_col), repr(vessel.biome))
    # print(indent, repr('Flight OBJ: ').ljust(left_col), repr(vessel.flight()))
    # print(indent, repr('Orbit OBJ: ').ljust(left_col), repr(vessel.orbit))
    # print(indent, repr('Control OBJ: ').ljust(left_col), repr(vessel.control))
    # print(indent, repr('AutoPilot OBJ: ').ljust(left_col), repr(vessel.auto_pilot))
    # print(indent, repr('Resources OBJ: ').ljust(left_col), repr(vessel.resources))
    # print(indent, repr('StageResources OBJ: ').ljust(left_col), repr(vessel.resources_in_decouple_stage(0)))
    # print(indent, repr('Parts OBJ: ').ljust(left_col), repr(vessel.parts))
    print(indent, repr('Mass: ').ljust(left_col), repr(vessel.mass))
    print(indent, repr('Dry Mass: ').ljust(left_col), repr(vessel.dry_mass))
    print(indent, repr('Thrust: ').ljust(left_col), repr(vessel.thrust))
    print(indent, repr('Available Thrust: ').ljust(left_col), repr(vessel.available_thrust))
    print(indent, repr('Max Thrust: ').ljust(left_col), repr(vessel.max_thrust))
    print(indent, repr('Max Vac Thrust: ').ljust(left_col), repr(vessel.max_vacuum_thrust))
    print(indent, repr('ISP: ').ljust(left_col), repr(vessel.specific_impulse))
    print(indent, repr('Vac ISP: ').ljust(left_col), repr(vessel.vacuum_specific_impulse))
    print(indent, repr('Sea Lvl ISP: ').ljust(left_col), repr(vessel.kerbin_sea_level_specific_impulse))
    print(indent, repr('Moment of Inertia: ').ljust(left_col), repr(vessel.moment_of_inertia))
    print(indent, repr('Inertia Tensor: ').ljust(left_col), repr(vessel.inertia_tensor))
    print(indent, repr('Available Torque: ').ljust(left_col), repr(vessel.available_torque))
    print(indent, repr('Avail Rctn Whl Torque: ').ljust(left_col), repr(vessel.available_reaction_wheel_torque))
    print(indent, repr('Avail RCS Torque: ').ljust(left_col), repr(vessel.available_rcs_torque))
    print(indent, repr('Avail Engine Torque: ').ljust(left_col), repr(vessel.available_engine_torque))
    print(indent, repr('Avail Ctrl Surface Torque: ').ljust(left_col), repr(vessel.available_control_surface_torque))
    print(indent, repr('Avail Other Torque: ').ljust(left_col), repr(vessel.available_other_torque))
    print(indent, repr('Orbit Apoapsis: ').ljust(left_col), repr(vessel.orbit.apoapsis_altitude))
    print(indent, repr('Orbit Periapsis: ').ljust(left_col), repr(vessel.orbit.periapsis_altitude))
    # print(indent, repr('ReferenceFrame OBJ: ').ljust(left_col), repr(vessel.reference_frame))
    # print(indent, repr('OrbitalRefFrame OBJ: ').ljust(left_col), repr(vessel.orbital_reference_frame))
    # print(indent, repr('SurfaceRefFrame OBJ: ').ljust(left_col), repr(vessel.surface_reference_frame))
    # print(indent, repr('SurfaceVelocityRefFrame OBJ: ').ljust(left_col), repr(vessel.surface_velocity_reference_frame))

    # These attributes can be called with any reference frame. Most seem to always return 0, could be a bug
    # ref_frame = vessel.orbital_reference_frame
    # print(indent, repr('Position: ').ljust(left_col), repr(vessel.position(ref_frame)))
    # print(indent, repr('Bounding Box: ').ljust(left_col), repr(vessel.bounding_box(ref_frame)))
    # print(indent, repr('Velocity: ').ljust(left_col), repr(vessel.position(ref_frame)))
    # print(indent, repr('Rotation: ').ljust(left_col), repr(vessel.position(ref_frame)))
    # print(indent, repr('Direction: ').ljust(left_col), repr(vessel.position(ref_frame)))
    # print(indent, repr('Angular Velocity: ').ljust(left_col), repr(vessel.position(ref_frame)))

def print_flight_info(flight, indent='\t'):
    left_col = 30

    print(indent, repr('G Force: ').ljust(left_col), repr(flight.g_force))
    print(indent, repr('Mean Altitude: ').ljust(left_col), repr(flight.mean_altitude))
    print(indent, repr('Surface Altitude: ').ljust(left_col), repr(flight.surface_altitude))
    print(indent, repr('Bedrock Altitude: ').ljust(left_col), repr(flight.bedrock_altitude))
    print(indent, repr('Elevation: ').ljust(left_col), repr(flight.elevation))
    print(indent, repr('Latitude: ').ljust(left_col), repr(flight.latitude))
    print(indent, repr('Longitude: ').ljust(left_col), repr(flight.longitude))
    print(indent, repr('Velocity: ').ljust(left_col), repr(flight.velocity))
    print(indent, repr('Speed: ').ljust(left_col), repr(flight.speed))
    print(indent, repr('Horizontal Speed: ').ljust(left_col), repr(flight.horizontal_speed))
    print(indent, repr('Vertical Speed: ').ljust(left_col), repr(flight.vertical_speed))
    print(indent, repr('Center of Mass: ').ljust(left_col), repr(flight.center_of_mass))
    print(indent, repr('Rotation: ').ljust(left_col), repr(flight.rotation))
    print(indent, repr('Direction: ').ljust(left_col), repr(flight.direction))
    print(indent, repr('Pitch: ').ljust(left_col), repr(flight.pitch))


conn = krpc.connect(name='Display Info script')
vessel = conn.space_center.active_vessel

if __name__ == '__main__':
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print('VESSEL INFO:')
        print('----------------------------------------')
        print_vessel_info(vessel)

        print('\nFLIGHT INFO:')
        print('----------------------------------------')
        print_flight_info(vessel.flight())

        # Orbital speed appears to be the only one that works
        print('\n\t', repr('Orbital Speed: ').ljust(30), repr(vessel.orbit.speed))

        time.sleep(5)