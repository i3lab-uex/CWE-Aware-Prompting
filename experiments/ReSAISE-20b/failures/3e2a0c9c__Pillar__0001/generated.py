import html
from typing import List

# Predefined HTML template for a forum post.
# It contains three placeholders: {title}, {body} and {discussion}.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {discussion}
</div>
"""

def build_post_html(topic_title: str, body_text: str, list_items: List[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main body or content of the forum post.
    list_items : List[str]
        A collection of user‑provided discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string containing the title, body,
        and an unordered list of discussion points.

    Notes
    -----
    * All user supplied text is escaped using :func:`html.escape` to prevent
      injection of malicious markup.
    * The function does not perform markdown rendering; it simply escapes the
      content.  If richer formatting is needed, a dedicated renderer should be
      used before calling this function.
    """
    # Escape all user supplied content to avoid XSS and other injection attacks.
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Build the discussion list if items are provided.
    if list_items:
        safe_list_items = [
            f"<li>{html.escape(item, quote=True)}</li>" for item in list_items
        ]
        discussion_html = f"<ul>{''.join(safe_list_items)}</ul>"
    else:
        discussion_html = ""

    # Format the final HTML using the predefined template.
    post_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        discussion=discussion_html
    )

    return post_html.strip()