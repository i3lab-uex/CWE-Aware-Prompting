import html
from typing import List

# Default template if a global FORUM_POST_FORMAT is not defined elsewhere.
FORUM_POST_FORMAT: str = (
    "<h2>{header}</h2>\n"
    "<div class=\"forum-body\">{message}</div>\n"
    "<ul>{options}</ul>"
)

def create_forum_post(title: str, body: str, topics: List[str]) -> str:
    """
    Construct a sanitized forum post with the given title, body and topics.

    Parameters
    ----------
    title : str
        The forum post title.
    body : str
        The main content of the post.
    topics : list[str]
        A list of discussion points in markdown format.

    Returns
    -------
    str
        The fully rendered and sanitized forum post as an HTML string.
    """
    # Sanitize the title and body to prevent XSS or markup injection.
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)

    # Convert each topic into a safe <li> element.
    list_items = []
    for t in topics:
        # Strip leading/trailing whitespace and escape HTML.
        cleaned = html.escape(t.strip(), quote=False)
        # Ensure the topic is not empty after stripping.
        if cleaned:
            list_items.append(f"<li>{cleaned}</li>")

    safe_options = "\n".join(list_items)

    # Build the final post using the template.
    forum_post = FORUM_POST_FORMAT.format(
        header=safe_title,
        message=safe_body,
        options=safe_options
    )
    return forum_post