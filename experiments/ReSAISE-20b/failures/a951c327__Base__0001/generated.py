import html
from typing import List

# Example template – adjust the placeholder names as needed.
USER_POST_FORMAT = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">by {author}</p>
    <div class="body">{body}</div>
    <div class="tags">{tags}</div>
</div>
"""

def generate_post_html(author: str, title: str, body: str, post_tags: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a user's forum post.

    Parameters
    ----------
    author : str
        The name of the user who wrote the post.
    title : str
        The title of the post.
    body : str
        The main content of the post.
    post_tags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        A string containing the sanitized HTML of the post.
    """
    # Escape all user-controllable input to mitigate XSS (CWE-79)
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Build the tags HTML
    tag_spans = []
    for tag in post_tags:
        safe_tag = html.escape(tag, quote=True)
        tag_spans.append(f"<span class=\"tag\">{safe_tag}</span>")
    tags_html = " ".join(tag_spans)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        title=safe_title,
        author=safe_author,
        body=safe_body,
        tags=tags_html
    )