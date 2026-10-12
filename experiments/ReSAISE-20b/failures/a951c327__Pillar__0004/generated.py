import html

# Predefined template with placeholders for author, title, body and tags.
USER_POST_FORMAT = """
<article class="post">
    <header>
        <h2>{title}</h2>
        <p class="author">Posted by: {author}</p>
    </header>
    <section class="content">
        {body}
    </section>
    <footer class="tags">
        {tags}
    </footer>
</article>
"""

def generate_post_html(author: str, title: str, body: str, post_tags: list[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Args:
        author: The name of the post's author.
        title: The post's title.
        body: The main content of the post.
        post_tags: A list of tags associated with the post.

    Returns:
        str: The fully rendered and sanitized HTML string.
    """
    # Escape all user supplied content to prevent XSS
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    # Preserve newlines in body by converting to <br>
    safe_body = html.escape(body, quote=True).replace('\n', '<br>')

    # Render tags as individual <span> elements, escaped
    safe_tags = ''.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span> '
        for tag in post_tags
    ).strip()

    # Fill the template
    rendered = USER_POST_FORMAT.format(
        author=safe_author,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )
    return rendered.strip()