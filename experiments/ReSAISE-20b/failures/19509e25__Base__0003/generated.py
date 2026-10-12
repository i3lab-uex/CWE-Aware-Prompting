import html

# Existing HTML template with placeholders for the post components.
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
        Post title.
    text : str
        Main content of the post.
    hashtags : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        A string containing safely escaped HTML for the forum post.
    """
    # Escape all user‑supplied content to avoid XSS.
    safe_poster = html.escape(poster_name, quote=True)
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=False)

    # Build tags string: each tag wrapped in a <span>.
    safe_tags = []
    for tag in hashtags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')
    tags_html = " ".join(safe_tags)

    # Format the final HTML using the provided template.
    return USER_POST_FORMAT.format(
        poster_name=safe_poster,
        headline=safe_headline,
        text=safe_text,
        tags=tags_html
    )