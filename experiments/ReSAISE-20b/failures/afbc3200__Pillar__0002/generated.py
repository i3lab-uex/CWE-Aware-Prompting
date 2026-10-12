import html
from typing import List

# Example template – in real usage this would be defined elsewhere.
FORUM_POST_FORMAT = """
<article class="forum-post">
  <header>
    <h1>{title}</h1>
  </header>
  <section class="post-body">
    {body}
  </section>
  <aside class="discussion-points">
    <h2>Discussion Points</h2>
    {points}
  </aside>
</article>
"""

def build_forum_entry(post_title: str, post_body: str, bullet_points: List[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    post_title : str
        The title or main topic of the forum post.
    post_body : str
        The main body or content of the forum post.
    bullet_points : list[str]
        A collection of user‑provided discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string.
    """
    # Escape title and body to avoid XSS or malformed markup
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Convert bullet points to a safe <ul> list
    safe_points = []
    for point in bullet_points:
        # Escape each markdown string; we do not render Markdown to keep it simple
        escaped = html.escape(point, quote=True)
        safe_points.append(f"<li>{escaped}</li>")
    points_html = "<ul>\n" + "\n".join(safe_points) + "\n</ul>"

    # Format the final HTML using a safe template
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )

    return formatted_post

# Example usage:
if __name__ == "__main__":
    title = "Welcome to the Forum"
    body = "Feel free to discuss any topic here. <script>alert('xss');</script>"
    points = [
        "First point with special chars: < & >",
        "Second point – Markdown _italic_ and **bold**"
    ]
    print(build_forum_entry(title, body, points))