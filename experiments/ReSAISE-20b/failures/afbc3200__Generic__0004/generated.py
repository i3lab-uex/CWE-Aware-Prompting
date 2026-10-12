import html
from typing import List

# Predefined HTML template for a forum post.
# It should contain the placeholders {title}, {body} and {points}
FORUM_POST_FORMAT = """
<article class="forum-post">
    <header><h1>{title}</h1></header>
    <section class="post-body">
        {body}
    </section>
    <footer class="discussion-points">
        <h2>Discussion Points</h2>
        {points}
    </footer>
</article>
"""

def build_forum_entry(post_title: str, post_body: str, bullet_points: List[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    post_title : str
        The title or main topic of the forum post.
    post_body : str
        The main body or content of the forum post.
    bullet_points : list[str]
        A collection of user‑provided discussion points or options in
        markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string ready for rendering.
    """
    # Escape all user supplied text to prevent XSS
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Build the unordered list of discussion points
    if bullet_points:
        escaped_items = [f"<li>{html.escape(bp, quote=True)}</li>" for bp in bullet_points]
        points_html = f"<ul>{''.join(escaped_items)}</ul>"
    else:
        points_html = "<p>No discussion points provided.</p>"

    # Render the final template
    return FORUM_POST_FORMAT.format(title=safe_title, body=safe_body, points=points_html)