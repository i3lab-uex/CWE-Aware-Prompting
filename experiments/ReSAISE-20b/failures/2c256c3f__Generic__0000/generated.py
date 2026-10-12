import html
from typing import List

# Example template (the actual one should be defined elsewhere in the project)
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p class="author">Posted by: {writer_name}</p>
  <div class="content">{body}</div>
  <div class="tags">{tags}</div>
</div>
"""

def generate_post_html(writer_name: str,
                       title: str,
                       body: str,
                       tag_list: List[str]) -> str:
    """
    Generate an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        The name of the author.
    title : str
        Post headline.
    body : str
        Main text content.
    tag_list : List[str]
        Tags associated with the post.

    Returns
    -------
    str
        Sanitised HTML string ready for rendering.
    """
    # Escape all user‑supplied data
    esc_writer = html.escape(writer_name, quote=True)
    esc_title  = html.escape(title, quote=True)
    esc_body   = html.escape(body, quote=False).replace("\n", "<br>")

    # Build tags HTML
    tag_html_parts = []
    for t in tag_list:
        esc_tag = html.escape(t, quote=True)
        tag_html_parts.append(f'<span>{esc_tag}</span>')
    tags_html = " ".join(tag_html_parts)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        writer_name=esc_writer,
        title=esc_title,
        body=esc_body,
        tags=tags_html
    )