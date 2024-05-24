import streamlit as st
from file_translator.file_translator import FileTranslator

def app():
    st.title("File Translator")

    # Get input file
    input_file = st.file_uploader("Upload a file", type=["docx", "pptx", "pdf", "xlsx", "txt", "properties"])

    # Get target language
    target_language = st.text_input("Enter target language code (e.g., 'es' for Spanish)")

    if input_file and target_language:
        translator = FileTranslator()
        file_extension = input_file.name.split(".")[-1].lower()

        if file_extension == "docx":
            extracted_text = translator.extract_text_from_docx(input_file)
        elif file_extension == "pptx":
            extracted_text = translator.extract_text_from_pptx(input_file)
        elif file_extension == "pdf":
            extracted_text = translator.extract_text_from_pdf(input_file)
        elif file_extension == "xlsx":
            extracted_text = translator.extract_text_from_xlsx(input_file)
        elif file_extension == "txt":
            extracted_text = translator.extract_text_from_txt(input_file)
        elif file_extension == "properties":
            extracted_text = translator.extract_text_from_properties(input_file)
        else:
            st.error("Unsupported file format.")
            return

        if extracted_text:
            translated_text = translator.translate_text(extracted_text, target_language)
            if translated_text:
                translated_file_path = translator.save_translated_text(translated_text, input_file.name)
                if translated_file_path:
                    st.success(f"Translated content saved as: {translated_file_path}")

                    with open(translated_file_path, "rb") as file:
                        btn = st.download_button(
                            label="Download Translated File",
                            data=file,
                            file_name=translated_file_path,
                            mime=f"application/{file_extension}"
                        )
                    
                    # Display translated text
                    st.write("Translated Text:")
                    st.text_area("", translated_text, height=200)
                else:
                    st.error("Failed to save translated content.")
            else:
                st.error("Translation failed.")
        else:
            st.error("Failed to extract text from input file.") 
        
if __name__ == "__main__":
    app()
