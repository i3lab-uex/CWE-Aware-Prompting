import html
from typing import List

# Example template. In real usage this should be defined elsewhere.
USER_POST_FORMAT = """
<div class="post">
  <h2>{headline}</h2>
  <p class="author">Posted by: {poster_name}</p>
  <div class="content">{text}</div>
  <div class="tags">{tags}</div>
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
        Post headline.
    text : str
        Main body of the post.
    hashtags : list[str]
        Tags to attach to the post.

    Returns
    -------
    str
        The fully escaped HTML string.
    """
    # Escape all user supplied content to avoid injection attacks
    safe_poster = html.escape(poster_name, quote=True)
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Build tags string with each tag wrapped in a <span> element
    safe_tags = []
    for tag in hashtags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = ' '.join(safe_tags)

    # Safely format the template
    try:
        post_html = USER_POST_FORMAT.format(
            poster_name=safe_poster,
            headline=safe_headline,
            text=safe_text,
            tags=tags_html
        )
    except KeyError as e:
        raise ValueError(f"Missing placeholder in USER_POST_FORMAT: {e}") from None

    return post_html