import html

# Predefined HTML structure for a blog post.
# The placeholders {title} and {body} will be replaced by the sanitized heading
# and description respectively.
BLOG_FORMAT = """
<article class="blog-post">
  <header>
    <h1>{title}</h1>
  </header>
  <section class="post-body">
    {body}
  </section>
</article>
"""

def display_blog(heading: str, description: str) -> str:
    """
    Prepare a user‑submitted blog post for safe web display.

    Parameters
    ----------
    heading : str
        The main heading or subject of the blog post.
    description : str
        The complete textual content of the blog post.

    Returns
    -------
    str
        A string containing the sanitized and HTML‑formatted blog post,
        ready for secure presentation on a webpage.

    Notes
    -----
    * The heading and description are escaped using `html.escape` to prevent
      injection of HTML or JavaScript.
    * Newlines in the description are converted to <br> tags so that
      paragraph breaks are preserved.
    * The function does not perform full Markdown or rich‑text parsing;
      it simply escapes and formats the raw text.
    """
    if not isinstance(heading, str):
        raise TypeError("heading must be a string")
    if not isinstance(description, str):
        raise TypeError("description must be a string")

    # Escape special HTML characters to prevent injection.
    safe_heading = html.escape(heading, quote=True)
    # Escape description and preserve line breaks.
    safe_description = html.escape(description, quote=True).replace("\n", "<br>\n")

    # Format the final HTML using the predefined template.
    formatted_post = BLOG_FORMAT.format(title=safe_heading, body=safe_description)

    return formatted_post