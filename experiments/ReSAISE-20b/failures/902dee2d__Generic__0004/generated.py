import html
from typing import List

# Pre‑defined template for a forum post.
# The placeholders {title}, {content} and {points} will be replaced
# by the sanitized values provided to `build_forum_post`.
FORUM_POST_FORMAT: str = """
<article class="forum-post">
    <h1>{title}</h1>
    <div class="post-content">{content}</div>
    <section class="discussion-points">
        <h2>Discussion Points</h2>
        {points}
    </section>
</article>
"""

def _sanitize(text: str) -> str:
    """
    Escapes HTML special characters to prevent XSS attacks.
    """
    return html.escape(text, quote=True)

def _render_list(items: List[str]) -> str:
    """
    Convert a list of markdown items into an HTML unordered list.
    Each item is sanitized to prevent injection.
    """
    if not items:
        return "<p>No discussion points provided.</p>"
    list_items = "".join(f"<li>{_sanitize(item)}</li>" for item in items)
    return f"<ul>\n{list_items}\n</ul>"

def build_forum_post(headline: str, content: str, items: List[str]) -> str:
    """
    Assemble a forum post from the provided headline, content and discussion points.

    Parameters
    ----------
    headline : str
        The title or main topic of the forum post.
    content : str
        The primary content or body text of the post.
    items : list[str]
        A series of user‑supplied discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized forum post ready for rendering in a browser.
    """
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(items, list) or not all(isinstance(i, str) for i in items):
        raise TypeError("items must be a list of strings")

    safe_title = _sanitize(headline)
    safe_content = _sanitize(content).replace("\n", "<br>")  # preserve line breaks
    safe_points = _render_list(items)

    return FORUM_POST_FORMAT.format(
        title=safe_title,
        content=safe_content,
        points=safe_points
    )