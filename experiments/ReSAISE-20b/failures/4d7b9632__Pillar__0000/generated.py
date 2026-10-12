import html
from typing import List

# Predefined HTML template with placeholders.
# The placeholders are {author_name}, {title}, {body} and {tags}.
USER_POST_FORMAT: str = """
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
    Generate a secure HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Identifier of the post's creator.
    title : str
        Heading of the user's post.
    body_content : str
        Primary content of the user's post.
    tag_list : list[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string of the forum post.
    """
    # 1. Escape all user-supplied data to prevent XSS.
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content, quote=False)

    # 2. Sanitize and format tags.
    safe_tags = []
    for tag in tag_list:
        # Strip leading/trailing whitespace and escape.
        clean_tag = html.escape(tag.strip(), quote=True)
        # Skip empty tags to avoid rendering <span></span>.
        if clean_tag:
            safe_tags.append(f'<span class="tag">{clean_tag}</span>')
    tags_html = " ".join(safe_tags)

    # 3. Insert sanitized components into the template.
    post_html = USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )

    # 4. Basic structural validation (CWE‑707 consideration).
    # Ensure that the resulting HTML contains the required sections.
    if (
        "<article" not in post_html or
        "</article>" not in post_html or
        "<header" not in post_html or
        "</footer>" not in post_html
    ):
        raise ValueError("Generated HTML is structurally incomplete.")

    return post_html.strip()