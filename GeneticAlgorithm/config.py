import neat
import fitness

#TODO this method
def run(fileName:str):
    config = neat.Config(neat.DefaultGenome,neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, fileName)
    population = neat.Population(config)

    # Adding reporters so we have some output
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(5))

    population.run(fitness.score, 300)
    return