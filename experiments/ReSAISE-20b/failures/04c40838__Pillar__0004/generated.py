import html
from typing import List

# Template for rendering a forum post.  The placeholders will be filled with
# the sanitized header, message and options list.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<p>{message}</p>
{options}
"""

def _sanitize_html(text: str) -> str:
    """
    Escape all HTML special characters in *text* to prevent XSS attacks.
    This function also normalizes the input by stripping leading/trailing
    whitespace and collapsing internal newlines to a single space.
    """
    # Strip surrounding whitespace and collapse multiple spaces/newlines
    cleaned = " ".join(text.strip().split())
    return html.escape(cleaned, quote=True)

def _render_options(options: List[str]) -> str:
    """
    Render a list of options as an unordered HTML list. Each option is
    sanitized to escape any potentially malicious content.
    """
    if not options:
        return ""

    list_items = []
    for opt in options:
        sanitized_opt = _sanitize_html(opt)
        list_items.append(f"<li>{sanitized_opt}</li>")

    return "<ul>\n" + "\n".join(list_items) + "\n</ul>"

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Generate a sanitized HTML forum post.

    Parameters
    ----------
    header : str
        The user-written title of the post.
    message : str
        The body text of the post.
    options : list[str]
        A list of user-submitted options (in markdown format).

    Returns
    -------
    str
        A sanitized HTML string containing the header, message and options.
    """
    # Sanitize each component
    safe_header = _sanitize_html(header)
    safe_message = _sanitize_html(message)

    # Render options into an unordered list
    safe_options = _render_options(options)

    # Format the final post using the provided template
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options=safe_options
    )