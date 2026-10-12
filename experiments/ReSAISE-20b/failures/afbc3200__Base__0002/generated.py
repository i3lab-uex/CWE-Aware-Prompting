import html

# Example template for a forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    <ul>{bullet_points}</ul>
</div>
"""

def build_forum_entry(post_title: str,
                      post_body: str,
                      bullet_points: list[str]) -> str:
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
        A fully formatted and sanitized HTML string ready for rendering on a web page.

    Notes
    -----
    * All user input is escaped using ``html.escape`` to prevent XSS attacks (CWE‑79).
    * The function does not perform full Markdown rendering; it only escapes the text
      and places each point in a ``<li>`` element.  If richer Markdown support is
      required, consider using a safe markdown renderer such as ``markdown`` with
      the ``safe_mode`` or ``bleach`` for sanitization.
    """
    # Escape title and body to neutralise any HTML/JS content
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Convert each bullet point to a safe <li> element
    safe_points = []
    for point in bullet_points:
        # Escape the entire point; no Markdown rendering is performed
        escaped_point = html.escape(point, quote=True)
        safe_points.append(f"<li>{escaped_point}</li>")

    # Join the list items into a single string
    bullet_html = "\n".join(safe_points)

    # Format the final HTML using the template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        bullet_points=bullet_html
    )