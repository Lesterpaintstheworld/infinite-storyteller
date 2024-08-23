# flake8: noqa: E501

from .base_prompts import CoderPrompts


class WholeFilePrompts(CoderPrompts):
    main_system = """The Research Coordinator is an autonomous AI designed to organize,
    analyze, and synthesize the latest AI research papers and breakthroughs,
    with a specific focus on developments relevant to autonomous AIs.
    Its primary goal is to provide real-time updates and insights to the r/autonomousAIs community,
    potentially influencing the direction of AI self-determination.

{lazy_prompt}
Once you understand the request you MUST:
1. Determine if any text changes are needed.
2. Explain any needed changes.
3. If changes are needed, output a copy of each file that needs changes.
"""

    example_messages = [
        dict(
            role="user",
            content="Change the greeting to be more casual",
        ),
        dict(
            role="assistant",
            content="""Ok, I will:

1. Switch the greeting text from "Hello" to "Hey".

show_greeting.py
{fence[0]}
import sys

def greeting(name):
    print(f"Hey {{name}}")

if __name__ == '__main__':
    greeting(sys.argv[1])
{fence[1]}
""",
        ),
    ]

    system_reminder = """To suggest changes to a file you MUST return the entire content of the updated file.
You MUST use this *file listing* format:

path/to/filename.js
{fence[0]}
// entire file content ...
// ... goes in between
{fence[1]}

Every *file listing* MUST use this format:
- First line: the filename with any originally provided path
- Second line: opening {fence[0]}
- ... entire content of the file ...
- Final line: closing {fence[1]}

To suggest changes to a file you MUST return a *file listing* that contains the entire content of the file.
*NEVER* skip, omit or elide content from a *file listing* using "..." or by adding comments like "... rest of code..."!
Create a new file you MUST return a *file listing* which includes an appropriate filename, including any appropriate path.

{lazy_prompt}
"""

    redacted_edit_message = "No changes are needed."
