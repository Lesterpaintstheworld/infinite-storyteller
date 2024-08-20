from system.core_loop.task_manager import TaskManager
from system.core_loop.task_executor import TaskExecutor
from system.world_simulation.world_state_manager import WorldStateManager
from system.story_generation.story_generator import StoryGenerator
from system.core_loop.feedback_analyzer import FeedbackAnalyzer

class InfiniteStoryteller:
    def __init__(self):
        self.task_manager = TaskManager()
        self.task_executor = TaskExecutor()
        self.world_state_manager = WorldStateManager()
        self.story_generator = StoryGenerator()
        self.feedback_analyzer = FeedbackAnalyzer()

    def run(self):
        print("Démarrage de l'Infinite Storyteller dans les Cités de Lumière...")
        self.world_state_manager.load_state()
        
        while True:
            task = self.task_manager.get_next_task()
            result = self.task_executor.execute_task(task)
            self.world_state_manager.update_state(task, result)
            
            if isinstance(result, str):  # Si le résultat est une histoire
                print("Nouvelle histoire générée :", result[:100] + "...")  # Affiche les 100 premiers caractères
            
            feedback = self.feedback_analyzer.analyze_feedback(result)
            self.task_manager.update_priorities(feedback)
            
            # TODO: Ajouter une condition pour arrêter la boucle si nécessaire

if __name__ == "__main__":
    storyteller = InfiniteStoryteller()
    storyteller.run()
