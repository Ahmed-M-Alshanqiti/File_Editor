from django import template

register = template.Library()

@register.filter
def force_str(uploaded_file):
    try:
        # Reset pointer before reading
        uploaded_file.open()
        content = uploaded_file.read()
        return content.decode('utf-8', errors='ignore')
    except:
        return "⚠ Unable to preview this text file."
