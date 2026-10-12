import html
from typing import List

# Pre‑defined HTML template for forum posts.
# The placeholders `{title}`, `{body}` and `{list}` will be replaced
# with the escaped title, body text and discussion points list.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  {list}
</div>
"""

def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a sanitized forum post.

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
        A fully formatted and sanitized forum post, including the
        header, message body, and safely rendered discussion points.

    Notes
    -----
    All user input is HTML‑escaped to mitigate XSS (CWE‑79).
    Markdown syntax is not interpreted; it is treated as plain text.
    """
    # Escape all user‑controlled input
    escaped_title = html.escape(subject, quote=True)
    escaped_body = html.escape(text, quote=True)

    # Render the discussion points as an unordered list
    if highlights:
        escaped_items = [
            f"<li>{html.escape(item, quote=True)}</li>" for item in highlights
        ]
        list_html = "<ul>\n" + "\n".join(escaped_items) + "\n</ul>"
    else:
        list_html = ""

    # Substitute into the template
    post_html = FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        list=list_html
    )

    return post_html.strip()