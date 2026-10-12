import html
from typing import List

# Example template; in real usage this would be defined elsewhere.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {discussion}
</div>
"""

def build_forum_entry(
    post_title: str,
    post_body: str,
    bullet_points: List[str]
) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    post_title : str
        The title or main topic of the forum post.
    post_body : str
        The main body or content of the forum post.
    bullet_points : list[str]
        A collection of user‑provided discussion points or options.

    Returns
    -------
    str
        The fully formatted and sanitized HTML representation of the forum post.
    """
    # Escape all user‑supplied content to prevent injection (CWE‑74)
    escaped_title = html.escape(post_title, quote=True)
    escaped_body = html.escape(post_body, quote=True)

    # Build the discussion section as a <ul> if points are provided
    if bullet_points:
        escaped_items = [
            f"<li>{html.escape(point, quote=True)}</li>" for point in bullet_points
        ]
        discussion_html = f"<ul>{''.join(escaped_items)}</ul>"
    else:
        discussion_html = ""

    # Format the final HTML using the predefined template
    return FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        discussion=discussion_html
    )