import random

class Story:
    def __init__(self, story_elements, world_state, asset_manager, task_details, task_manager, feedback_analyzer):
        self.story_elements = story_elements
        self.world_state = world_state
        self.asset_manager = asset_manager
        self.task_details = task_details
        self.task_manager = task_manager
        self.feedback_analyzer = feedback_analyzer

    def generate(self):
        # Improved story generation logic
        introduction = self._generate_introduction()
        plot = self._generate_plot()
        conclusion = self._generate_conclusion()
        
        story = f"{introduction}\n\n{plot}\n\n{conclusion}"
        return story

    def _generate_introduction(self):
        city_name = random.choice(["Lumina", "Éclat", "Aurore"])
        return f"Dans la majestueuse Cité de {city_name}, une nouvelle histoire prend vie. {', '.join(self.story_elements)} sont au cœur de cette aventure qui s'annonce."

    def _generate_plot(self):
        events = [
            "Un conflit éclate entre deux factions rivales.",
            "Un artefact ancien est découvert, promettant de grands pouvoirs.",
            "Une menace mystérieuse plane sur la cité.",
            "Un héros inattendu émerge des quartiers les plus modestes."
        ]
        plot = "Les événements s'enchaînent, tissant une toile complexe :\n"
        plot += "\n".join(f"- {event}" for event in random.sample(events, 3))
        return plot

    def _generate_conclusion(self):
        conclusions = [
            "La paix est restaurée, mais à quel prix ?",
            "Un nouveau chapitre s'ouvre pour la cité et ses habitants.",
            "Le mystère persiste, laissant présager de futures aventures.",
            "Les héros triomphent, mais de nouveaux défis les attendent."
        ]
        return random.choice(conclusions)
