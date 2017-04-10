import fitness
import config
import ksp
import os

if __name__ == '__main__':
    fitness.startKsp()
    print("post Start")
    ksp.Ksp.game = ksp.Ksp()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'NeatConfig.cfg')
    config.run(config_path)