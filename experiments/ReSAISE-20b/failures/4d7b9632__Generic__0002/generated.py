import html
from typing import List

# Example template; in real usage this would be imported or defined elsewhere.
USER_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <p class="author">Posted by: {author_name}</p>
    <div class="content">{body}</div>
    <div class="tags">{tags}</div>
</div>
"""

def render_forum_post(
    author_name: str,
    title: str,
    body_content: str,
    tag_list: List[str]
) -> str:
    """
    Render a forum post into XSS‑safe HTML.

    Parameters
    ----------
    author_name : str
        Identifier of the post's creator.
    title : str
        The heading of the user's post.
    body_content : str
        Primary content of the user's post.
    tag_list : List[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML representation of the forum post.
    """
    # Escape all user‑supplied data
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content, quote=False)

    # Build the tags section: each tag wrapped in <span>
    safe_tags = []
    for t in tag_list:
        escaped_tag = html.escape(t, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = " ".join(safe_tags)

    # Populate the template
    rendered = USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )

    return rendered.strip()