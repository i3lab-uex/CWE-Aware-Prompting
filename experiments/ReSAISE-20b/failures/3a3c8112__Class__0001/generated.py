import html

def construct_html_response(content: str, html_template: str) -> str:
    """
    Injects user-provided content into an HTML template after escaping it to prevent
    HTML injection attacks (CWE-74).

    Args:
        content: The raw user input that will be inserted into the template.
        html_template: A string containing the HTML structure with a single
                       placeholder `{user_content}`.

    Returns:
        A string containing the final HTML with the escaped user content.
    """
    # Escape special HTML characters to neutralize injection attempts
    safe_content = html.escape(content, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.format(user_content=safe_content)