import html
from typing import List

# Template for a forum post.  The placeholders are `{heading}`, `{content}` and `{options}`
FORUM_POST_FORMAT = """<div class="forum-post">
  <h2>{heading}</h2>
  <div class="post-body">{content}</div>
  {options}
</div>"""

def construct_forum_content(heading: str, content: str, choices: List[str]) -> str:
    """
    Construct a sanitized and formatted forum post.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main content or body of the forum post.  Any HTML special characters are escaped.
    choices : list[str]
        A collection of user‑provided options or discussion points in markdown format.
        Each item is escaped and rendered as a list item inside an unordered list.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post, including the header,
        message, and safely rendered options.

    Raises
    ------
    ValueError
        If any of the arguments is not a string (or list for choices).
    """
    # Validate input types
    if not isinstance(heading, str):
        raise ValueError("heading must be a string")
    if not isinstance(content, str):
        raise ValueError("content must be a string")
    if not isinstance(choices, list) or not all(isinstance(c, str) for c in choices):
        raise ValueError("choices must be a list of strings")

    # Escape heading and content to prevent XSS
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build the options list
    if choices:
        escaped_items = [f"<li>{html.escape(choice, quote=True)}</li>" for choice in choices]
        options_html = f"<ul>{''.join(escaped_items)}</ul>"
    else:
        options_html = ""

    # Render the final post
    return FORUM_POST_FORMAT.format(
        heading=safe_heading,
        content=safe_content,
        options=options_html
    )