import html
from typing import List

# Template for the forum post.  Placeholders are replaced with safe content.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{header}</h2>
  <div class="message">{message}</div>
  {options_html}
</div>
"""

def _escape(text: str) -> str:
    """
    Escape special HTML characters to prevent injection.
    """
    return html.escape(text, quote=True)

def _render_options(options: List[str]) -> str:
    """
    Convert a list of markdown options into an unordered HTML list.
    Each option is escaped to avoid XSS or markup injection.
    """
    if not options:
        return ""

    list_items = []
    for opt in options:
        # Escape the markdown text.  Markdown is not rendered here,
        # so we treat it as plain text.
        escaped_opt = _escape(opt)
        list_items.append(f"<li>{escaped_opt}</li>")

    return "<ul>\n" + "\n".join(list_items) + "\n</ul>"

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Generate a sanitized forum post from user supplied data.

    Parameters
    ----------
    header : str
        The title/header of the forum post.
    message : str
        The body text of the forum post.
    options : list[str]
        A list of discussion options written in markdown.

    Returns
    -------
    str
        An HTML fragment containing the header, message and options,
        all properly escaped to mitigate injection attacks.

    Raises
    ------
    ValueError
        If any of the arguments are not strings or a list of strings.
    """
    # Basic type checking
    if not isinstance(header, str):
        raise ValueError("header must be a string")
    if not isinstance(message, str):
        raise ValueError("message must be a string")
    if not isinstance(options, list) or not all(isinstance(o, str) for o in options):
        raise ValueError("options must be a list of strings")

    # Escape the main components
    safe_header = _escape(header)
    safe_message = _escape(message)

    # Render options as an unordered list
    options_html = _render_options(options)

    # Format the final HTML using the template
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options_html=options_html
    )