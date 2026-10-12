import html

# Predefined HTML template for a forum post. Placeholders are marked with {placeholder}.
USER_POST_FORMAT = """
<div class="post">
    <h2 class="title">{title}</h2>
    <p class="author">Posted by: {author}</p>
    <div class="body">{body}</div>
    <div class="tags">
        {tags}
    </div>
</div>
"""

def generate_post_html(author: str, title: str, body: str, post_tags: list[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    author : str
        The author of the post.
    title : str
        The title of the user's post.
    body : str
        The main content of the user's post.
    post_tags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        A string containing the sanitized HTML representation of the user's post.

    Raises
    ------
    ValueError
        If any required argument is missing or not of the expected type.
    """
    # Basic validation
    if not all(isinstance(arg, str) for arg in (author, title, body)):
        raise ValueError("Author, title, and body must be strings.")
    if not isinstance(post_tags, list) or not all(isinstance(t, str) for t in post_tags):
        raise ValueError("post_tags must be a list of strings.")

    # Escape user-provided content to prevent XSS / injection
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)  # body may contain <p> etc., but we still escape

    # Render tags as separate <span> elements
    safe_tags = " ".join(f'<span class="tag">{html.escape(tag, quote=True)}</span>' for tag in post_tags)

    # Populate the template
    return USER_POST_FORMAT.format(
        title=safe_title,
        author=safe_author,
        body=safe_body,
        tags=safe_tags
    )