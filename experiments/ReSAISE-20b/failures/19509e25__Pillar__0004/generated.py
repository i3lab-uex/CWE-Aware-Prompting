import html
from typing import List

# Example template; in real code this would be defined elsewhere.
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
        Post title.
    text : str
        Main content of the post.
    hashtags : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        Safe HTML string ready to be rendered.
    """
    # Escape all user supplied fields to avoid injection
    safe_poster = html.escape(poster_name, quote=True)
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=False)  # Preserve line breaks

    # Wrap each tag in a <span> and escape the tag text
    safe_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in hashtags
    ]
    tags_html = ' '.join(safe_tags)

    # Format the final HTML using the template
    try:
        return USER_POST_FORMAT.format(
            poster_name=safe_poster,
            headline=safe_headline,
            text=safe_text,
            tags=tags_html
        )
    except KeyError as exc:
        # Log or re‑raise with context if template is malformed
        raise ValueError(f"Missing placeholder in USER_POST_FORMAT: {exc}") from exc