import html

# Example template – replace with the actual one in your project.
USER_POST_FORMAT = """
<article class="post">
    <h2>{title}</h2>
    <p class="author">Posted by: {author_name}</p>
    <div class="content">{content}</div>
    <footer class="tags">{tags}</footer>
</article>
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
        content: Main text content of the post.
        post_tags: List of tags associated with the post.

    Returns:
        A string containing the fully escaped and formatted HTML.
    """
    # Escape user‑supplied values to prevent XSS
    escaped_author = html.escape(author_name, quote=True)
    escaped_title = html.escape(post_title, quote=True)
    escaped_content = html.escape(content, quote=False)  # Preserve newlines etc.

    # Build tags string – each tag wrapped in a <span>
    escaped_tags = []
    for tag in post_tags:
        # Ensure each tag is also escaped
        safe_tag = html.escape(tag, quote=True)
        escaped_tags.append(f'<span class="tag">{safe_tag}</span>')
    tags_html = " ".join(escaped_tags)

    # Populate the template
    html_output = USER_POST_FORMAT.format(
        author_name=escaped_author,
        title=escaped_title,
        content=escaped_content,
        tags=tags_html
    )

    return html_output.strip()