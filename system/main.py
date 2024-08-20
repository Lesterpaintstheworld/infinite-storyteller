import time
import os
from system.core_loop.task_manager import TaskManager
from system.core_loop.task_executor import TaskExecutor
from system.core_loop.feedback_analyzer import FeedbackAnalyzer

from system.world_simulation.world_state_manager import WorldStateManager
from assets.asset_manager import AssetManager
from .story_generation.story_generator import StoryGenerator

class InfiniteStoryteller:
    def __init__(self):
        self.task_manager = TaskManager()
        self.feedback_analyzer = FeedbackAnalyzer()
        self.world_state_manager = WorldStateManager()
        self.asset_manager = AssetManager(os.path.join(os.path.dirname(__file__), '..', '..', 'assets'))
        self.story_generator = StoryGenerator(self.asset_manager, self.task_manager, self.feedback_analyzer)
        
        self.task_executor = TaskExecutor(self.task_manager, self.feedback_analyzer, self.world_state_manager, self.story_generator)

    def run(self):
        """
        Main loop of the Infinite Storyteller system.
        """
        print("Démarrage du système Infinite Storyteller dans les Cités de Lumière...")
        try:
            while True:
                # Créer et prioriser les tâches
                task = self.task_manager.create_task("default_task", {"description": "Tâche par défaut"})
                
                if task:
                    # Exécuter la tâche de plus haute priorité
                    result = self.task_executor.execute_task(task)
                    
                    # Analyser le feedback et ajuster les priorités
                    feedback = self.get_feedback()
                    analysis = self.feedback_analyzer.analyze_feedback(feedback)
                    adjustments = self.feedback_analyzer.adjust_priorities(analysis)
                    
                    # Mettre à jour les priorités des tâches en fonction du feedback
                    self.task_manager.update_priorities(adjustments)
                    
                    # Mettre à jour l'état du monde
                    self.world_state_manager.update_state(task, result)
                    
                    print(f"Tâche exécutée : {task['type']}")
                else:
                    print("Aucune tâche à exécuter. En attente...")
                    time.sleep(5)  # Attendre 5 secondes avant de vérifier de nouvelles tâches
        except KeyboardInterrupt:
            print("Arrêt du système Infinite Storyteller...")
        finally:
            self.cleanup()

    def get_feedback(self):
        """
        Collecter le feedback de diverses sources.
        Cette méthode devrait être implémentée pour recueillir le feedback des lecteurs, les métriques du système, etc.
        """
        # TODO: Implémenter la collecte de feedback
        return {}

    def cleanup(self):
        """
        Effectuer les opérations de nettoyage nécessaires avant l'arrêt.
        """
        # Sauvegarder l'état du monde
        self.world_state_manager.save_state()
        # Sauvegarder l'état de l'analyseur de feedback
        self.feedback_analyzer.export_analysis('feedback_analysis.json')
        print("État du système sauvegardé. Arrêt terminé.")

if __name__ == "__main__":
    storyteller = InfiniteStoryteller()
    storyteller.run()
