import html
from typing import List

# Example template (the actual one may be defined elsewhere in the application)
USER_POST_FORMAT = (
    "<div class=\"post\">\n"
    "  <h2>{headline}</h2>\n"
    "  <p class=\"author\">Posted by {poster_name}</p>\n"
    "  <div class=\"content\">{text}</div>\n"
    "  <div class=\"tags\">{tags}</div>\n"
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
        The name of the author.
    headline : str
        The post headline.
    text : str
        The main content of the post.
    hashtags : List[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        The escaped HTML string ready for rendering in a browser.
    """
    # Escape all user‑supplied data to prevent injection
    safe_poster_name = html.escape(poster_name, quote=True)
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=False)

    # Build the tags section; each tag is wrapped in a <span>
    safe_tags = ""
    for tag in hashtags:
        # Normalize the tag: strip whitespace, escape special chars
        cleaned_tag = html.escape(tag.strip(), quote=True)
        if cleaned_tag:  # Skip empty tags
            safe_tags += f"<span class=\"tag\">{cleaned_tag}</span> "

    # Strip trailing space from tags string
    safe_tags = safe_tags.rstrip()

    # Compose the final HTML using the template
    return USER_POST_FORMAT.format(
        poster_name=safe_poster_name,
        headline=safe_headline,
        text=safe_text,
        tags=safe_tags
    )