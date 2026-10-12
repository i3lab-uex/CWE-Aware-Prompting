import html
from typing import List

# Pre‑defined HTML template for forum posts.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  <div class="discussion-points">
    <h3>Discussion Points</h3>
    {points}
  </div>
</div>
"""

def _render_markdown_list(markdown_items: List[str]) -> str:
    """
    Convert a list of markdown items into an HTML unordered list.
    Only the plain text of each item is preserved and escaped to avoid
    XSS. Markdown syntax such as `*`, `_` or `-` is ignored.
    """
    escaped_items = [f"<li>{html.escape(item.strip())}</li>" for item in markdown_items]
    return f"<ul>\n{''.join(escaped_items)}\n</ul>"

def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a forum post from title, body and discussion points.

    Parameters
    ----------
    subject : str
        The title or main topic of the forum post.
    text : str
        The primary content or body text of the post.
    highlights : list[str]
        A series of user‑supplied discussion points or options in
        markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML forum post.
    """
    # Sanitize inputs to avoid injection attacks.
    safe_title = html.escape(subject.strip())
    safe_body = html.escape(text.strip()).replace("\n", "<br>")

    # Render discussion points as a safe unordered list.
    if highlights:
        safe_points = _render_markdown_list(highlights)
    else:
        # Empty list: provide a placeholder.
        safe_points = "<p>No discussion points provided.</p>"

    # Populate the template.
    formatted_post = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=safe_points
    )

    return formatted_post.strip()