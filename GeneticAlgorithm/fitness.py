import time, sys, os
import neat
from ksp import Ksp
import krpc
from monitor import Monitor
import reporter
import math
import subprocess
import pyautogui
import traceback

def calc_fitness(vessel, flight):
    # VERTICAL_WEIGHT = 1
    HORIZONTAL_WEIGHT = 0
    ALTITUDE_WEIGHT = 1
    AP_WEIGHT = 0.001
    PE_WEIGHT = 0.001
    ORBITAL_GOAL = 80000
    ORBIT_WEIGHT = 51
    FUEL_WEIGHT = 1

    velocity = flight.horizontal_speed
    fuel = vessel.mass - vessel.dry_mass
    periapsis = vessel.orbit.periapsis_altitude
    apoapsis = vessel.orbit.apoapsis_altitude

    periapsisDiff = math.fabs(periapsis - ORBITAL_GOAL)
    apoapsisDiff = math.fabs(apoapsis - ORBITAL_GOAL)
    
    # potentially another scoring option
    # 100 - abs(80-apoapsis[km])- (eccentricity * 10)
    
    if flight.vertical_speed > 0:
        altitude = flight.mean_altitude
    else:
        altitude = apoapsis
    Monitor.this.setMaxAlt(altitude)
    Monitor.this.setMaxPeriapsis(periapsis)
    Monitor.this.setMaxApoapsis(apoapsis)
    try:
        file = open("logs.lg", "a")
        file.write(str(apoapsis))
        file.write(",")
        file.write(str(periapsis))
        file.write(",")
        file.write(str(altitude))
        file.write(",")
    except:
        print("Failed to log")
    finally:
        file.close()
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

def tryToConnectStatic():
    conn = None
    for i in range(5):
        try:
            conn = krpc.connect(name="Genetics")
            break
        except:
            conn = None
    if conn is None:
        return None
    return conn.krpc.current_game_scene
    
def execute(genomes, config):
    averages = []
    if Ksp.APP == None:
        startKsp()
    for genomeID, genome in genomes:
        try:
            averages.append(runGenome(genome, config, sum(averages)/float(len(averages)) if len(averages) > 0 else 100000))
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            startKsp()
            averages.append(runGenome(genome, config, sum(averages)/float(len(averages)) if len(averages) > 0 else 100000))
        genome.fitness = calc_fitness(Ksp.game.vessel, Ksp.game.flight)
        subprocess.call('cls',shell=True)
        print("Fitness: ", genome.fitness)
        print(Ksp.death)
        print(reporter.CustomReporter.previousGeneration)
        try:
            file = open("logs.lg", "a")
            file.write(str(genome.fitness))
            file.write(str(os.linesep))
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            print("failed to log")
        finally:
            file.close()
    if averages[-1] > 1.1 * sum(averages)/float(len(averages)):
        print("Restart required")
        startKsp()
    try:
        Ksp.game.reloadGame()
    except:
        startKsp()
    
def runGenome(genome, config, average, previouslyFailed = False):
    restartRequired = 0
    net = neat.nn.RecurrentNetwork.create(genome, config)
    Ksp.game.reconnect()
    Ksp.game.restart()
    time.sleep(5)
    Ksp.game.launch()
    times = []
    time.sleep(0.001)
    print(neat.StdOutReporter.previousGeneration)
    while Ksp.game.isValidFlight:
        try:
            start = time.time()
            Ksp.game.useOutput(net.activate(Ksp.game.getInputs()))
            times.append(time.time() - start)
            #print(times[-1])
            if times[-1] > average * 2:
                restartRequired += 1
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            restartRequired = previouslyFailed =  True
            break
    if restartRequired > len(times)*0.25 and not previouslyFailed:
        print("Previous genome experienced heavy lag, reloading game and running genome again")
        try:
            Ksp.game.reloadGame()
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            startKsp()
        return runGenome(genome, config, average * 1.05, True)
    elif restartRequired and previouslyFailed:
        print("Previous genome experienced heavy lag, restarting Ksp and running genome again")
        startKsp()
        return runGenome(genome, config, average * 1.05, True)
    return sum(times)/float(len(times)) if len(times) > 0 else 1
    
def killKsp():
    if Ksp.APP is not None:
        print("Restarting Ksp")
        Ksp.APP.terminate()
    else:
        print("Ksp is either not running or we lost it somehow\nHopefully its just dead")

def startKsp(loadTime = 80, trys = 0):
    startButton = (518, 529)
    resumeButton = (647, 457)
    AI2 = (784, 404)
    loadButton = (995, 771)
    if Ksp.APP is not None:
        killKsp()
    print("Starting Ksp")
    Ksp.APP = subprocess.Popen("C:\\SteamFiles\\Steam\\steamapps\\common\\Kerbal Space Program\\KSP_x64.exe")
    print ("Waiting: ", loadTime, "to click start")
    time.sleep(loadTime)
    print("Clicking Start Button")
    Ksp.click(startButton)
    time.sleep(5)
    print("Clicking resumeButton")
    Ksp.click(resumeButton)
    time.sleep(2)
    print("Clicking ai2")
    Ksp.click(AI2)
    time.sleep(0.5)
    print("clicking load button")
    Ksp.click(loadButton)
    print("Going to attempt to connect")
    gameScene = tryToConnectStatic()
    if gameScene is not None:
        time.sleep(0.5)
        Ksp.goToLaunchPad()
    elif trys > 5:
        print("Failed to restart after 5 tries exiting and waiting for Nonprofitgibi to fix")
        sys.exit(1)
    else:
        print("Failed to restart correctly trying again with more time")
        return startKsp(loadTime + 10, trys + 1)