import html
from typing import List

# Example template; in real usage this would be defined elsewhere.
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
    Construct a secure HTML representation of a forum post.

    All user supplied content is escaped to prevent XSS or injection attacks.
    Each tag is wrapped in a <span> element.

    Parameters
    ----------
    poster_name : str
        The name of the post's author.
    headline : str
        The headline of the user's post.
    text : str
        The primary text content of the user's post.
    hashtags : List[str]
        A collection of tags related to the post.

    Returns
    -------
    str
        XSS‑protected HTML string of the formatted post.
    """
    # Escape all user supplied fields
    safe_poster_name = html.escape(poster_name, quote=True)
    safe_headline   = html.escape(headline,   quote=True)
    safe_text       = html.escape(text,       quote=True)

    # Build the tags string
    escaped_tags = [f'<span>{html.escape(tag, quote=True)}</span>' for tag in hashtags]
    tags_html = " ".join(escaped_tags)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        poster_name=safe_poster_name,
        headline=safe_headline,
        text=safe_text,
        tags=tags_html
    )