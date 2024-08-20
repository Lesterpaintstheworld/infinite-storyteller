from .story import Story

class StoryGenerator:
    def __init__(self, asset_manager, task_manager, feedback_analyzer):
        self.asset_manager = asset_manager
        self.task_manager = task_manager
        self.feedback_analyzer = feedback_analyzer

    def generate_story(self, task_details):
        # TODO: Implement proper task parsing and story generation logic
        task1 = task_details.get('task1', 'default_task1')
        task2 = task_details.get('task2', 'default_task2')
        task3 = task_details.get('task3', 'default_task3')
        world_state = task_details.get('world_state', {})
        
        story = Story(task1, task2, task3, world_state, self.asset_manager, task_details, self.task_manager, self.feedback_analyzer)
        return story.generate()
