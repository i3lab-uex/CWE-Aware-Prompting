import html

# Example template (replace with the actual one used in your project)
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p class="author">Posted by: {author_name}</p>
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

    Parameters
    ----------
    author_name : str
        The name of the post's author.
    post_title : str
        The headline of the user's post.
    content : str
        The primary text content of the user's post.
    post_tags : list[str]
        A collection of tags related to the post.

    Returns
    -------
    str
        The HTML string with all user‑controlled input properly escaped.
    """
    # Escape all user supplied strings
    esc_author = html.escape(author_name, quote=True)
    esc_title = html.escape(post_title, quote=True)
    esc_content = html.escape(content, quote=False)  # Preserve line breaks etc.

    # Render each tag inside a <span> and escape it
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in post_tags
    ]
    tags_html = ' '.join(escaped_tags)

    # Format the template with escaped values
    html_output = USER_POST_FORMAT.format(
        author_name=esc_author,
        title=esc_title,
        content=esc_content,
        tags=tags_html
    )
    return html_output