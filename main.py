import streamlit as st
from file_translator.file_translator import FileTranslator

def main():
    st.title("File Translator")

    # Get input file
    input_file = st.file_uploader("Upload a .docx file", type=["docx"])

    # Get target language
    target_language = st.text_input("Enter target language (e.g., 'es' for Spanish)")

    if input_file and target_language:
        translator = FileTranslator()

        try:
            content = translator.extract_text_and_formatting_from_docx(input_file)
            st.write("Extracted Text:")
            for paragraph in content:
                for run in paragraph['runs']:
                    st.write(run['text'])

            translated_content = translator.translate_docx_content(content, target_language)
            output_file_name = f"translated_{input_file.name}"
            translated_file_path, message = translator.save_translated_docx(translated_content, output_file_name)
            st.success(message)

            with open(translated_file_path, "rb") as file:
                st.download_button(
                    label="Download Translated File",
                    data=file,
                    file_name=translated_file_path,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()