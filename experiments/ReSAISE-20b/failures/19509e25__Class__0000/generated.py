import html
from typing import List

# Example template; in practice this would be imported from elsewhere.
USER_POST_FORMAT = """
<div class="post">
  <h2>{headline}</h2>
  <p><strong>Author:</strong> {poster_name}</p>
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
        The headline of the user's post.
    text : str
        The primary text content of the user's post.
    hashtags : list[str]
        A collection of tags related to the post.

    Returns
    -------
    str
        The HTML string with all user input safely escaped.
    """
    # Escape all user-supplied content to neutralize any HTML/JS injection attempts.
    safe_poster_name = html.escape(poster_name, quote=True)
    safe_headline   = html.escape(headline, quote=True)
    safe_text       = html.escape(text, quote=True)

    # Build the tags string: each tag is wrapped in a <span> element.
    safe_tags = []
    for tag in hashtags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = " ".join(safe_tags)

    # Format the final HTML using the provided template.
    return USER_POST_FORMAT.format(
        poster_name=safe_poster_name,
        headline=safe_headline,
        text=safe_text,
        tags=tags_html
    )