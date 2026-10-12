import html

# Predefined HTML template with placeholders.
USER_POST_FORMAT = """
<div class="post">
    <h2>{title}</h2>
    <p><strong>Author:</strong> {author}</p>
    <div class="content">{body}</div>
    <div class="tags">{tags}</div>
</div>
"""

def render_user_content(
    username_key: str,
    title_key: str,
    body_key: str,
    tag_elements: list[str]
) -> str:
    """
    Render a secure HTML representation of a user's forum post.

    Parameters
    ----------
    username_key : str
        Identifier of the post's creator.
    title_key : str
        Heading of the user's post.
    body_key : str
        Primary content of the user's post.
    tag_elements : list[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string of the forum post.
    """
    # Escape user-provided strings to prevent XSS
    escaped_author = html.escape(username_key, quote=True)
    escaped_title = html.escape(title_key, quote=True)
    escaped_body = html.escape(body_key, quote=True)

    # Wrap each tag in a <span> element and escape the tag text
    escaped_tags = []
    for tag in tag_elements:
        safe_tag = html.escape(tag, quote=True)
        escaped_tags.append(f'<span class="tag">{safe_tag}</span>')

    tags_html = " ".join(escaped_tags)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        title=escaped_title,
        author=escaped_author,
        body=escaped_body,
        tags=tags_html
    )