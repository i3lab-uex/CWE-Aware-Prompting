import html
from typing import List

# Example template – in real usage this would be defined elsewhere.
USER_POST_FORMAT = """
<article class="forum-post">
    <header>
        <h2>{title}</h2>
        <p class="author">Posted by: {author_name}</p>
    </header>
    <section class="content">
        {body}
    </section>
    <footer class="tags">
        {tags}
    </footer>
</article>
"""

def render_forum_post(
    author_name: str,
    title: str,
    body_content: str,
    tag_list: List[str]
) -> str:
    """
    Generate a safe HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Identifier of the post's creator.
    title : str
        Heading of the user's post.
    body_content : str
        Primary content of the user's post.
    tag_list : List[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML version of the forum post.
    """
    # Escape all user-provided content
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content, quote=False)

    # Wrap each tag in a <span> and escape the tag text
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    ]
    safe_tags = ' '.join(escaped_tags)

    # Render the final HTML using the template
    rendered_html = USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )

    return rendered_html.strip()