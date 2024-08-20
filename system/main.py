from system.core_loop.task_manager import TaskManager
from system.core_loop.task_executor import TaskExecutor
from system.world_simulation.world_state_manager import WorldStateManager
from system.story_generation.story_generator import StoryGenerator

class InfiniteStoryteller:
    def __init__(self):
        self.task_manager = TaskManager()
        self.task_executor = TaskExecutor()
        self.world_state_manager = WorldStateManager()
        self.story_generator = StoryGenerator()

    def run(self):
        print("Démarrage de l'Infinite Storyteller...")
        self.world_state_manager.load_state()
        
        while True:
            task = self.task_manager.get_next_task()
            if task:
                result = self.task_executor.execute_task(task)
                self.world_state_manager.update_state(task, result)
                
                if isinstance(result, str):
                    print("Nouvelle histoire générée :", result[:100] + "...")  # Affiche les 100 premiers caractères
            else:
                print("Aucune tâche disponible. En attente...")
                # TODO: Ajouter une pause ou une condition de sortie

def main():
    storyteller = InfiniteStoryteller()
    storyteller.run()

if __name__ == "__main__":
    main()
