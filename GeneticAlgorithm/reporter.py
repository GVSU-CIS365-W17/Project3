import neat.reporting
from neat.six_util import itervalues, iterkeys

class CustomReporter(neat.reporting.StdOutReporter):
    previousGeneration = None
    def post_reproduction(self, config, population, species):
        super().post_reproduction(config, population, species)

    def found_solution(self, config, generation, best):
        super().found_solution(config, generation, best)

    def start_generation(self, generation):
        super().start_generation(generation)

    def post_evaluate(self, config, population:neat.Population, species, best_genome):
        super().post_evaluate(config, population, species, best_genome)
            
    def end_generation(self, config, population, species_set):
        ng = len(population)
        ns = len(species_set.species)
        if self.show_species_detail:
            sp.call('cls',shell=True)
            StdOutReporter.previousGeneration = ""
            StdOutReporter.previousGeneration += 'Population of {0:d} members in {1:d} species:'.format(ng, ns) + os.linesep
            sids = list(iterkeys(species_set.species))
            sids.sort()
            StdOutReporter.previousGeneration += "   ID   age  size  fitness  adj fit  stag" + os.linesep
            StdOutReporter.previousGeneration += "  ====  ===  ====  =======  =======  ====" + os.linesep
            for sid in sids:
                s = species_set.species[sid]
                a = self.generation - s.created
                n = len(s.members)
                f = "--" if s.fitness is None else "{:.1f}".format(s.fitness)
                af = "--" if s.adjusted_fitness is None else "{:.3f}".format(s.adjusted_fitness)
                st = self.generation - s.last_improved
                StdOutReporter.previousGeneration += "  {: >4}  {: >3}  {: >4}  {: >7}  {: >7}  {: >4}".format(sid, a, n, f, af, st) + os.linesep
        else:
            print('Population of {0:d} members in {1:d} species'.format(ng, ns))
        
        print(StdOutReporter.previousGeneration)
        elapsed = time.time() - self.generation_start_time
        self.generation_times.append(elapsed)
        self.generation_times = self.generation_times[-10:]
        average = sum(self.generation_times) / len(self.generation_times)
        print('Total extinctions: {0:d}'.format(self.num_extinctions))
        if len(self.generation_times) > 1:
            print("Generation time: {0:.3f} sec ({1:.3f} average)".format(elapsed, average))
        else:
            print("Generation time: {0:.3f} sec".format(elapsed))

    def complete_extinction(self):
        super().complete_extinction()

    def info(self, msg):
        super().info(msg)

    def species_stagnant(self, sid, species):
        super().species_stagnant(sid, species)

    def end_generation(self, config, population, species):
        super().end_generation(config, population, species)