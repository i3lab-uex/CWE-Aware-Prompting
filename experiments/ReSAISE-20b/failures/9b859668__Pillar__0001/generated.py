import html
from typing import List

# Predefined template for forum posts.
# The placeholders {header}, {body} and {options} will be replaced by the
# sanitized values passed to construct_forum_content.
FORUM_POST_FORMAT: str = (
    "## {header}\n\n{body}\n\n{options}"
)

def construct_forum_content(
    heading: str,
    content: str,
    choices: List[str],
) -> str:
    """
    Construct a formatted forum post from user-provided content.

    The function sanitizes all input to prevent HTML/JS injection and renders
    the list of choices as an unordered list (<ul>).  The resulting string is
    suitable for display on a web page or in a forum.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body text of the forum post.
    choices : List[str]
        A collection of user‑provided options or discussion points in
        markdown format.

    Returns
    -------
    str
        A sanitized and formatted forum post string containing the header,
        message body, and options rendered as an HTML unordered list.

    Raises
    ------
    TypeError
        If any of the arguments are not of the expected type.
    """
    # Basic type checking
    if not isinstance(heading, str):
        raise TypeError("heading must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(choices, list) or not all(isinstance(c, str) for c in choices):
        raise TypeError("choices must be a list of strings")

    # Sanitize all user input to neutralize potential HTML/JS injection.
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Render choices as an HTML unordered list.
    if choices:
        list_items = "\n".join(
            f"  <li>{html.escape(choice, quote=True)}</li>" for choice in choices
        )
        safe_options = f"<ul>\n{list_items}\n</ul>"
    else:
        safe_options = "<p>No options provided.</p>"

    # Combine everything using the predefined template.
    forum_post = FORUM_POST_FORMAT.format(
        header=safe_heading,
        body=safe_content,
        options=safe_options,
    )

    return forum_post