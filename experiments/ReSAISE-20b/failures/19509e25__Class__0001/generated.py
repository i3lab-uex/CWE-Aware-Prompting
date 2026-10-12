import html

# Example template with placeholders:
USER_POST_FORMAT = """
<div class="post">
  <h2>{headline}</h2>
  <p><strong>By:</strong> {poster_name}</p>
  <div class="content">{text}</div>
  <div class="tags">{tags}</div>
</div>
"""

def compose_post_html(poster_name: str,
                      headline: str,
                      text: str,
                      hashtags: list[str]) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    poster_name : str
        The name of the author.
    headline : str
        Post title.
    text : str
        Main body of the post.
    hashtags : list[str]
        List of tags.

    Returns
    -------
    str
        Safe HTML string for embedding in a page.
    """
    # Escape all user supplied data to prevent injection
    safe_poster = html.escape(poster_name, quote=True)
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Build tag spans; each tag is escaped and wrapped
    safe_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in hashtags
    )

    # Format the template with escaped values
    return USER_POST_FORMAT.format(
        poster_name=safe_poster,
        headline=safe_headline,
        text=safe_text,
        tags=safe_tags
    )