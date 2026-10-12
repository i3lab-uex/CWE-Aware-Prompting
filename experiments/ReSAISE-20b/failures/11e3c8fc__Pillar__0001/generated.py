import html
from typing import List

# Example template – in real usage this would be defined elsewhere.
USER_POST_FORMAT = """
<article class="post" data-author="{author_id}">
  <h2>{post_heading}</h2>
  <div class="content">{content}</div>
  <footer class="tags">{labels}</footer>
</article>
"""

def render_blog_post(
    author_id: str,
    post_heading: str,
    content: str,
    labels: List[str]
) -> str:
    """
    Render a secure HTML representation of a forum post.

    Parameters
    ----------
    author_id : str
        Identifier of the post's creator.
    post_heading : str
        Heading/title of the user's post.
    content : str
        Main content/body of the post.
    labels : List[str]
        Tags/labels associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string for the forum post.
    """
    # Escape all user-supplied data to avoid injection
    safe_author_id = html.escape(author_id, quote=True)
    safe_heading = html.escape(post_heading, quote=False)  # quotes not needed in headings
    safe_content = html.escape(content, quote=True)

    # Wrap each label in a <span> and escape it
    escaped_labels = [
        f'<span class="tag">{html.escape(label, quote=True)}</span>'
        for label in labels
    ]
    # Join the tags with a space to avoid concatenation issues
    safe_labels = " ".join(escaped_labels)

    # Use the template with explicit keyword arguments to avoid accidental injection
    rendered = USER_POST_FORMAT.format(
        author_id=safe_author_id,
        post_heading=safe_heading,
        content=safe_content,
        labels=safe_labels
    )

    return rendered