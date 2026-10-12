import html
from typing import List

# Default template if one is not provided elsewhere.
FORUM_POST_FORMAT = (
    "<h1>{header}</h1>\n"
    "<div class=\"content\">{message}</div>\n"
    "{options}"
)

def construct_forum_content(heading: str, content: str, choices: List[str]) -> str:
    """
    Construct a sanitized and formatted forum post.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body text of the forum post.
    choices : list[str]
        A collection of user‑provided options or discussion points in Markdown
        format.

    Returns
    -------
    str
        The complete forum post with a header, body and an HTML unordered list of
        choices. All user supplied data is escaped to prevent XSS or other
        injection attacks.

    Raises
    ------
    ValueError
        If any of the arguments are not of the expected type.
    """
    if not isinstance(heading, str):
        raise ValueError("heading must be a string")
    if not isinstance(content, str):
        raise ValueError("content must be a string")
    if not (isinstance(choices, list) and all(isinstance(c, str) for c in choices)):
        raise ValueError("choices must be a list of strings")

    # Escape all user supplied text to prevent HTML injection
    safe_heading = html.escape(heading)
    safe_content = html.escape(content)

    # Convert markdown choices to plain text and wrap each in <li>
    list_items = []
    for choice in choices:
        # Escape the markdown text; we do not render Markdown here
        escaped_choice = html.escape(choice)
        list_items.append(f"  <li>{escaped_choice}</li>")

    # Build the unordered list if there are any choices
    options_html = ""
    if list_items:
        options_html = "<ul>\n" + "\n".join(list_items) + "\n</ul>"

    # Format the final post using the template
    formatted_post = FORUM_POST_FORMAT.format(
        header=safe_heading,
        message=safe_content,
        options=options_html
    )

    return formatted_post