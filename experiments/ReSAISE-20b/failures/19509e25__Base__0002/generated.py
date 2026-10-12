import html

# Example template; replace with the actual one used in your application.
USER_POST_FORMAT = """
<div class="post">
  <h2>{headline}</h2>
  <p><strong>By:</strong> {poster_name}</p>
  <div class="content">{text}</div>
  <div class="tags">{tags}</div>
</div>
"""

def compose_post_html(poster_name: str, headline: str, text: str,
                      hashtags: list[str]) -> str:
    """
    Build an XSS‑safe HTML representation of a forum post.

    Parameters
    ----------
    poster_name : str
        The name of the user who posted.
    headline : str
        The title of the post.
    text : str
        The main body content of the post.
    hashtags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        An HTML string containing the escaped post data and tags.
    """
    # Escape all user‑supplied content to neutralise HTML/JS injection
    escaped_poster = html.escape(poster_name, quote=True)
    escaped_headline = html.escape(headline, quote=True)
    escaped_text = html.escape(text, quote=True)

    # Build tags: each tag is wrapped in <span> and escaped
    escaped_tags = []
    for tag in hashtags:
        # Ensure the tag is a string and strip surrounding whitespace
        if not isinstance(tag, str):
            raise TypeError(f"Tag must be a string, got {type(tag).__name__}")
        clean_tag = tag.strip()
        escaped_tag = html.escape(clean_tag, quote=True)
        escaped_tags.append(f'<span>{escaped_tag}</span>')

    tags_html = ' '.join(escaped_tags)

    # Format the final HTML using the provided template
    return USER_POST_FORMAT.format(
        poster_name=escaped_poster,
        headline=escaped_headline,
        text=escaped_text,
        tags=tags_html
    )