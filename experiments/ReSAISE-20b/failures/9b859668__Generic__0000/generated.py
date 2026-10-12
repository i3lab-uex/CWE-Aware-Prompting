import html
from typing import List

# Example format string.  In real usage this could be imported from a config module.
FORUM_POST_FORMAT = """<h1>{header}</h1>
<div class="post-body">
{message}
</div>
<ul class="options">
{options}
</ul>"""

def construct_forum_content(
    heading: str,
    content: str,
    choices: List[str]
) -> str:
    """
    Construct a sanitized forum post from the given heading, content and choices.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body text of the forum post. Markdown is not processed; it is
        escaped to prevent injection.
    choices : list[str]
        A list of options or discussion points. Each entry is treated as
        plain text and safely escaped before being wrapped in <li> tags.

    Returns
    -------
    str
        A fully formatted HTML snippet containing the header, body and options.
    """
    # Basic type checks
    if not isinstance(heading, str):
        raise TypeError("heading must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not isinstance(choices, list) or not all(isinstance(c, str) for c in choices):
        raise TypeError("choices must be a list of strings")

    # Escape the heading and content to avoid XSS
    safe_heading = html.escape(heading)
    safe_content = html.escape(content)

    # Convert each choice to a safely escaped <li> element
    safe_options = "\n".join(
        f"  <li>{html.escape(choice)}</li>" for choice in choices
    )

    # Assemble the final post using the template
    return FORUM_POST_FORMAT.format(
        header=safe_heading,
        message=safe_content,
        options=safe_options
    )