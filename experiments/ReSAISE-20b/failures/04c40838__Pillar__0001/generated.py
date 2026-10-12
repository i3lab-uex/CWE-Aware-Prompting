import html
from typing import List

# Template for rendering the forum post.  The placeholders are replaced with
# sanitized values using str.format.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<p>{message}</p>
{options_section}
"""

def _sanitize(text: str) -> str:
    """
    Escape any HTML special characters to prevent injection attacks.
    This mitigates CWE-707 by ensuring that user supplied content
    is well‑formed and cannot break the surrounding markup.
    """
    return html.escape(text, quote=True)

def _render_options(options: List[str]) -> str:
    """
    Convert a list of markdown options into an unordered HTML list.
    Each option is first sanitized to avoid injection.  The resulting
    string contains only safe markup.
    """
    if not options:
        return ""

    list_items = []
    for opt in options:
        # Convert markdown to plain text by stripping common markup
        sanitized = _sanitize(opt)
        list_items.append(f"    <li>{sanitized}</li>")

    return "<ul>\n" + "\n".join(list_items) + "\n</ul>"

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Render a forum post from user supplied header, message and options.

    Parameters
    ----------
    header : str
        The title of the post.
    message : str
        The body text of the post.
    options : List[str]
        A list of user submitted options (in markdown format).

    Returns
    -------
    str
        A sanitized HTML string containing the header, message and options.
    """
    # Sanitize all user inputs
    safe_header = _sanitize(header)
    safe_message = _sanitize(message)

    # Render options section
    options_html = _render_options(options)
    if options_html:
        options_section = f"<h3>Discussion Options</h3>\n{options_html}"
    else:
        options_section = ""

    # Compose final output
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options_section=options_section
    )