import html
from typing import List

# Example template. In real usage this would be defined elsewhere.
USER_POST_FORMAT = """
<article class="post">
  <h1>{title}</h1>
  <p class="author">Posted by: {writer_name}</p>
  <div class="content">{body}</div>
  <div class="tags">{tags}</div>
</article>
"""

def generate_post_html(
    writer_name: str,
    title: str,
    body: str,
    tag_list: List[str]
) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        Name of the author.
    title : str
        Post headline.
    body : str
        Main content of the post.
    tag_list : list[str]
        List of tags to associate with the post.

    Returns
    -------
    str
        Safe HTML string ready for rendering.
    """
    # Escape all user‑supplied content to prevent XSS
    safe_writer = html.escape(writer_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)

    # Build the tag spans; each tag is escaped individually
    safe_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    )

    # Use the template to assemble the final HTML
    return USER_POST_FORMAT.format(
        writer_name=safe_writer,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )