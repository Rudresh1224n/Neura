import fitz

def extract_resume_text(file_path):

    text = ""

    try:
        doc = fitz.open(file_path)

        for page in doc:
            text += page.get_text()

        return text

    except Exception as e:
        return ""