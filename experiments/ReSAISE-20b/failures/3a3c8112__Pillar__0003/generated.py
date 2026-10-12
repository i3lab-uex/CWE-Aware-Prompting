import html

def construct_html_response(content: str, html_template: str) -> str:
    """
    Injects user-provided content into an HTML template after escaping it.

    Args:
        content (str): The dynamic user-supplied content.
        html_template (str): The HTML template containing a `{user_content}` placeholder.

    Returns:
        str: The final HTML string with the escaped content inserted.
    """
    # Escape special HTML characters to prevent injection
    safe_content = html.escape(content, quote=True)

    # Replace the placeholder with the escaped content
    final_html = html_template.replace("{user_content}", safe_content)

    return final_html