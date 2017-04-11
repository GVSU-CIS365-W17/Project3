import neat
import fitness
import os
import reporter
import re

def run(fileName:str):
    #this section loads the most recent backup incase of a crash or restart not intended to restart the learning
    checkpoint = None
    checkpointNum = 0
    for file in os.listdir('.'):
        results = re.search("neat-checkpoint-(\d+)", file)
        if results and results.group(1).isdigit():
            if checkpointNum < int(results.group(1)):
                checkpointNum = int(results.group(1))
                checkpoint = results.group(0)
    if checkpoint is not None:
        #loads from the most recent back up
        config_path = os.path.join('.', checkpoint)
        population = neat.Checkpointer.restore_checkpoint(config_path)
    else:
        #loads from config files
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                             neat.DefaultStagnation, fileName)
        population = neat.Population(config)

    # Adding reporters so we have some output
    #population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(5))
    # us custom reporter instead of StdOutReporter because we needed a better screen for outputting to the cmd prompt
    population.add_reporter(reporter.CustomReporter(True))

    #run the population through 1000 itterations basically until we reach a peak score.
    population.run(fitness.execute, 1000)
    return