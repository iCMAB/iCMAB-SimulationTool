from mapek import Knowledge, Monitor, Analyzer, Planner, Executer
from subject import ACVUpdater
from ml_models import MODELS

from config import get_config

def run_simulation():
    """Runs the ACV simulation."""
    
    model = select_model()

    d = get_config('mab', 'd')
    alpha = get_config('mab', 'alpha')
    epsilon = get_config('mab', 'epsilon')
    n_arms = get_config('acvs', 'num_acvs') - 1
    n_bootstrap = get_config('mab', 'n_bootstrap')
    ideal_distance = get_config('acvs', 'ideal_distance') 

    knowledge = Knowledge()
    
    knowledge.ideal_distance = ideal_distance
    knowledge.mab_model = model(
        d = d,
        n_arms = n_arms, 
        ideal_distance = ideal_distance,
        alpha = alpha, 
        epsilon = epsilon, 
        n_bootstrap = n_bootstrap,
    )

    num_sim_runs = get_config('simulation', 'num_simulation_runs')
    for _ in range(num_sim_runs):
        updater = ACVUpdater()
        executer = Executer(updater)
        planner = Planner(executer)
        analyzer = Analyzer(planner)
        monitor = Monitor(analyzer)

        updater.register(monitor)
        updater.run_update_loop()

def select_model():
    """Selects the model to use for the simulation."""

    print("\nSelect a model:")
    print(get_config('output', 'minor_divider'))
    
    for i, model in enumerate(MODELS):
        print(f"{i + 1}. {model[0]}")

    print()

    selection = ""
    while (not selection.isdigit()) or (int(selection) not in range(1, len(MODELS) + 1)):
        selection = input("Selection: ")

    return MODELS[int(selection) - 1][1]


if __name__ == '__main__':
    run_simulation()
