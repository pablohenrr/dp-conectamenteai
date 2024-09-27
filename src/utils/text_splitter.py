from io import StringIO

def split_text(text, max_tokens=5000):
    words = text.split()
    segments = []
    current_segment = StringIO()
    current_length = 0

    for word in words:
        word_length = len(word) + 1 
        if current_length + word_length > max_tokens:
            segments.append(current_segment.getvalue().strip())
            current_segment = StringIO()
            current_length = 0
        current_segment.write(word + ' ')
        current_length += word_length

    if current_length > 0:
        segments.append(current_segment.getvalue().strip())

    return segments
