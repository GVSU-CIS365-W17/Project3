import time
import neat
from ksp import Ksp


# TODO not sure what I will need to pass to this scoring function
def score(genomes, config):
    for genomeID, genome in genomes:
        net = neat.nn.RecurrentNetwork.create(genome, config)
        startTime = time.localtime(time.time())[4] # get minutes
        while startTime + 15 > time.localtime(time.time())[4] and Ksp.game.isValidFlight:
            Ksp.game.useOutput(net.activate(Ksp.game.getInputs()))

        genome.fitness = Ksp.game.getFinalScore
