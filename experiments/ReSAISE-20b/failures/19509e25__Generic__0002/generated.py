import html
from typing import List

# Pre‑defined template with placeholders.
# Example format: "<div class='post'><h1>{headline}</h1><p>by {poster_name}</p><div>{text}</div><div class='tags'>{tags}</div></div>"
USER_POST_FORMAT: str = (
    "<div class='post'>"
    "<h1>{headline}</h1>"
    "<p>by {poster_name}</p>"
    "<div class='content'>{text}</div>"
    "<div class='tags'>{tags}</div>"
    "</div>"
)

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
        Title/headline of the post.
    text : str
        Main body content of the post.
    hashtags : List[str]
        Tags associated with the post.

    Returns
    -------
    str
        Escaped HTML string formatted according to USER_POST_FORMAT.
    """
    # Escape all user supplied strings
    safe_poster_name = html.escape(poster_name, quote=True)
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=True)

    # Build tag span elements
    tag_spans = []
    for tag in hashtags:
        # Ensure each tag is escaped and trimmed
        clean_tag = html.escape(tag.strip(), quote=True)
        if clean_tag:  # skip empty tags
            tag_spans.append(f"<span class='tag'>{clean_tag}</span>")

    tags_html = " ".join(tag_spans)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        poster_name=safe_poster_name,
        headline=safe_headline,
        text=safe_text,
        tags=tags_html
    )