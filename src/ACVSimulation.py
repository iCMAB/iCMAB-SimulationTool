import subject

from mapek.Knowledge import Knowledge
from mapek.Monitor import Monitor
from mapek.Analyzer import Analyzer
from mapek.Planner import Planner
from mapek.Executer import Executer
from subject.ACVUpdater import ACVUpdater

from ml_models.linearUCB import LinearUCB
from ml_models.linearTS import LinearThompsonSampling

model_options = [
    ('LinearUCB', LinearUCB), 
    ('LinearThompsonSampling', LinearThompsonSampling)
]

def run_simulation():
    """Runs the ACV simulation."""
    
    knowledge = Knowledge()
    knowledge.ideal_distance = subject.IDEAL_DISTANCE
    model = select_model()      

    d = 1
    alpha = 0.1
    knowledge.model = model(d=d, alpha=alpha)

    updater = ACVUpdater()
    
    executer = Executer(updater)
    planner = Planner(executer)
    analyzer = Analyzer(planner)
    monitor = Monitor(analyzer)

    updater.register(monitor)
    updater.read_data()

def select_model():
    """Selects the model to use for the simulation."""
    
    print("\nSelect a model:\n")
    for i, model in enumerate(model_options):
        print(f"{i + 1}. {model[0]}")

    selection = int(input("\nSelection: "))
    return model_options[selection - 1][1]

if __name__ == '__main__':
    run_simulation()