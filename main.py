import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from pptx import Presentation
from docx import Document
import openpyxl
import fitz
from googletrans import Translator
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from file_translator.file_translator import FileTranslator

if __name__ == "__main__":
    file_translator = FileTranslator()
    file_translator.run()