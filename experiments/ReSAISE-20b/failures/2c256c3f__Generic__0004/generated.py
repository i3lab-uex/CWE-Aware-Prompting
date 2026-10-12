import html
from typing import List

# Example template; in real use this would be defined elsewhere.
USER_POST_FORMAT = """
<div class="post">
    <h1>{title}</h1>
    <p><strong>Author:</strong> {writer_name}</p>
    <div class="content">{body}</div>
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
        Name of the post's author.
    title : str
        Post headline.
    body : str
        Main text content of the post.
    tag_list : List[str]
        Collection of tags related to the post.

    Returns
    -------
    str
        HTML string with placeholders replaced by escaped content.
    """
    # Escape user‑supplied text to prevent XSS
    safe_writer = html.escape(writer_name, quote=True)
    safe_title = html.escape(title, quote=True)
    # Body may contain line breaks; escape but preserve them as <br>
    safe_body = html.escape(body, quote=True).replace("\n", "<br>")

    # Build tags; each tag is wrapped in a <span>
    safe_tags = "".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    )

    # Populate the template
    return USER_POST_FORMAT.format(
        writer_name=safe_writer,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )