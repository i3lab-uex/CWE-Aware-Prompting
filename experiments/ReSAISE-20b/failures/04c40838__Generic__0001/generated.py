import html
from typing import List

# Define a simple template for forum posts.  
FORUM_POST_FORMAT = """<div class="forum-post">
  <h2>{header}</h2>
  <p>{message}</p>
  {options_section}
</div>"""


def _sanitize_markdown_option(option: str) -> str:
    """
    Very light sanitization for a markdown option. The goal is to escape any
    HTML special characters that might break the surrounding markup while
    preserving Markdown syntax. For a production system you would use a full
    Markdown renderer that supports sanitization.
    """
    # Escape HTML entities first
    escaped = html.escape(option, quote=True)
    return escaped


def generate_forum_post(header: str, message: str, options: List[str]) -> str:
    """
    Build a sanitized forum post from the given header, message and list of
    options. The resulting string contains an unordered list (<ul>) for the
    options.

    Parameters
    ----------
    header : str
        The title of the forum post.
    message : str
        The main body text of the post.
    options : list[str]
        A list of user-submitted options (Markdown format).

    Returns
    -------
    str
        A sanitized HTML string containing the formatted forum post.

    Raises
    ------
    ValueError
        If any of the arguments are not of the expected type.
    """
    if not isinstance(header, str):
        raise ValueError("header must be a string")
    if not isinstance(message, str):
        raise ValueError("message must be a string")
    if not isinstance(options, list) or not all(isinstance(o, str) for o in options):
        raise ValueError("options must be a list of strings")

    # Escape header and message to prevent XSS
    safe_header = html.escape(header, quote=True)
    safe_message = html.escape(message, quote=True)

    # Build the options section
    if options:
        list_items = []
        for opt in options:
            sanitized_opt = _sanitize_markdown_option(opt)
            list_items.append(f"<li>{sanitized_opt}</li>")
        options_html = "<ul>\n" + "\n".join(list_items) + "\n</ul>"
    else:
        options_html = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        header=safe_header,
        message=safe_message,
        options_section=options_html
    )