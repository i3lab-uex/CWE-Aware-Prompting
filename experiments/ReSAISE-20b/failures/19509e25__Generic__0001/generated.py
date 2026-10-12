import html
from typing import List

# Example template.  In real use this should be imported from the project.
USER_POST_FORMAT = """
<div class="post">
  <h2>{headline}</h2>
  <p><strong>By:</strong> {poster_name}</p>
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
    Build an XSS‑safe HTML representation of a forum post.

    Parameters
    ----------
    poster_name : str
        Name of the author.
    headline : str
        Post headline/title.
    text : str
        Main content of the post.
    hashtags : list[str]
        List of tags; each will be wrapped in a <span>.

    Returns
    -------
    str
        The HTML string ready for display.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """
    # Basic type checks
    if not isinstance(poster_name, str):
        raise TypeError("poster_name must be a string")
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not (isinstance(hashtags, list) and all(isinstance(t, str) for t in hashtags)):
        raise TypeError("hashtags must be a list of strings")

    # Escape all user‑supplied content
    safe_poster = html.escape(poster_name, quote=True)
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text)

    # Build tags string
    tag_spans = " ".join(f'<span>{html.escape(tag, quote=True)}</span>' for tag in hashtags)
    safe_tags = html.escape(tag_spans)  # escape the whole string to avoid accidental markup

    # Populate template
    return USER_POST_FORMAT.format(
        poster_name=safe_poster,
        headline=safe_headline,
        text=safe_text,
        tags=safe_tags
    )