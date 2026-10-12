import html
from typing import List

# Predefined HTML template with placeholders for author, title, body and tags.
USER_POST_FORMAT = """
<article class="post">
    <header>
        <h1>{title}</h1>
        <p class="author">Posted by: {author}</p>
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
        Author name.
    title : str
        Post title.
    body : str
        Main content of the post.
    post_tags : List[str]
        List of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string.
    """
    # Escape all user-supplied text to prevent XSS or broken markup
    safe_author = html.escape(author, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False).replace("\n", "<br>")

    # Build tags HTML: each tag inside a <span class="tag"> element
    safe_tags = []
    for tag in post_tags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = " ".join(safe_tags)

    # Render the final HTML
    return USER_POST_FORMAT.format(
        author=safe_author,
        title=safe_title,
        body=safe_body,
        tags_html=tags_html
    )