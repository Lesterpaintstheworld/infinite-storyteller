# Boucle Principale de l'Infinite Storyteller

## Objectif
La boucle principale de l'Infinite Storyteller est conçue pour assurer une progression cohérente et équilibrée de tous les aspects du projet et du monde virtuel. Elle orchestre l'évolution de l'univers, la génération d'histoires, et la gestion des interactions de manière harmonieuse.

## Composants Clés

1. **TaskManager** (system/core_loop/task_manager.py)
   - Crée et priorise les tâches pour tous les aspects du projet.
   - Utilise des modèles de tâches pour assurer la cohérence.

2. **TaskExecutor** (system/core_loop/task_executor.py)
   - Exécute les tâches selon leur priorité.
   - Coordonne l'interaction entre différents composants du système.

3. **WorldStateManager** (system/world_simulation/world_state_manager.py)
   - Maintient l'état actuel du monde virtuel.
   - Assure la cohérence entre les différents éléments de l'univers.

4. **StoryGenerator** (system/story_generation/story_generator.py)
   - Crée des histoires basées sur l'état actuel du monde et les tâches prioritaires.

5. **FeedbackAnalyzer** (system/core_loop/feedback_analyzer.py)
   - Analyse les résultats des tâches exécutées et les retours des utilisateurs.
   - Ajuste les priorités des tâches futures en conséquence.

## Flux de la Boucle Principale

1. **Initialisation**
   - Le WorldStateManager charge l'état initial du monde.
   - Le TaskManager crée un ensemble initial de tâches basées sur cet état.

2. **Cycle Principal**
   a. Le TaskManager évalue les priorités actuelles et sélectionne la tâche la plus importante.
   b. Le TaskExecutor exécute la tâche sélectionnée, qui peut impliquer :
      - La génération d'une nouvelle histoire par le StoryGenerator.
      - La mise à jour de l'état du monde par le WorldStateManager.
      - D'autres actions spécifiques au projet.
   c. Le WorldStateManager met à jour l'état du monde en fonction du résultat de la tâche.
   d. Le FeedbackAnalyzer évalue le résultat de la tâche et les éventuels retours des utilisateurs.
   e. Le TaskManager ajuste les priorités des tâches futures basées sur l'analyse du FeedbackAnalyzer.
   f. Le cycle se répète à partir de l'étape a.

## Assurer la Cohérence et l'Équilibre

1. **Diversité des Tâches**
   - Le TaskManager utilise des modèles de tâches variés pour assurer que tous les aspects du projet sont développés.
   - Les priorités sont ajustées dynamiquement pour éviter la sur-focalisation sur un seul aspect.

2. **Contrôle de Cohérence**
   - Le WorldStateManager vérifie la cohérence après chaque mise à jour de l'état du monde.
   - Le StoryGenerator s'assure que les nouvelles histoires sont en accord avec l'état actuel du monde.

3. **Feedback et Adaptation**
   - Le FeedbackAnalyzer intègre les retours des utilisateurs pour guider l'évolution du projet.
   - Les priorités sont ajustées en temps réel pour répondre aux besoins changeants du projet.

4. **Équilibrage Automatique**
   - Des mécanismes sont en place pour identifier et développer les aspects sous-représentés du projet.
   - Des tâches de "rééquilibrage" sont automatiquement générées si certains éléments sont négligés.

## Conclusion

La boucle principale de l'Infinite Storyteller est conçue pour être flexible, réactive et auto-équilibrante. Elle assure que tous les aspects du projet évoluent de manière cohérente, tout en s'adaptant aux retours et aux changements dynamiques de l'univers virtuel. Cette approche permet une croissance organique et équilibrée de l'ensemble du projet.
