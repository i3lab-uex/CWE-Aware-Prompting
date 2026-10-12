import html
from typing import List

# Predefined template for the post.
USER_POST_FORMAT = """
<article class="user-post">
  <header>
    <h2>{title}</h2>
    <p class="author">Posted by {author}</p>
  </header>
  <section class="content">
    {body}
  </section>
  <footer class="tags">
    {tags_html}
  </footer>
</article>
"""

def generate_post_html(author: str, title: str, body: str, post_tags: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    author : str
        The name of the user who wrote the post.
    title : str
        Title of the post.
    body : str
        Main content of the post. May contain newlines and user-provided text.
    post_tags : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        A string containing a safe HTML snippet ready for inclusion in a page.

    Raises
    ------
    ValueError
        If any required argument is missing or empty.
    """
    if not all([author, title, body]):
        raise ValueError("Author, title, and body must be non-empty strings")

    # Escape all user-provided content to prevent XSS
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)

    # Preserve line breaks in the body by converting newlines to <br>
    safe_body = html.escape(body, quote=True).replace("\n", "<br>")

    # Build tags HTML; each tag is wrapped in a <span>
    safe_tags = []
    for tag in post_tags:
        if tag:  # ignore empty tags
            safe_tag = html.escape(tag, quote=True)
            safe_tags.append(f'<span class="tag">{safe_tag}</span>')
    tags_html = " ".join(safe_tags)

    # Format the final HTML
    html_output = USER_POST_FORMAT.format(
        title=safe_title,
        author=safe_author,
        body=safe_body,
        tags_html=tags_html
    )

    return html_output.strip()