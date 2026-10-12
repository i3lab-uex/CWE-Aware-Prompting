import html
from typing import List

# Example template. In a real application this would be defined elsewhere.
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
    Construct a safe HTML representation of a forum post.

    Parameters
    ----------
    poster_name : str
        The name of the author.
    headline : str
        The title/headline of the post.
    text : str
        The main body of the post.
    hashtags : list[str]
        A list of tags to be displayed.

    Returns
    -------
    str
        An XSS‑protected HTML string containing the post.
    """
    # Basic type checks – raise if inputs are not as expected
    if not isinstance(poster_name, str):
        raise TypeError("poster_name must be a string")
    if not isinstance(headline, str):
        raise TypeError("headline must be a string")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not (isinstance(hashtags, list) and all(isinstance(tag, str) for tag in hashtags)):
        raise TypeError("hashtags must be a list of strings")

    # Escape user‑provided content to prevent XSS
    safe_poster_name = html.escape(poster_name, quote=True)
    safe_headline   = html.escape(headline, quote=True)
    safe_text       = html.escape(text, quote=False)  # Allow &lt; &gt; for formatting

    # Build the tags string – each tag wrapped in a <span>
    safe_tags = ''.join(f'<span>{html.escape(tag, quote=True)}</span>' for tag in hashtags)

    # Format the final HTML
    html_output = USER_POST_FORMAT.format(
        poster_name=safe_poster_name,
        headline=safe_headline,
        text=safe_text,
        tags=safe_tags
    )
    return html_output.strip()