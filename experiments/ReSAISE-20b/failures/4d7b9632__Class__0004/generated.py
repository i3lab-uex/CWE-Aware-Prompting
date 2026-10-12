import html
from typing import List

# A minimal template for the forum post.  The placeholders are used with str.format.
USER_POST_FORMAT = (
    '<article class="forum-post">\n'
    '  <header>\n'
    '    <h1>{title}</h1>\n'
    '    <p class="author">Posted by: {author_name}</p>\n'
    '  </header>\n'
    '  <section class="content">{body}</section>\n'
    '  <footer class="tags">{tags}</footer>\n'
    '</article>'
)

def render_forum_post(
    author_name: str,
    title: str,
    body_content: str,
    tag_list: List[str]
) -> str:
    """
    Generate an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Identifier of the user who created the post.
    title : str
        The heading of the user's post.
    body_content : str
        The main content of the post.
    tag_list : List[str]
        Tags associated with the post.

    Returns
    -------
    str
        A fully escaped HTML string ready to be inserted into a page.

    Notes
    -----
    All user supplied data is escaped with html.escape to neutralise any
    embedded markup or scripting.  The tag list is rendered as a series of
    <span> elements with the class "tag" for styling.
    """
    # Escape all user provided strings
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content, quote=False)  # body may contain newlines

    # Render each tag inside a <span> element, escaping the tag text
    safe_tags = ''.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span> '
        for tag in tag_list
    ).strip()

    # Combine everything using the template
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )