from io import BytesIO
import os
from pptx import Presentation
from docx import Document
import openpyxl
import fitz
from googletrans import Translator
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class FileTranslator:
    def extract_text_from_docx(self, file):
        extracted_text = ""
        doc = Document(file)
        for paragraph in doc.paragraphs:
            extracted_text += paragraph.text + "\n"
        return extracted_text

    def extract_text_from_pptx(self, file):
        extracted_text = ""
        presentation = Presentation(file)
        for slide in presentation.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    extracted_text += shape.text + "\n"
        return extracted_text

    def extract_text_from_pdf(self, file):
        extracted_text = ""
        file_bytes = BytesIO(file.read())
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        for page in pdf_document:
            extracted_text += page.get_text()
        return extracted_text

    def extract_text_from_xlsx(self, file):
        extracted_text = ""
        try:
            wb = openpyxl.load_workbook(file)
            for sheet in wb.sheetnames:
                ws = wb[sheet]
                for row in ws.iter_rows(values_only=True):
                    for cell in row:
                        if cell:
                            extracted_text += str(cell) + "\n"
        except Exception as e:
            print(f"Error extracting text from XLSX: {e}")
        return extracted_text

    def extract_text_from_txt(self, file):
        extracted_text = ""
        extracted_text = file.read().decode("utf-8")
        return extracted_text

    def extract_text_from_properties(self, file):
        extracted_text = ""
        for line in file:
            line = line.decode("utf-8").strip()
            if line and not line.startswith('#'):
                key_value = line.split('=', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    extracted_text += f"{key.strip()}={value.strip()}\n"
        return extracted_text

    def translate_text(self, text, target_language):
        try:
            translator = Translator()
            translated = translator.translate(text, dest=target_language)
            return translated.text
        except Exception as e:
            print(f"Translation failed: {e}")
            return None

    def save_translated_text(self, translated_text, file_name):
        file_name, file_extension = os.path.splitext(file_name)
        translated_file_path = f"{file_name}_translated{file_extension}"
        try:
            if file_extension.lower() == '.docx':
                doc = Document()
                for paragraph in translated_text.split('\n'):
                    doc.add_paragraph(paragraph)
                doc.save(translated_file_path)
            elif file_extension.lower() == '.pptx':
                presentation = Presentation()
                for slide_text in translated_text.split('\n\n'):
                    slide = presentation.slides.add_slide(presentation.slide_layouts[5])
                    text_frame = slide.shapes.add_textbox(0, 0, 1, 1).text_frame
                    text_frame.text = slide_text
                presentation.save(translated_file_path)
            elif file_extension.lower() == '.pdf':
                styles = getSampleStyleSheet()
                doc = SimpleDocTemplate(translated_file_path, pagesize=letter)
                elements = []
                for paragraph in translated_text.split('\n'):
                    elements.append(Paragraph(paragraph, styles["BodyText"]))
                doc.build(elements)
            elif file_extension.lower() == '.xlsx':
                translated_workbook = openpyxl.Workbook()
                translated_sheet = translated_workbook.active
                for line in translated_text.split('\n'):
                    translated_sheet.append([line])
                translated_workbook.save(translated_file_path)
            elif file_extension.lower() == '.txt':
                with open(translated_file_path, 'w', encoding='utf-8') as file:
                    file.write(translated_text)
            else:
                print("Unsupported file format.")
                return None
        except Exception as e:
            print(f"Error saving translated file: {e}")
            return None
        return translated_file_path