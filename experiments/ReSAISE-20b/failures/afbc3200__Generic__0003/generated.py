import html
from typing import List

# Example template – in real usage this would be defined elsewhere.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    {bullet_points}
</div>
"""

def build_forum_entry(
    post_title: str,
    post_body: str,
    bullet_points: List[str]
) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    post_title : str
        The title or main topic of the forum post.
    post_body : str
        The main body/content of the forum post.
    bullet_points : list[str]
        A collection of discussion points or options in markdown format.

    Returns
    -------
    str
        Fully formatted and sanitized HTML representation of the forum post.
    """
    if not isinstance(post_title, str):
        raise TypeError("post_title must be a string")
    if not isinstance(post_body, str):
        raise TypeError("post_body must be a string")
    if not isinstance(bullet_points, list):
        raise TypeError("bullet_points must be a list of strings")
    if not all(isinstance(p, str) for p in bullet_points):
        raise TypeError("all items in bullet_points must be strings")

    # Escape title and body to prevent XSS
    escaped_title = html.escape(post_title)
    escaped_body = html.escape(post_body)

    # Render bullet points as <ul><li>...</li></ul>
    if bullet_points:
        rendered_items = "".join(
            f"<li>{html.escape(bp)}</li>" for bp in bullet_points
        )
        rendered_list = f"<ul>{rendered_items}</ul>"
    else:
        rendered_list = ""

    return FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        bullet_points=rendered_list
    )