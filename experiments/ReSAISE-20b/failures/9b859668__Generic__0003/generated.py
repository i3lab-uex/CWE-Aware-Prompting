import html
from typing import List

# Define a simple template for the forum post.
FORUM_POST_FORMAT = """<article>
  <header><h1>{heading}</h1></header>
  <section>{content}</section>
  {options_section}
</article>"""


def construct_forum_content(
    heading: str,
    content: str,
    choices: List[str]
) -> str:
    """
    Construct a sanitized forum post from user-provided data.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body text of the forum post.
    choices : list[str]
        A collection of user-provided options or discussion points
        in markdown format.

    Returns
    -------
    str
        A fully rendered HTML string containing the header, content,
        and an unordered list of options.

    Notes
    -----
    All user-provided strings are escaped with html.escape to prevent
    injection attacks. The markdown in `choices` is not parsed; it is
    simply displayed verbatim inside list items.
    """
    # Escape user inputs to avoid XSS
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build the options list
    if choices:
        escaped_items = [
            f"  <li>{html.escape(choice, quote=True)}</li>"
            for choice in choices
        ]
        options_section = (
            "<section>\n  <ul>\n"
            + "\n".join(escaped_items)
            + "\n  </ul>\n</section>"
        )
    else:
        options_section = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        heading=safe_heading,
        content=safe_content,
        options_section=options_section
    )