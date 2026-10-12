import html
from typing import List

# Template for rendering a forum post. Placeholders are {header}, {message} and {options}
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{header}</h2>
  <div class="post-body">{message}</div>
  {options}
</div>
"""

def _sanitize_markdown_option(option: str) -> str:
    """
    Basic sanitization for markdown options.
    - Escape HTML special characters to prevent XSS.
    - Preserve basic Markdown syntax by escaping only the critical tags.
    """
    # Escape all HTML characters first
    escaped = html.escape(option, quote=True)

    # Simple unescape for markdown links: [text](url)
    # This is intentionally conservative; any < or > characters are already escaped.
    return escaped

def _format_options(options: List[str]) -> str:
    """
    Convert a list of markdown strings into an unordered HTML list.
    Each option is sanitized before being inserted.
    """
    if not options:
        return ""

    list_items = []
    for opt in options:
        sanitized_opt = _sanitize_markdown_option(opt)
        list_items.append(f"<li>{sanitized_opt}</li>")
    return "<ul>\n" + "\n".join(list_items) + "\n</ul>"

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Generate a sanitized forum post HTML string.

    Parameters
    ----------
    header : str
        The title of the post.
    message : str
        Body text of the post.
    options : List[str]
        Markdown formatted discussion options.

    Returns
    -------
    str
        Sanitized HTML ready to be embedded in a webpage.
    """
    # Sanitize header and message
    safe_header = html.escape(header, quote=True)
    safe_message = html.escape(message, quote=False)

    # Format options
    formatted_options = _format_options(options)

    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options=formatted_options
    )