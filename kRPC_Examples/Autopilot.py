import krpc
import sys

conn = krpc.connect(name='Autopilot script')
vessel = conn.space_center.active_vessel

# Set up autopilot
autopilot = vessel.auto_pilot
autopilot.engage()

# Takes two angles as command line input an sets autopilot to that bearing
autopilot.target_pitch_and_heading(float(sys.argv[1]), float(sys.argv[2]))

# Wait for maneuver to complete before exiting the script (will disable autopilot)
autopilot.wait()
autopilot.disengage()

# Enable SAS to hold bearing
vessel.control.sas = True
vessel.control.sas_mode = conn.space_center.SASMode.stability_assist