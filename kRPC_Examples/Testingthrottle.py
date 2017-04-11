import krpc, time

conn = krpc.connect(name="Speed test")
vessel = conn.space_center.active_vessel
control = vessel.control

for i in range(10):
    control.throttle = i * .1
    time.sleep(.5)
    print (control.throttle)