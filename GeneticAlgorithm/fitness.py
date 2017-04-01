import time
import neat
from ksp import Ksp
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
        genome.fitness = Ksp.game.score
