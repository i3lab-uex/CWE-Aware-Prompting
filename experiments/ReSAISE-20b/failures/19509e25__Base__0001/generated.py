import html

# Example HTML template with placeholders for poster_name, headline, text and tags.
USER_POST_FORMAT = """
<div class="post">
  <h2>{headline}</h2>
  <p class="author">Posted by: {poster_name}</p>
  <div class="content">{text}</div>
  <div class="tags">{tags}</div>
</div>
"""

def compose_post_html(poster_name: str, headline: str, text: str, hashtags: list[str]) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    poster_name : str
        Name of the author.
    headline : str
        Post headline.
    text : str
        Main content of the post.
    hashtags : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        A string containing a safe HTML representation of the post.
    """
    # Escape all user‑supplied content to prevent XSS
    safe_poster_name = html.escape(poster_name, quote=True)
    safe_headline   = html.escape(headline, quote=True)
    safe_text       = html.escape(text, quote=False)  # Preserve newlines as text

    # Build the tags string with each tag wrapped in a <span>
    safe_tags = ''.join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in hashtags
    )

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        poster_name=safe_poster_name,
        headline=safe_headline,
        text=safe_text,
        tags=safe_tags
    )