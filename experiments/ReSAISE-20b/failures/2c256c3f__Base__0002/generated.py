import html
from typing import List

# Example template – in real usage this should be defined elsewhere and imported.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p class="author">By: {writer_name}</p>
  <div class="body">{body}</div>
  <div class="tags">{tags}</div>
</div>
"""

def generate_post_html(writer_name: str,
                       title: str,
                       body: str,
                       tag_list: List[str]) -> str:
    """
    Construct an XSS‑safe HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        Name of the author.
    title : str
        Post headline.
    body : str
        Main content of the post.
    tag_list : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        Escaped HTML string suitable for rendering in a web page.
    """
    # Escape all user‑supplied content to prevent XSS
    safe_writer = html.escape(writer_name, quote=True)
    safe_title  = html.escape(title, quote=True)
    safe_body   = html.escape(body, quote=True)

    # Build tag spans – each tag is escaped individually
    safe_tags = " ".join(f'<span>{html.escape(tag, quote=True)}</span>'
                         for tag in tag_list)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        writer_name=safe_writer,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )