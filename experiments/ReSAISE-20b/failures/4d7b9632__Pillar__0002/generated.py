import html

# Example template – replace with the actual constant in your code base.
USER_POST_FORMAT = (
    '<article class="forum-post">'
    '  <header>'
    '    <h2>{title}</h2>'
    '    <p class="author">Posted by: {author_name}</p>'
    '  </header>'
    '  <section class="content">{body}</section>'
    '  <footer>{tags}</footer>'
    '</article>'
)

def render_forum_post(author_name: str, title: str,
                      body_content: str, tag_list: list[str]) -> str:
    """
    Render a secure HTML representation of a forum post.

    All user-supplied content is escaped to prevent XSS. Tags are wrapped in
    <span> elements and each tag value is escaped as well.

    Parameters:
        author_name (str): Identifier of the post's creator.
        title (str): Heading of the user's post.
        body_content (str): Primary content of the user's post.
        tag_list (list[str]): Sequence of tags associated with the post.

    Returns:
        str: XSS-protected HTML string for the forum post.
    """
    # Escape all user inputs
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content, quote=False)  # Preserve newlines

    # Build tags string
    safe_tags = ''.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    )

    # Format the template with escaped values
    rendered = USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )
    return rendered