import html
from typing import List

# A simple forum post template.  The placeholders are `{title}`, `{content}` and `{points}`.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-content">{content}</div>
  {points}
</div>
"""

def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a forum post from the supplied title, body text and highlights.

    Parameters
    ----------
    subject : str
        The post's title or main topic.
    text : str
        The body of the forum post.
    highlights : list[str]
        Discussion points or options.  Each element may contain Markdown
        syntax, but it will be treated as plain text and safely escaped.

    Returns
    -------
    str
        A fully formatted HTML string ready for rendering in a forum.
    """
    # Escape user input to avoid injection attacks (CWE‑74)
    safe_title = html.escape(subject, quote=True)
    safe_content = html.escape(text, quote=False)

    # Build an unordered list of the highlights.
    if highlights:
        escaped_items = [f"<li>{html.escape(item, quote=False)}</li>" for item in highlights]
        points_html = f"<ul>{''.join(escaped_items)}</ul>"
    else:
        points_html = ""

    # Insert all parts into the template.
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        content=safe_content,
        points=points_html
    )