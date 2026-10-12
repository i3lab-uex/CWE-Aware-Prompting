import html
from typing import List

# Pre‑defined HTML template for forum posts.
# It contains three placeholders: {title}, {body} and {points}.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    <ul class="discussion-points">
        {points}
    </ul>
</div>
"""

def create_forum_entry(title: str, body: str, points: List[str]) -> str:
    """
    Assemble a structured forum post.

    Parameters
    ----------
    title : str
        The title or main topic of the forum post.
    body : str
        The primary content or body text of the post.
    points : list[str]
        A series of user‑supplied discussion points or options in markdown format.

    Returns
    -------
    str
        The fully formatted and sanitized forum post, including the header,
        message body, and safely rendered discussion points.

    Notes
    -----
    * All user‑supplied content is HTML escaped to prevent injection.
    * Markdown syntax within points is preserved as plain text; it will not be
      interpreted as HTML.
    * The function avoids CWE‑707 by ensuring that the generated output is
      well‑formed HTML and does not contain any unescaped user input.
    """
    # Sanitize title and body
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Build the list of discussion points
    safe_points_items = []
    for point in points:
        # Escape each point; preserve markdown characters but prevent HTML injection
        escaped_point = html.escape(point, quote=True)
        safe_points_items.append(f"<li>{escaped_point}</li>")

    # Join the list items into a single string
    safe_points_html = "\n        ".join(safe_points_items)

    # Format the final HTML using the template
    forum_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points_html
    )

    return forum_post.strip()