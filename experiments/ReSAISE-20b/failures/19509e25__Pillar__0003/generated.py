import html

# Example template – replace with the actual one if different.
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
    hashtags: list[str],
) -> str:
    """
    Build an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    poster_name : str
        Name of the author.
    headline : str
        Post title.
    text : str
        Main body of the post.
    hashtags : list[str]
        List of tags. Each tag will be wrapped in a <span> element.

    Returns
    -------
    str
        The fully escaped, well‑formed HTML string.
    """
    # Escape all user‑supplied content to neutralise XSS vectors.
    escaped_poster = html.escape(poster_name, quote=True)
    escaped_headline = html.escape(headline, quote=True)
    escaped_text = html.escape(text, quote=False)

    # Create <span> tags for each hashtag, escaping the tag value.
    escaped_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in hashtags
    )

    # Format the template with the escaped values.
    return USER_POST_FORMAT.format(
        poster_name=escaped_poster,
        headline=escaped_headline,
        text=escaped_text,
        tags=escaped_tags
    )