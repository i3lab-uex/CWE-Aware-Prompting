import html
from typing import List

# Example template – replace with the actual format in your project.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p class="author">Posted by {author}</p>
  <div class="body">{body}</div>
  <div class="tags">
    {tags}
  </div>
</div>
"""

def generate_post_html(author: str, title: str, body: str,
                       post_tags: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    author : str
        The name of the post author.
    title : str
        The title of the post.
    body : str
        The main content of the post.
    post_tags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        The sanitized HTML string ready to be embedded in a page.

    Notes
    -----
    All user‑supplied input is escaped using `html.escape` to prevent
    Cross‑Site Scripting (CWE‑79). No additional sanitization is performed
    beyond escaping, so content that is intended to be HTML (e.g. rich text)
    should be handled separately by the caller.
    """
    # Escape all user‑controllable input
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)

    # Convert tags into escaped <span> elements
    safe_tags = []
    for tag in post_tags:
        # Ensure the tag itself is escaped; no quotes needed inside <span>
        safe_tag = html.escape(tag, quote=False)
        safe_tags.append(f'<span class="tag">{safe_tag}</span>')

    tags_html = " ".join(safe_tags)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        title=safe_title,
        author=safe_author,
        body=safe_body,
        tags=tags_html
    )