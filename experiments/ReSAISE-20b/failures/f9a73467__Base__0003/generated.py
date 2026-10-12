import html
from typing import List

# Pre‑defined HTML template with placeholders for title, body and discussion points
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h2>{title}</h2>
  <div class="post-body">{body}</div>
  {discussion}
</div>
"""

def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a sanitized forum post.

    Parameters
    ----------
    subject : str
        Title or main topic of the forum post.
    text : str
        Primary content/body of the post.
    highlights : list[str]
        Discussion points or options in markdown format.

    Returns
    -------
    str
        Fully formatted and HTML‑escaped forum post.
    """
    # Escape user input to prevent XSS
    escaped_subject = html.escape(subject, quote=True)
    escaped_text = html.escape(text, quote=True)

    # Build discussion points list
    if highlights:
        escaped_items = [f"<li>{html.escape(item, quote=True)}</li>" for item in highlights]
        discussion_html = "<ul>\n" + "\n".join(escaped_items) + "\n</ul>"
    else:
        discussion_html = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        title=escaped_subject,
        body=escaped_text.replace("\n", "<br>"),
        discussion=discussion_html
    )