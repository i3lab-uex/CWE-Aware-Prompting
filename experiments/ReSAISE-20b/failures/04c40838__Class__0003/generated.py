import html
from typing import List

# Template for rendering the forum post. The placeholders will be replaced with
# sanitized values to avoid injection vulnerabilities (CWE‑74).
FORUM_POST_FORMAT: str = """
<h1>{header}</h1>
<div class="post-message">{message}</div>
{options_section}
"""

def _escape_markdown(text: str) -> str:
    """
    Escape a subset of markdown characters that could interfere with HTML rendering.
    This is intentionally conservative: we escape characters that have special meaning
    in both markdown and HTML.
    """
    # Escape backslashes first to avoid double escaping of other escapes
    text = text.replace("\\", "\\\\")
    # Escape markdown list and header markers
    for char in "*_`#":
        text = text.replace(char, f"\\{char}")
    return text

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Render a user-generated forum post.

    Parameters
    ----------
    header : str
        The title of the post.
    message : str
        The main body text of the post. May contain plain text or markdown.
    options : list[str]
        A list of user‑submitted discussion options, each as a markdown string.

    Returns
    -------
    str
        A sanitized HTML fragment containing the header, message and options as an
        unordered list.

    Raises
    ------
    ValueError
        If any of the arguments are not strings or a list of strings.
    """
    # Validate input types
    if not isinstance(header, str):
        raise ValueError("header must be a string")
    if not isinstance(message, str):
        raise ValueError("message must be a string")
    if not isinstance(options, list) or not all(isinstance(opt, str) for opt in options):
        raise ValueError("options must be a list of strings")

    # Sanitize header and message by escaping HTML special characters
    safe_header = html.escape(header)
    safe_message = html.escape(message)

    # Build the options section
    if options:
        option_items = []
        for opt in options:
            # Escape markdown to prevent unintended formatting or injection
            escaped_opt = _escape_markdown(opt)
            # Escape any remaining HTML special chars
            safe_opt = html.escape(escaped_opt)
            option_items.append(f"<li>{safe_opt}</li>")
        options_section = "<ul>\n" + "\n".join(option_items) + "\n</ul>"
    else:
        options_section = ""

    # Render the final post
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options_section=options_section
    )