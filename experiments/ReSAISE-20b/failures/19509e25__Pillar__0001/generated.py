import html
import re

# Example template – in real use this would be defined elsewhere
USER_POST_FORMAT = (
    '<div class="post">'
    '  <h2>{headline}</h2>'
    '  <p class="author">Posted by {poster_name}</p>'
    '  <div class="content">{text}</div>'
    '  <div class="tags">{tags}</div>'
    '</div>'
)

# Regular expression that matches safe tag characters: letters, digits, hyphens, and underscores.
_TAG_SANITIZE_RE = re.compile(r'^[A-Za-z0-9_-]+$')

def _sanitize_tag(tag: str) -> str | None:
    """
    Return a sanitized tag string if it matches the allowed pattern, otherwise None.
    """
    cleaned = tag.strip()
    if _TAG_SANITIZE_RE.match(cleaned):
        return html.escape(cleaned, quote=True)
    return None

def compose_post_html(
    poster_name: str,
    headline: str,
    text: str,
    hashtags: list[str]
) -> str:
    """
    Construct a safe HTML representation of a forum post.

    Parameters
    ----------
    poster_name : str
        Name of the author.
    headline : str
        Post title.
    text : str
        Main body of the post.
    hashtags : list[str]
        Tags to associate with the post.

    Returns
    -------
    str
        XSS‑protected HTML string formatted according to USER_POST_FORMAT.

    Raises
    ------
    ValueError
        If any required argument is not a string or if the template is malformed.
    """
    # Basic type checks to guard against unexpected input
    if not all(isinstance(arg, str) for arg in (poster_name, headline, text)):
        raise ValueError("poster_name, headline, and text must be strings")
    if not isinstance(hashtags, list):
        raise ValueError("hashtags must be a list of strings")

    # Escape user supplied content
    safe_poster = html.escape(poster_name, quote=True)
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=False)  # Preserve line breaks if needed

    # Sanitize tags and build span elements
    tag_spans = []
    for t in hashtags:
        if not isinstance(t, str):
            continue  # skip non‑string tags
        sanitized = _sanitize_tag(t)
        if sanitized:
            tag_spans.append(f'<span class="tag">{sanitized}</span>')
    tags_html = ' '.join(tag_spans)

    # Format the final HTML
    try:
        post_html = USER_POST_FORMAT.format(
            poster_name=safe_poster,
            headline=safe_headline,
            text=safe_text,
            tags=tags_html
        )
    except KeyError as exc:
        raise ValueError(f"Template missing placeholder: {exc}") from exc

    return post_html