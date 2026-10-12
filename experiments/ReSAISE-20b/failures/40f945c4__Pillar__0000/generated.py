import html
from typing import List

# Example template with placeholders.
USER_POST_FORMAT = """
<article class="post">
    <header>
        <h1>{post_heading}</h1>
        <p class="author">Posted by: {user_name}</p>
    </header>
    <section class="content">
        {post_content}
    </section>
    <footer class="tags">
        {post_tags}
    </footer>
</article>
"""

def build_post_html(user_name: str,
                    post_heading: str,
                    post_content: str,
                    post_tags: List[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Parameters
    ----------
    user_name : str
        Author of the post.
    post_heading : str
        Title of the post.
    post_content : str
        Main body content of the post. May contain user supplied text.
    post_tags : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        A safe, well‑formed HTML string ready for rendering.

    Raises
    ------
    ValueError
        If any required argument is missing or empty.
    """
    # Basic validation: ensure all arguments are provided
    if not user_name or not post_heading or not post_content:
        raise ValueError("user_name, post_heading, and post_content must be non‑empty")

    # Escape all user supplied content to avoid XSS
    safe_user_name = html.escape(user_name, quote=True)
    safe_heading = html.escape(post_heading, quote=True)

    # Allow only a subset of HTML in post_content. For simplicity,
    # we escape everything and then unescape a few safe tags.
    # Here we permit <b>, <i>, <u>, <strong>, <em> and <p>.
    allowed_tags = {"b", "i", "u", "strong", "em", "p", "br"}
    # Escape the content first
    escaped_content = html.escape(post_content, quote=True)
    # Re‑introduce allowed tags
    import re

    def _unescape_allowed(match: re.Match) -> str:
        tag = match.group(1)
        return f"<{tag}>" if tag in allowed_tags else ""

    # Pattern to find escaped tags like &lt;b&gt;
    pattern = re.compile(r"&lt;(/?)([a-zA-Z0-9]+)&gt;")
    safe_content = pattern.sub(lambda m: f"<{m.group(1)}{m.group(2)}>" if m.group(2) in allowed_tags else "", escaped_content)

    # Build tag spans
    safe_tag_spans = []
    for tag in post_tags:
        if not isinstance(tag, str):
            continue  # skip non-string tags
        escaped_tag = html.escape(tag, quote=True)
        safe_tag_spans.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = " ".join(safe_tag_spans)

    # Render the final HTML
    return USER_POST_FORMAT.format(
        user_name=safe_user_name,
        post_heading=safe_heading,
        post_content=safe_content,
        post_tags=tags_html
    )