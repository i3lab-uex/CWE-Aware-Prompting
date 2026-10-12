import html
from typing import List

# Template used to format the forum post. Placeholders:
#   {header}  - sanitized header
#   {message} - sanitized message body
#   {options} - HTML unordered list of options (or empty string if none)
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{header}</h2>
    <div class="post-body">{message}</div>
    {options}
</div>
"""

def _escape_and_wrap_options(options: List[str]) -> str:
    """
    Convert a list of markdown options into an HTML unordered list.
    Each option is escaped to avoid XSS attacks. Markdown links are left
    as plain text; if you need proper rendering, consider a markdown parser.
    """
    if not options:
        return ""

    list_items = []
    for opt in options:
        escaped_opt = html.escape(opt)
        list_items.append(f"<li>{escaped_opt}</li>")
    return f"\n<ul>\n{''.join(list_items)}\n</ul>"

def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Generate a sanitized HTML snippet for a forum post.

    Parameters
    ----------
    header : str
        The title of the forum post.
    message : str
        The main body text of the post.
    options : list[str]
        A list of discussion options in markdown format.

    Returns
    -------
    str
        A sanitized HTML string containing the header, message, and options.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """
    if not isinstance(header, str):
        raise TypeError("header must be a string")
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    if not isinstance(options, list) or not all(isinstance(o, str) for o in options):
        raise TypeError("options must be a list of strings")

    sanitized_header = html.escape(header)
    sanitized_message = html.escape(message).replace("\n", "<br>")

    options_html = _escape_and_wrap_options(options)

    return FORUM_POST_FORMAT.format(
        header=sanitized_header,
        message=sanitized_message,
        options=options_html
    )