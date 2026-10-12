import html
from typing import List

# A simple template for forum posts.
FORUM_POST_FORMAT = """
<h2>{header}</h2>
<div class="post-body">
{body}
</div>
<ul class="options-list">
{options}
</ul>
"""

def build_forum_post(title: str, post_body: str, options_list: List[str]) -> str:
    """
    Construct a formatted forum post.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    post_body : str
        The main content or body of the forum post.
    options_list : list[str]
        A collection of user‑provided options or discussion points.

    Returns
    -------
    str
        The sanitized and formatted forum post.

    Raises
    ------
    TypeError
        If ``options_list`` is not a list or if any item in it is not a string.
    """
    # Validate input types
    if not isinstance(options_list, list):
        raise TypeError("options_list must be a list")
    for idx, opt in enumerate(options_list):
        if not isinstance(opt, str):
            raise TypeError(f"option at index {idx} is not a string")

    # Sanitize title and body
    safe_title = html.escape(title)
    safe_body = html.escape(post_body).replace("\n", "<br>")

    # Render options as an HTML unordered list
    safe_options = "\n".join(
        f"  <li>{html.escape(opt)}</li>" for opt in options_list
    )

    # Build final post using the template
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=safe_options
    )