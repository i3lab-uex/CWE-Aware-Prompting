import html

# Predefined HTML template with placeholders.
USER_POST_FORMAT = (
    '<article class="forum-post">\n'
    '  <header>\n'
    '    <h2>{title}</h2>\n'
    '    <p class="author">Posted by {author_name}</p>\n'
    '  </header>\n'
    '  <section class="content">{body}</section>\n'
    '  <footer class="tags">{tags}</footer>\n'
    '</article>'
)

def render_forum_post(author_name: str, title: str, body_content: str,
                      tag_list: list[str]) -> str:
    """
    Generate a secure HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Identifier of the post's creator.
    title : str
        Heading of the user's post.
    body_content : str
        Primary content of the user's post.
    tag_list : list[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        XSS-protected HTML string of the forum post.
    """
    # Escape all user-supplied content to prevent XSS.
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content)

    # Build tag spans safely.
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    ]
    tags_html = ' '.join(escaped_tags)

    # Render the final HTML using the template.
    rendered_html = USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )
    return rendered_html