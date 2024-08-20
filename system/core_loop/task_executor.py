from system.core_loop.task_manager import TaskManager
from system.services.world_state_manager import WorldStateManager
from system.services.feedback_analyzer import FeedbackAnalyzer
from system.story_generation.story_generator import StoryGenerator
from system.world_simulation.city_evolution import evolve_city
from system.world_simulation.event_scheduler import schedule_events

class TaskExecutor:
    def __init__(self, task_manager: TaskManager, world_state_manager: WorldStateManager, feedback_analyzer: FeedbackAnalyzer):
        self.task_manager = task_manager
        self.world_state_manager = world_state_manager
        self.feedback_analyzer = feedback_analyzer
        self.story_generator = StoryGenerator()

    def execute_task(self, task):
        """
        Execute the given task using appropriate system components.
        
        :param task: The task to be executed
        :return: Result of the task execution
        """
        task_type = task['type']
        task_details = task['details']

        if task_type == 'generate_story':
            result = self.story_generator.generate_story(task_details)
        elif task_type == 'evolve_city':
            result = evolve_city(task_details['city'], task_details['time_period'], task_details['events'])
        elif task_type == 'schedule_events':
            result = schedule_events(task_details['city'], task_details['time_period'])
        else:
            raise ValueError(f"Unknown task type: {task_type}")

        self.record_result(task, result)
        return result

    def record_result(self, task, result):
        """
        Record the results of task execution.
        
        :param task: The executed task
        :param result: The result of the task execution
        """
        self.world_state_manager.update_state(task, result)
        self.feedback_analyzer.analyze_task_result(task, result)
        self.task_manager.update_task_status(task['id'], 'completed')

    def run_core_loop(self):
        """
        Run the core loop of the system.
        """
        while True:
            next_task = self.task_manager.get_next_task()
            if next_task:
                self.execute_task(next_task)
            else:
                # No more tasks, exit the loop
                break

    def get_task_handler(self, task_type):
        """
        Retrieve the appropriate handler for a given task type.
        
        :param task_type: The type of the task
        :return: The task handler
        """
        handlers = {
            'generate_story': self.story_generator.generate_story,
            'evolve_city': evolve_city,
            'schedule_events': schedule_events,
        }
        return handlers.get(task_type, None)
