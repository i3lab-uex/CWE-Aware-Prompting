import html

# Existing template string with placeholders for the post components.
USER_POST_FORMAT = """
<div class="post">
  <h2>{headline}</h2>
  <p class="author">Posted by: {poster_name}</p>
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
        Name of the author.
    headline : str
        Title of the post.
    text : str
        Main content of the post.
    hashtags : list[str]
        List of tags to be displayed.

    Returns
    -------
    str
        Safe HTML string ready for inclusion in a web page.
    """
    # Escape all user‑supplied content to avoid injection
    safe_poster = html.escape(poster_name, quote=True)
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=False)

    # Wrap each tag in a <span> element and escape the tag content
    escaped_tags = [
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in hashtags
    ]
    tags_html = ' '.join(escaped_tags)

    # Format the final HTML using the template
    return USER_POST_FORMAT.format(
        poster_name=safe_poster,
        headline=safe_headline,
        text=safe_text,
        tags=tags_html
    )