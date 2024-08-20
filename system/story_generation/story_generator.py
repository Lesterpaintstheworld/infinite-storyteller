from .story import Story

class StoryGenerator:
    def __init__(self, asset_manager, task_manager, feedback_analyzer):
        self.asset_manager = asset_manager
        self.task_manager = task_manager
        self.feedback_analyzer = feedback_analyzer

    def generate_story(self, task_details):
        # Implement basic story generation logic
        story_elements = task_details.get('story_elements', ['default_element'])
        world_state = task_details.get('world_state', {})
        
        story = Story(story_elements, world_state, self.asset_manager, task_details, self.task_manager, self.feedback_analyzer)
        return story.generate()
