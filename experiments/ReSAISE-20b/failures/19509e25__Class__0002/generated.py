import html

# Pre‑defined template with named placeholders.  The actual format is up to the
# application but should contain `{poster_name}`, `{headline}`, `{text}` and
# `{tags}`.
USER_POST_FORMAT = (
    "<article class=\"post\">\n"
    "  <header>\n"
    "    <h2>{headline}</h2>\n"
    "    <p class=\"author\">Posted by {poster_name}</p>\n"
    "  </header>\n"
    "  <section class=\"content\">\n"
    "    {text}\n"
    "  </section>\n"
    "  <footer class=\"tags\">\n"
    "    {tags}\n"
    "  </footer>\n"
    "</article>"
)


def compose_post_html(
    poster_name: str,
    headline: str,
    text: str,
    hashtags: list[str],
) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    poster_name : str
        Name of the user who posted.
    headline : str
        Title of the post.
    text : str
        Main body content of the post.  Newlines are preserved.
    hashtags : list[str]
        List of tags to be displayed, each wrapped in a <span> element.

    Returns
    -------
    str
        Safely escaped HTML string ready to be embedded in a page.
    """
    # Escape all user supplied strings so that any HTML or script tags are
    # rendered harmless.  We use html.escape which converts &, <, > and ".
    safe_poster_name = html.escape(poster_name, quote=True)
    safe_headline = html.escape(headline, quote=True)

    # Preserve paragraph breaks in the main text by converting newlines to <br>.
    # This is a simple approach; more sophisticated formatting could be used.
    safe_text = html.escape(text, quote=True).replace("\n", "<br>")

    # Render each tag inside a <span>.  Tags themselves are escaped as well.
    rendered_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in hashtags
    )

    # Insert the escaped components into the template.
    return USER_POST_FORMAT.format(
        poster_name=safe_poster_name,
        headline=safe_headline,
        text=safe_text,
        tags=rendered_tags,
    )