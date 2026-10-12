import html
from typing import List

# Example template – in real use this would be defined elsewhere.
USER_POST_FORMAT = """
<article class="forum-post">
  <header>
    <h1>{title}</h1>
    <p class="author">Posted by {author_name}</p>
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
    Render a forum post as safe HTML.

    Parameters
    ----------
    author_name : str
        Identifier of the post's creator.
    title : str
        The heading of the user's post.
    body_content : str
        The primary content of the user's post.
    tag_list : list[str]
        A sequence of tags associated with the post.

    Returns
    -------
    str
        An XSS‑protected HTML representation of the forum post.
    """
    # Escape all user supplied content
    esc_author = html.escape(author_name, quote=True)
    esc_title = html.escape(title, quote=True)
    esc_body = html.escape(body_content, quote=False)

    # Build tag spans
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    ]
    tags_html = " ".join(escaped_tags)

    # Render the template
    return USER_POST_FORMAT.format(
        author_name=esc_author,
        title=esc_title,
        body=esc_body,
        tags=tags_html
    )