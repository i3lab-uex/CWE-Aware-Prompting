import html
from typing import List

# The forum post template.  Placeholders are `{header}`, `{message}` and `{options}`.
FORUM_POST_FORMAT = """<h2>{header}</h2>
<div>{message}</div>
{options}
"""

def _escape_markdown(md: str) -> str:
    """
    Escape a markdown string so that it is safe to render as HTML.
    This uses the `markdown2` library with `safe_mode="escape"`, which
    escapes any raw HTML in the markdown text.
    """
    try:
        import markdown2  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "markdown2 library is required to render options safely. "
            "Install it with `pip install markdown2`."
        ) from exc

    return markdown2.markdown(md, safe_mode="escape")

def construct_forum_content(
    heading: str,
    content: str,
    choices: List[str]
) -> str:
    """
    Construct a sanitized forum post containing a heading, body content,
    and an unordered list of options.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body text of the forum post.
    choices : List[str]
        A list of user-provided options or discussion points in markdown format.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post.
    """
    # Escape user input to prevent XSS
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Render each choice as a markdown list item and then wrap in <ul>
    ul_items = ""
    for choice in choices:
        # Escape the markdown text before rendering
        rendered_choice = _escape_markdown(choice)
        ul_items += f"<li>{rendered_choice}</li>\n"

    safe_options = f"<ul>\n{ul_items}</ul>"

    # Populate the template
    return FORUM_POST_FORMAT.format(
        header=safe_heading,
        message=safe_content,
        options=safe_options
    )