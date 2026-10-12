import html

def create_html_output(input_text: str, html_template: str) -> str:
    """
    Create an HTML string by safely inserting user-provided content into a template.

    Args:
        input_text: The raw text supplied by the user.
        html_template: An HTML string containing a single placeholder `{user_content}`.

    Returns:
        A new HTML string with the user content escaped to prevent injection.
    """
    # Escape special characters in the user input
    safe_content = html.escape(input_text, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)