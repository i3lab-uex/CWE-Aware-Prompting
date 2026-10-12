import html
from typing import List

# Predefined template for forum posts.
# Example: "<h1>{header}</h1>\n<p>{body}</p>\n{options}"
FORUM_POST_FORMAT = "<h1>{header}</h1>\n<p>{body}</p>\n{options}"


def construct_forum_content(heading: str, content: str, choices: List[str]) -> str:
    """
    Construct a sanitized and formatted forum post.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body of the forum post.
    choices : list[str]
        A collection of user-provided options or discussion points in markdown format.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post,
        including the header, message body, and an HTML unordered list of options.
    """
    # Escape all user-provided strings to neutralize special HTML characters.
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build the <ul> element with each choice as a safe <li>.
    list_items = []
    for item in choices:
        # Escape each choice to avoid injection.
        safe_item = html.escape(item, quote=True)
        list_items.append(f"  <li>{safe_item}</li>")
    safe_options = "<ul>\n" + "\n".join(list_items) + "\n</ul>" if list_items else ""

    # Format the final post using the predefined template.
    return FORUM_POST_FORMAT.format(
        header=safe_heading,
        body=safe_content,
        options=safe_options
    )