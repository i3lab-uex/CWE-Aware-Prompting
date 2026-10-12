import html
from typing import List

# Example template; in real usage this should be imported from the project constants
FORUM_POST_FORMAT = """
<article class="forum-post">
  <header>
    <h2>{title}</h2>
  </header>
  <section class="post-body">
    {body}
  </section>
  <footer class="discussion-points">
    <h3>Discussion Points</h3>
    {points}
  </footer>
</article>
"""

def create_forum_post(topic: str, text_body: str, points: List[str]) -> str:
    """
    Create a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic : str
        The title or main topic of the forum post.
    text_body : str
        The main body or content of the forum post.
    points : list[str]
        A collection of user‑provided discussion points or options in Markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML representation of the forum post.

    Raises
    ------
    ValueError
        If any argument is not of the expected type.
    """
    # Validate input types
    if not isinstance(topic, str):
        raise ValueError("topic must be a string")
    if not isinstance(text_body, str):
        raise ValueError("text_body must be a string")
    if not isinstance(points, list) or not all(isinstance(p, str) for p in points):
        raise ValueError("points must be a list of strings")

    # Escape content to avoid XSS and ensure well‑formedness
    escaped_title = html.escape(topic, quote=True)
    escaped_body = html.escape(text_body, quote=True).replace("\n", "<br>")

    # Render points as an unordered list
    if points:
        escaped_points = "".join(
            f"<li>{html.escape(p, quote=True)}</li>" for p in points
        )
        ul_html = f"<ul>{escaped_points}</ul>"
    else:
        ul_html = "<p>No discussion points provided.</p>"

    # Substitute into the template
    return FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        points=ul_html
    )