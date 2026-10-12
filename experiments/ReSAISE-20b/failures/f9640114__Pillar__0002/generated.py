import html
from typing import List

# A simple template for the forum post.  The placeholders are:
#   {header}  – The title of the post
#   {body}    – The main content of the post
#   {options} – A rendered HTML unordered list of options
FORUM_POST_FORMAT = (
    "<div class='forum-post'>\n"
    "  <h2>{header}</h2>\n"
    "  <div class='post-body'>\n{body}\n  </div>\n"
    "  <div class='post-options'>\n{options}\n  </div>\n"
    "</div>"
)

def build_forum_post(title: str, post_body: str, options_list: List[str]) -> str:
    """
    Construct a sanitized forum post with the given title, body, and options.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    post_body : str
        The main content or body of the forum post.  It may contain user-provided
        text that could include characters with special meaning in HTML.
    options_list : List[str]
        A collection of user-provided options or discussion points in markdown
        format.  Each option is rendered as an <li> element inside a <ul>.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post.  All user
        supplied content is escaped to prevent XSS or injection attacks.

    Raises
    ------
    ValueError
        If any of the arguments are not of the expected type.
    """
    # Validate argument types
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    if not isinstance(post_body, str):
        raise ValueError("post_body must be a string")
    if not isinstance(options_list, list) or not all(isinstance(opt, str) for opt in options_list):
        raise ValueError("options_list must be a list of strings")

    # Escape user input to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Render options as an unordered list
    if options_list:
        rendered_options = "<ul>\n"
        for opt in options_list:
            safe_opt = html.escape(opt, quote=True)
            rendered_options += f"    <li>{safe_opt}</li>\n"
        rendered_options += "</ul>"
    else:
        rendered_options = "<p>No options provided.</p>"

    # Compose the final post using the template
    forum_post = FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=rendered_options
    )

    return forum_post