import html
from typing import List

# Template for a forum post. The placeholders {header}, {message} and {options}
# will be replaced with the sanitized content.  The options are wrapped in an
# unordered list (<ul>) so that any markdown is rendered as plain text.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<div class="post-body">{message}</div>
{options}
"""

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Render a user‑generated forum post.

    Parameters
    ----------
    header : str
        The title of the post.
    message : str
        The body text of the post.
    options : list[str]
        A list of user‑submitted discussion options.  Each option is assumed to
        be in markdown format but will be escaped before rendering.

    Returns
    -------
    str
        A sanitized HTML string containing the header, message and options.
    """
    # Escape all user input to prevent injection attacks (CWE‑74).
    safe_header = html.escape(header, quote=True)
    safe_message = html.escape(message, quote=True)

    # Convert options into an unordered list.  Each option is escaped.
    if options:
        safe_options = "<ul>\n" + "\n".join(
            f"<li>{html.escape(opt, quote=True)}</li>" for opt in options
        ) + "\n</ul>"
    else:
        safe_options = ""

    # Format the final post using the template.
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options=safe_options
    )