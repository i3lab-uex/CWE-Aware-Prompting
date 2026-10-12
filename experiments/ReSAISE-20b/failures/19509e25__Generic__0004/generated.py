import html

# The HTML template is expected to be defined elsewhere in the codebase.
# It should contain placeholders named `poster_name`, `headline`, `text`,
# and `tags`. For example:
#
# USER_POST_FORMAT = """
# <div class="post">
#   <h2>{headline}</h2>
#   <p class="author">Posted by: {poster_name}</p>
#   <div class="content">{text}</div>
#   <div class="tags">{tags}</div>
# </div>
# """

def compose_post_html(poster_name: str,
                      headline: str,
                      text: str,
                      hashtags: list[str]) -> str:
    """
    Construct an XSS‑safe HTML representation of a forum post.

    Parameters
    ----------
    poster_name : str
        Name of the user who posted.
    headline : str
        Title/headline of the post.
    text : str
        Main content/body of the post.
    hashtags : list[str]
        List of tags associated with the post.

    Returns
    -------
    str
        The HTML string ready to be rendered. All user supplied content is
        escaped to prevent cross‑site scripting attacks.

    Raises
    ------
    ValueError
        If any of the required arguments are missing or empty.
    """
    # Basic validation
    if not all([poster_name, headline, text]) or hashtags is None:
        raise ValueError("All arguments must be provided and non-empty")

    # Escape user input to prevent XSS
    safe_poster = html.escape(poster_name, quote=True)
    safe_headline = html.escape(headline, quote=True)
    safe_text = html.escape(text, quote=False)  # preserve newlines

    # Build tags string: each tag wrapped in <span>
    safe_tags = []
    for tag in hashtags:
        if not isinstance(tag, str):
            continue  # skip non‑string tags
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f'<span class="tag">{escaped_tag}</span>')

    tags_html = " ".join(safe_tags)

    # Format the final HTML using the predefined template
    try:
        formatted = USER_POST_FORMAT.format(
            poster_name=safe_poster,
            headline=safe_headline,
            text=safe_text.replace("\n", "<br>"),
            tags=tags_html
        )
    except NameError:
        raise RuntimeError("USER_POST_FORMAT is not defined in the current context")

    return formatted