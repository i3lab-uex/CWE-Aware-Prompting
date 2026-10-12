import html

# Predefined HTML template with placeholders for author, title, body and tags.
USER_POST_FORMAT = """
<article class="post">
    <header>
        <h2>{title}</h2>
        <p class="author">Posted by {author}</p>
    </header>
    <div class="content">{body}</div>
    <footer class="tags">
        {tags}
    </footer>
</article>
"""

def generate_post_html(author: str, title: str, body: str, post_tags: list[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Args:
        author: The author's name.
        title: Title of the post.
        body: Main content of the post.
        post_tags: List of tags associated with the post.

    Returns:
        A string containing safe HTML for the post.
    """
    # Escape all user-provided content to prevent XSS
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)

    # Build tag spans safely
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    ]
    tags_html = " ".join(escaped_tags)

    # Format the final HTML with sanitized parts
    return USER_POST_FORMAT.format(
        title=safe_title,
        author=safe_author,
        body=safe_body,
        tags=tags_html
    )