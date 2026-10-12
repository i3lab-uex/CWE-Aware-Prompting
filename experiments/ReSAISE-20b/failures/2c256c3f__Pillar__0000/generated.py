import html
from typing import List

# Example template; in real usage this would be defined elsewhere.
USER_POST_FORMAT = """
<article class="post">
  <h2>{title}</h2>
  <p class="author">Posted by: {writer_name}</p>
  <div class="content">{body}</div>
  <footer class="tags">{tags}</footer>
</article>
"""

def generate_post_html(writer_name: str,
                       title: str,
                       body: str,
                       tag_list: List[str]) -> str:
    """
    Generate an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        The name of the post's author.
    title : str
        The headline of the user's post.
    body : str
        The primary text content of the user's post.
    tag_list : list[str]
        A collection of tags related to the post.

    Returns
    -------
    str
        A string containing the HTML representation of the post.
    """
    # Escape all user‑supplied content to prevent XSS
    safe_writer_name = html.escape(writer_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Wrap each tag in a <span> element, escaping the tag text
    safe_tags = ' '.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    )

    # Safely format the template with escaped values
    return USER_POST_FORMAT.format(
        writer_name=safe_writer_name,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )