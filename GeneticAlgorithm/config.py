import neat
import fitness
import os
import reporter

#TODO this method
def run(fileName:str):
    config = neat.Config(neat.DefaultGenome,neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, fileName)
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-checkpoint-26')

    population = neat.Checkpointer.restore_checkpoint(config_path)

    # Adding reporters so we have some output
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(5))
    population.add_reporter(reporter.CustomReporter())

    population.run(fitness.score, 300)
    return