import html
from typing import List

# Example template; in real usage this would be provided by the system.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  {points}
</div>
"""

def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a forum post from user supplied components.

    Parameters
    ----------
    subject : str
        The title or main topic of the forum post.
    text : str
        The primary content or body text of the post.
    highlights : List[str]
        A list of discussion points or options in markdown format.

    Returns
    -------
    str
        The fully formatted and sanitized forum post as an HTML string.
    """
    # Sanitize title and body to prevent injection
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(text, quote=True)

    # Build the unordered list of discussion points
    if highlights:
        li_items = []
        for point in highlights:
            # Escape each point; strip leading/trailing whitespace
            escaped = html.escape(point.strip(), quote=True)
            li_items.append(f"<li>{escaped}</li>")
        points_html = "<ul>\n" + "\n".join(li_items) + "\n</ul>"
    else:
        points_html = ""

    # Render the final template
    post_html = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )

    return post_html.strip()