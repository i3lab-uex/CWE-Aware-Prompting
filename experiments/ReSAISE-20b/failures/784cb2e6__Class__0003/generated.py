import html
from typing import List

# Predefined template for the forum post.
# It should contain three placeholders: {header}, {body} and {options}.
FORUM_POST_FORMAT = (
    "<h2>{header}</h2>\n"
    "<div>{body}</div>\n"
    "<ul>{options}</ul>"
)

def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a sanitized and formatted forum post.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    body : str
        The main content or body of the forum post.
    topics : list[str]
        A collection of user‑provided options or discussion points in markdown format.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post, including a header,
        message body, and an unordered list of options.

    Notes
    -----
    All user‑supplied content is escaped to prevent HTML injection (CWE-74).
    """
    # Escape all user input to neutralize any special HTML characters.
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Convert each topic to a list item and escape it.
    escaped_topics = [
        f"<li>{html.escape(topic, quote=True)}</li>" for topic in topics
    ]
    options_html = "\n".join(escaped_topics)

    # Format the final post using the predefined template.
    formatted_post = FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=options_html
    )
    return formatted_post