import html

# Example template; adjust placeholders as needed.
FORUM_POST_FORMAT = """
<h1>{header}</h1>
<div class="post-body">{body}</div>
<ul class="options">
{options}
</ul>
"""

def construct_forum_content(heading: str, content: str, choices: list[str]) -> str:
    """
    Construct a safe, formatted forum post.

    Parameters
    ----------
    heading : str
        The title or subject line of the forum post.
    content : str
        The main body text of the forum post.
    choices : list[str]
        A list of discussion options or points, provided in markdown.

    Returns
    -------
    str
        A sanitized HTML string containing the formatted forum post.
    """
    # Sanitize all user input to prevent XSS
    safe_heading = html.escape(heading, quote=True)
    safe_content = html.escape(content, quote=True)

    # Convert each choice into a list item; escape each choice
    safe_choices = []
    for choice in choices:
        escaped_choice = html.escape(choice, quote=True)
        safe_choices.append(f"    <li>{escaped_choice}</li>")

    # Join the list items into a single string
    options_html = "\n".join(safe_choices)

    # Format the final post using the template
    formatted_post = FORUM_POST_FORMAT.format(
        header=safe_heading,
        body=safe_content,
        options=options_html
    )

    return formatted_post.strip()