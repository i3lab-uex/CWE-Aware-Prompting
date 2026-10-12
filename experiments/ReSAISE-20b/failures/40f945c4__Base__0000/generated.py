import html

# Predefined HTML template for a user post.
# The placeholders are named to match the function arguments.
USER_POST_FORMAT = """
<article class="post">
    <header>
        <h2>{post_heading}</h2>
        <p class="author">Posted by: {user_name}</p>
    </header>
    <section class="content">
        {post_content}
    </section>
    <footer class="tags">
        {post_tags}
    </footer>
</article>
"""

def build_post_html(user_name: str,
                    post_heading: str,
                    post_content: str,
                    post_tags: list[str]) -> str:
    """
    Generates a sanitized HTML representation of a user's forum post.

    Parameters
    ----------
    user_name : str
        The author of the post.
    post_heading : str
        The title of the user's post.
    post_content : str
        The main content of the user's post.
    post_tags : list[str]
        A list of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string ready for rendering in a browser.
    """
    # Escape all user-controlled input to prevent XSS (CWE-79)
    safe_user_name = html.escape(user_name, quote=True)
    safe_post_heading = html.escape(post_heading, quote=True)

    # Post content may contain line breaks; preserve them as <br> tags.
    # We also escape to prevent script injection.
    escaped_content = html.escape(post_content, quote=True).replace("\n", "<br>")

    # Build the tags section: each tag is wrapped in a <span>.
    escaped_tags = []
    for tag in post_tags:
        # Ensure each tag is a string and escape it
        escaped_tag = html.escape(str(tag), quote=True)
        escaped_tags.append(f'<span class="tag">{escaped_tag}</span>')

    safe_post_tags = " ".join(escaped_tags)

    # Format the final HTML using the predefined template.
    return USER_POST_FORMAT.format(
        user_name=safe_user_name,
        post_heading=safe_post_heading,
        post_content=escaped_content,
        post_tags=safe_post_tags
    )