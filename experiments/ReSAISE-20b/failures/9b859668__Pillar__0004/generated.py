import html
from typing import List

# Predefined template for forum posts.  The placeholders are expected to be
# formatted using str.format().
FORUM_POST_FORMAT: str = (
    "<div class='forum-post'>\n"
    "  <h2>{header}</h2>\n"
    "  <div class='post-content'>\n{message}\n  </div>\n"
    "  <ul class='options'>\n{options}\n  </ul>\n"
    "</div>"
)


def construct_forum_content(
    heading: str,
    content: str,
    choices: List[str]
) -> str:
    """
    Construct a sanitized forum post from user-provided heading, content,
    and a list of options.  The options are rendered as an HTML unordered
    list (<ul>).

    Args:
        heading: The title or subject line of the forum post.
        content: The main body text of the forum post.
        choices: A list of user-provided options or discussion points
                 (in markdown format).

    Returns:
        A string containing the fully formatted and sanitized forum post.

    Raises:
        ValueError: If any required argument is missing or if the choices
                    list is empty.
    """
    # Basic validation of arguments
    if not isinstance(heading, str) or not heading.strip():
        raise ValueError("Heading must be a non-empty string.")
    if not isinstance(content, str):
        raise ValueError("Content must be a string.")
    if not isinstance(choices, list) or not choices:
        raise ValueError("Choices must be a non-empty list of strings.")
    if any(not isinstance(c, str) for c in choices):
        raise ValueError("All choices must be strings.")

    # Escape heading and content to prevent XSS or injection
    safe_heading = html.escape(heading.strip())
    # Preserve line breaks in content by converting \n to <br>
    safe_content = html.escape(content).replace("\n", "<br>")

    # Build the options list.  Each choice is escaped and wrapped in <li>.
    option_items = []
    for idx, choice in enumerate(choices, start=1):
        # Strip surrounding whitespace and escape
        escaped_choice = html.escape(choice.strip())
        option_items.append(f"    <li>{escaped_choice}</li>")

    options_html = "\n".join(option_items)

    # Assemble the final post using the template
    formatted_post = FORUM_POST_FORMAT.format(
        header=safe_heading,
        message=safe_content,
        options=options_html
    )

    return formatted_post