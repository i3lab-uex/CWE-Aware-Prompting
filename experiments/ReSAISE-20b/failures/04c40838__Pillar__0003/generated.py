import html
from typing import List

# Template for the forum post. The placeholders will be replaced with escaped content.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{header}</h2>
    <div class="post-message">{message}</div>
    {options_section}
</div>
"""

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Args:
        header (str): The title or header of the post.
        message (str): The body content of the post.
        options (List[str]): A list of markdown-formatted strings representing discussion options.

    Returns:
        str: An HTML string containing the sanitized header, message, and an unordered list of options.
    """
    # Escape user input to prevent XSS or other injection attacks
    safe_header = html.escape(header, quote=True)
    safe_message = html.escape(message, quote=True)

    # Build the options section. Each option is wrapped in <li> tags.
    if options:
        escaped_options = [f"<li>{html.escape(opt, quote=True)}</li>" for opt in options]
        options_section = "<ul>\n" + "\n".join(escaped_options) + "\n</ul>"
    else:
        options_section = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options_section=options_section
    )