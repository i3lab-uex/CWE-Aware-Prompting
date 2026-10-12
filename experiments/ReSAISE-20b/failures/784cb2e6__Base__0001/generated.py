import html
from typing import List

# Predefined template for forum posts.
FORUM_POST_FORMAT = """<h1>{header}</h1>
<div>{message}</div>
<ul>{options}</ul>"""

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
        A collection of user‑provided options or discussion points in markdown
        format.  Each topic will be rendered as a list item.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post, including
        a header, message body, and an HTML unordered list of options.

    Notes
    -----
    All user input is escaped using :func:`html.escape` to prevent cross‑site
    scripting (CWE‑79).  The function does not perform full Markdown
    rendering; it only ensures that the content is safely embedded in HTML.
    """
    # Escape user input to neutralize any HTML or script tags.
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Convert each topic to a list item after escaping.
    safe_topics = [
        f"<li>{html.escape(topic, quote=True)}</li>" for topic in topics
    ]

    # Join list items into a single string.
    options_html = "\n".join(safe_topics)

    # Render the final post using the template.
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        message=safe_body,
        options=options_html
    )