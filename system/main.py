from system.core_loop.task_manager import TaskManager
from system.core_loop.task_executor import TaskExecutor
from system.world_simulation.world_state_manager import WorldStateManager
from system.story_generation.story_generator import StoryGenerator
from system.core_loop.feedback_analyzer import FeedbackAnalyzer

import openai
import time

class InfiniteStoryteller:
    def __init__(self):
        self.task_manager = TaskManager()
        self.task_executor = TaskExecutor()
        self.world_state_manager = WorldStateManager()
        self.story_generator = StoryGenerator()
        openai.api_key = "YOUR_OPENAI_API_KEY"  # Remplacez par votre clé API
        self.feedback_analyzer = FeedbackAnalyzer()

    def call_openai(self, prompt, context):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Vous êtes un assistant créatif pour la génération d'histoires."},
                    {"role": "user", "content": f"Contexte: {context}\n\nTâche: {prompt}"}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            print(f"Erreur lors de l'appel à OpenAI: {e}")
            return None

    def run(self):
        while True:
            task = self.task_manager.get_next_task()
            if task:
                context = self.world_state_manager.get_current_state()
                prompt = f"Générez une histoire basée sur la tâche suivante : {task.details}"
                
                openai_response = self.call_openai(prompt, context)
                
                if openai_response:
                    # Utilisez la réponse d'OpenAI pour générer l'histoire
                    story = self.story_generator.generate_story(task.details, openai_response)
                    
                    # Mettez à jour l'état du monde avec la nouvelle histoire
                    self.world_state_manager.update_state(task, story)
                    
                    # Exécutez la tâche avec l'histoire générée
                    self.task_executor.execute_task(task, story)
                else:
                    print("Impossible de générer une histoire. Passons à la tâche suivante.")
            else:
                print("Aucune tâche disponible. Attente...")
                time.sleep(60)  # Attendez une minute avant de vérifier à nouveau
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
