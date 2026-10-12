import html

# Example template; replace with the actual one in your codebase.
USER_POST_FORMAT = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">Posted by {author_name}</p>
    <div class="content">{content}</div>
    <div class="tags">{tags}</div>
</div>
"""

def create_post_html(author_name: str,
                     post_title: str,
                     content: str,
                     post_tags: list[str]) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Args:
        author_name: Name of the post's author.
        post_title: Headline of the user's post.
        content: Primary text content of the post.
        post_tags: Collection of tags related to the post.

    Returns:
        A string containing a well‑formed, escaped HTML snippet.
    """
    # Escape all user supplied data to prevent injection
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_content = html.escape(content, quote=False)  # Preserve newlines

    # Build tags string; each tag is wrapped in a <span> and escaped
    safe_tags = ''.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    )

    # Insert escaped values into the template
    html_post = USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        content=safe_content.replace('\n', '<br>'),  # Preserve line breaks
        tags=safe_tags
    )

    return html_post