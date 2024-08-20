import json
from queue import PriorityQueue

class Task:
    def __init__(self, task_type, details, priority):
        self.task_type = task_type
        self.details = details
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

class TaskManager:
    def __init__(self):
        self.task_queue = PriorityQueue()
        self.load_task_templates()

    def load_task_templates(self):
        # TODO: Implémenter le chargement des modèles de tâches depuis les fichiers JSON
        pass

    def create_task(self, task_type, details, priority=None):
        if priority is None:
            priority = self.calculate_priority(task_type, details)
        task = Task(task_type, details, priority)
        self.task_queue.put(task)

    def get_next_task(self):
        if not self.task_queue.empty():
            return self.task_queue.get()
        else:
            return None

    def update_priorities(self, adjustments):
        # TODO: Implémenter la mise à jour des priorités basée sur les ajustements
        pass

    def calculate_priority(self, task_type, details):
        # TODO: Implémenter un algorithme de calcul de priorité basé sur le type de tâche et les détails
        return 1  # Priorité par défaut
