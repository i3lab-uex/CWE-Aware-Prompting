import html

# Predefined template for displaying a blog post.
BLOG_FORMAT = (
    "<article>\n"
    "  <h1>{subject}</h1>\n"
    "  <div class=\"content\">{description}</div>\n"
    "</article>"
)


def publish_blog_article(subject: str, description: str) -> str:
    """
    Return a sanitized and formatted blog post ready for safe display.

    Parameters
    ----------
    subject : str
        The heading of the blog post.
    description : str
        The main text content of the blog post.

    Returns
    -------
    str
        The HTML string containing the escaped title and body.

    Raises
    ------
    TypeError
        If either argument is not a string.
    ValueError
        If either argument is an empty string after stripping whitespace.
    """
    if not isinstance(subject, str):
        raise TypeError("subject must be a string")
    if not isinstance(description, str):
        raise TypeError("description must be a string")

    # Trim whitespace and ensure non-empty content
    subject_clean = subject.strip()
    description_clean = description.strip()

    if not subject_clean:
        raise ValueError("subject cannot be empty")
    if not description_clean:
        raise ValueError("description cannot be empty")

    # Escape HTML special characters to prevent XSS
    subject_escaped = html.escape(subject_clean, quote=True)
    description_escaped = html.escape(description_clean, quote=True)

    # Format the blog post using the predefined template
    formatted_blog = BLOG_FORMAT.format(
        subject=subject_escaped,
        description=description_escaped
    )

    return formatted_blog