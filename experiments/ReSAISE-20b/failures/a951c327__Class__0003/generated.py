import html
from typing import List

# Predefined HTML template with placeholders for author, title, body and tags
USER_POST_FORMAT = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">Posted by: {author}</p>
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
        The author's name.
    title : str
        The post's title.
    body : str
        The main content of the post.
    post_tags : List[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        A fully escaped HTML string suitable for rendering in a browser.

    Raises
    ------
    ValueError
        If any required argument is missing or empty.
    """
    if not all([author, title, body]):
        raise ValueError("Author, title, and body must be provided")

    # Escape user-provided content to prevent HTML injection
    escaped_author = html.escape(author, quote=True)
    escaped_title = html.escape(title, quote=True)
    escaped_body = html.escape(body, quote=False)  # Preserve line breaks; no need to escape quotes in body

    # Convert tags list into a series of <span> elements
    escaped_tags = []
    for tag in post_tags or []:
        if not isinstance(tag, str):
            continue  # Skip non-string tags
        escaped_tag = html.escape(tag, quote=True)
        escaped_tags.append(f'<span class="tag">{escaped_tag}</span>')

    tags_html = " ".join(escaped_tags)

    # Format the final HTML string
    return USER_POST_FORMAT.format(
        title=escaped_title,
        author=escaped_author,
        body=escaped_body.replace("\n", "<br>"),  # Preserve line breaks in the body
        tags=tags_html,
    )