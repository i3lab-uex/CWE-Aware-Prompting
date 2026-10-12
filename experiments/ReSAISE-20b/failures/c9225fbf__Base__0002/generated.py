import html

# Example template with placeholders for author, title, content and tags.
USER_POST_FORMAT = """
<article class="forum-post">
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

    Parameters
    ----------
    author_name : str
        Name of the user who created the post.
    post_title : str
        Title of the post.
    content : str
        Main body text of the post.
    post_tags : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        HTML string safely escaped and formatted for display.
    """
    # Escape all user supplied text to prevent XSS
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_content = html.escape(content)

    # Wrap each tag in a <span> and escape it
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    ]
    tags_html = ' '.join(escaped_tags)

    # Format the final HTML using a safe template
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        content=safe_content,
        tags=tags_html
    )