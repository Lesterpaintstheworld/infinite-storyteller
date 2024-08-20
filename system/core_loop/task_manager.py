import uuid
from queue import PriorityQueue

class TaskManager:
    def __init__(self):
        self.task_queue = PriorityQueue()

    def create_task(self, task_type, details, priority=None):
        """
        Create a new task based on the current state of the universe and system needs.
        
        :param task_type: Type of the task
        :param details: Additional details for the task
        :param priority: Priority of the task (if not provided, will be assigned automatically)
        :return: Created task object
        """
        task_id = str(uuid.uuid4())
        task = {
            'id': task_id,
            'type': task_type,
            'details': details,
            'status': 'pending'
        }
        
        if priority is None:
            priority = self.assign_priority(task)
        
        task['priority'] = priority
        self.add_task(task)
        return task

    def assign_priority(self, task):
        """
        Assign priority to a task based on its importance and urgency.
        
        :param task: The task to assign priority to
        :return: Assigned priority value
        """
        # Implement a more sophisticated priority assignment logic
        base_priority = 5
        
        # Adjust priority based on task type
        if task['type'] == 'story_task':
            base_priority += 2
        elif task['type'] == 'character_task':
            base_priority += 1
        
        # Adjust priority based on task details
        if 'urgency' in task['details']:
            base_priority += task['details']['urgency']
        
        # Ensure priority is within bounds
        return max(1, min(base_priority, 10))

    def add_task(self, task):
        """
        Add a task to the priority queue.
        
        :param task: The task to be added
        """
        self.task_queue.put((-task['priority'], task))

    def get_next_task(self):
        """
        Get the next highest priority task from the queue.
        
        :return: The next task, or None if the queue is empty
        """
        if not self.task_queue.empty():
            return self.task_queue.get()[1]
        return None

    def update_task_priority(self, task_id, new_priority):
        """
        Update the priority of a task in the queue.
        
        :param task_id: The ID of the task to update
        :param new_priority: The new priority value
        """
        # Create a new queue to hold tasks temporarily
        temp_queue = PriorityQueue()
        
        while not self.task_queue.empty():
            priority, task = self.task_queue.get()
            if task['id'] == task_id:
                task['priority'] = new_priority
                temp_queue.put((-new_priority, task))
            else:
                temp_queue.put((priority, task))
        
        # Replace the original queue with the updated one
        self.task_queue = temp_queue

    def remove_task(self, task_id):
        """
        Remove a task from the queue.
        
        :param task_id: The ID of the task to remove
        """
        temp_queue = PriorityQueue()
        
        while not self.task_queue.empty():
            priority, task = self.task_queue.get()
            if task['id'] != task_id:
                temp_queue.put((priority, task))
        
        self.task_queue = temp_queue

    def get_tasks_by_type(self, task_type):
        """
        Get all tasks of a specific type.
        
        :param task_type: The type of tasks to retrieve
        :return: A list of tasks of the specified type
        """
        tasks = []
        temp_queue = PriorityQueue()
        
        while not self.task_queue.empty():
            priority, task = self.task_queue.get()
            if task['type'] == task_type:
                tasks.append(task)
            temp_queue.put((priority, task))
        
        self.task_queue = temp_queue
        return tasks

# Add more methods as needed for task management
