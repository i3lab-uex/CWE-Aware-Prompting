import html
from typing import List

# Template for a forum post.  The placeholders are:
#   {header}   – the title of the post
#   {message}  – the main body content
#   {options}  – a rendered list of options (as <ul>...</ul>)
FORUM_POST_FORMAT: str = (
    "=== {header} ===\n\n{message}\n\nOptions:\n{options}"
)


def _escape_markdown(text: str) -> str:
    """
    Escape HTML special characters in a markdown string.
    This prevents injection of arbitrary markup into the final post.
    """
    return html.escape(text)


def _render_options(options_list: List[str]) -> str:
    """
    Convert a list of markdown strings into an HTML unordered list.
    Each option is escaped to neutralise special characters.
    """
    if not options_list:
        return "<ul></ul>"

    items = []
    for opt in options_list:
        escaped_opt = _escape_markdown(opt)
        items.append(f"  <li>{escaped_opt}</li>")
    return "<ul>\n" + "\n".join(items) + "\n</ul>"


def build_forum_post(title: str, post_body: str, options_list: List[str]) -> str:
    """
    Construct a sanitized forum post.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    post_body : str
        The main content or body of the forum post.
    options_list : list[str]
        A collection of user‑provided options or discussion points in markdown format.

    Returns
    -------
    str
        A sanitized and formatted forum post containing the header, message,
        and options as an HTML unordered list.

    Raises
    ------
    ValueError
        If any of the arguments are not of the expected type.
    """
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    if not isinstance(post_body, str):
        raise ValueError("post_body must be a string")
    if not isinstance(options_list, list):
        raise ValueError("options_list must be a list of strings")
    if not all(isinstance(opt, str) for opt in options_list):
        raise ValueError("all items in options_list must be strings")

    safe_title = _escape_markdown(title)
    safe_body = _escape_markdown(post_body)
    rendered_options = _render_options(options_list)

    return FORUM_POST_FORMAT.format(
        header=safe_title,
        message=safe_body,
        options=rendered_options
    )