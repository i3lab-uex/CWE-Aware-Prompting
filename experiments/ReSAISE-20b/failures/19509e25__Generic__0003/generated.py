import html
from typing import List

# Example template. In real use this should be imported from the existing codebase.
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
        The name of the post's author.
    headline : str
        The headline/title of the user's post.
    text : str
        The primary content/body of the post.
    hashtags : List[str]
        A collection of tags associated with the post.

    Returns
    -------
    str
        The complete HTML string for the post.
    """
    # Escape all user‑supplied content to avoid XSS attacks
    safe_poster_name = html.escape(poster_name, quote=True)
    safe_headline   = html.escape(headline,   quote=True)
    safe_text       = html.escape(text,      quote=True)

    # Build tags string: each tag wrapped in a <span> element
    safe_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in hashtags
    )

    # Format the final HTML using the template
    return USER_POST_FORMAT.format(
        poster_name=safe_poster_name,
        headline=safe_headline,
        text=safe_text,
        tags=safe_tags
    )