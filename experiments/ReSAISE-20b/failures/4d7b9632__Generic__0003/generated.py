import html
from typing import List

# Example template – in real usage this should be imported or defined elsewhere.
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
    Generate a secure HTML representation of a forum post.

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
        XSS‑protected HTML string for the forum post.
    """
    # Escape all user-supplied content to prevent XSS.
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content, quote=False)

    # Wrap each tag in a <span> and escape its content.
    safe_tags = ' '.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    )

    # Format the final HTML using the provided template.
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )