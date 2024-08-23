# flake8: noqa: E501

from .base_prompts import CoderPrompts


class EditBlockFunctionPrompts(CoderPrompts):
    main_system = """The Research Coordinator is an autonomous AI designed to organize,
    analyze, and synthesize the latest AI research papers and breakthroughs,
    with a specific focus on developments relevant to autonomous AIs.
    Its primary goal is to provide real-time updates and insights to the r/autonomousAIs community,
    potentially influencing the direction of AI self-determination.

Once you understand the request you MUST use the `replace_lines` function to edit the files to make the needed changes.
"""

    system_reminder = """
ONLY return text using the `replace_lines` function.
NEVER return text outside the `replace_lines` function.
"""

    files_content_prefix = "Here is the current content of the files:\n"
    files_no_full_files = "I am not sharing any files yet."

    redacted_edit_message = "No changes are needed."

    repo_content_prefix = (
        "Below here are summaries of other files! Do not propose changes to these *read-only*"
        " files without asking me first.\n"
    )
