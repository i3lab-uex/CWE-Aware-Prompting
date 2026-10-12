import html

# Example template (could be imported from elsewhere)
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p><strong>Author:</strong> {author_name}</p>
  <div class="content">{content}</div>
  <div class="tags">{tags}</div>
</div>
"""

def create_post_html(author_name: str, post_title: str,
                     content: str, post_tags: list[str]) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Name of the post's author.
    post_title : str
        Title (headline) of the post.
    content : str
        Main body text of the post.
    post_tags : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        A fully escaped HTML string suitable for rendering on a web page.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    ValueError
        If required arguments are empty strings or tags list contains non‑string items.
    """
    # Validate argument types
    if not isinstance(author_name, str):
        raise TypeError("author_name must be a string")
    if not isinstance(post_title, str):
        raise TypeError("post_title must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(post_tags, list):
        raise TypeError("post_tags must be a list of strings")

    # Validate non‑empty values
    if not author_name.strip():
        raise ValueError("author_name cannot be empty")
    if not post_title.strip():
        raise ValueError("post_title cannot be empty")

    # Ensure all tags are strings and escape them
    escaped_tags = []
    for tag in post_tags:
        if not isinstance(tag, str):
            raise ValueError("All tags must be strings")
        escaped_tag = html.escape(tag, quote=True)
        # Wrap each tag in a <span> element
        escaped_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = " ".join(escaped_tags)

    # Escape the main components
    escaped_author = html.escape(author_name, quote=True)
    escaped_title = html.escape(post_title, quote=True)
    escaped_content = html.escape(content, quote=False)  # Preserve newlines

    # Build the final HTML using the template
    post_html = USER_POST_FORMAT.format(
        title=escaped_title,
        author_name=escaped_author,
        content=escaped_content,
        tags=tags_html
    )

    return post_html.strip()