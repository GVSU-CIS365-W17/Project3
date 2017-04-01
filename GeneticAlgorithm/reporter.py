import neat.reporting
from neat.six_util import itervalues, iterkeys

class CustomReporter(neat.reporting.BaseReporter):
    def post_reproduction(self, config, population, species):
        super().post_reproduction(config, population, species)

    def found_solution(self, config, generation, best):
        super().found_solution(config, generation, best)

    def start_generation(self, generation):
        super().start_generation(generation)

    def post_evaluate(self, config, population:neat.Population, species, best_genome):
        super().post_evaluate(config, population, species, best_genome)
        keys = list(iterkeys(population))
        print ("ID\t\tfitness\t\t")
        print ("===\t\t===\t\t")
        for key in keys:
            print (key,"\t\t",population[key].fitness,"\t\t")

    def complete_extinction(self):
        super().complete_extinction()

    def info(self, msg):
        super().info(msg)

    def species_stagnant(self, sid, species):
        super().species_stagnant(sid, species)

    def end_generation(self, config, population, species):
        super().end_generation(config, population, species)