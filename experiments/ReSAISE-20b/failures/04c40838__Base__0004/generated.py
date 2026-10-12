import html
from typing import List

# Template for rendering a forum post. Placeholders: {header}, {message}, {options}
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{header}</h2>
  <div class="post-message">{message}</div>
  {options_section}
</div>
"""

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Generate a sanitized forum post with header, message and options.

    Parameters
    ----------
    header : str
        The user‑written title of the post.
    message : str
        The body text of the post.
    options : List[str]
        A list of user‑submitted options (markdown format) for discussion.

    Returns
    -------
    str
        A sanitized HTML string ready to be embedded in a web page.
    """
    # Escape all user‑provided content to prevent XSS
    safe_header = html.escape(header, quote=True)
    safe_message = html.escape(message, quote=True)

    # Render options as an unordered list. Each option is escaped individually.
    if options:
        list_items = "\n".join(
            f"  <li>{html.escape(opt, quote=True)}</li>" for opt in options
        )
        options_section = f"\n<ul>\n{list_items}\n</ul>"
    else:
        options_section = ""

    # Combine everything using the template
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options_section=options_section
    )