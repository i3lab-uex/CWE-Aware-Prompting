import html
from typing import List

# Example template. In a real system this might be loaded from a config or file.
USER_POST_FORMAT: str = """
<div class="post">
    <h2>{headline}</h2>
    <p class="author">Posted by: {poster_name}</p>
    <div class="content">{text}</div>
    <div class="tags">
        {tags}
    </div>
</div>
"""

def compose_post_html(
    poster_name: str,
    headline: str,
    text: str,
    hashtags: List[str]
) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    poster_name : str
        Name of the author.
    headline : str
        Post title.
    text : str
        Main body of the post.
    hashtags : List[str]
        Tags associated with the post.

    Returns
    -------
    str
        The rendered HTML string.
    """
    # Escape all user‑supplied content to prevent injection
    safe_poster = html.escape(poster_name, quote=True)
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=False)

    # Build tags string: each tag wrapped in <span> and escaped
    safe_tags = []
    for tag in hashtags:
        # Ensure the tag is a string; ignore non‑string entries
        if not isinstance(tag, str):
            continue
        escaped_tag = html.escape(tag.strip(), quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')

    tags_html = " ".join(safe_tags)

    # Render the template
    rendered = USER_POST_FORMAT.format(
        poster_name=safe_poster,
        headline=safe_headline,
        text=safe_text,
        tags=tags_html
    )
    return rendered.strip()