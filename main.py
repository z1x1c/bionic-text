import fitz
import flet as ft
from flet import CrossAxisAlignment, FilePicker, Column, ElevatedButton, MainAxisAlignment, Row, Text, FilePickerResultEvent, icons, alignment
import os
import subprocess

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        blocks = page.get_text("blocks")
        previous_block_id = -1  # Initialize to an invalid block ID
        for block in blocks:
            if block[6] == 0:  # This checks if the block is a text block
                if previous_block_id != block[5]:
                    text += "\n\n"  # Add paragraph separation
                text += block[4]
                previous_block_id = block[5]
    return text

def make_bionic(text, font_size):
    # Create new PDF
    new_pdf = fitz.open()
    page = new_pdf.new_page(width=595, height=842)  # A4 size in points

    bold_font = "Times-Bold"
    regular_font = "Times-Roman"
    cursor_x = 72  # Starting x position for the text
    cursor_y = 72  # Starting y position for the text

    # words = text.strip().split()
    paragraphs = text.strip().split("\n\n")
    
    for paragraph in paragraphs:
        words = paragraph.strip().split()

        for word in words:
            # Split word into bold and regular parts
            index = len(word) // 2
            bold_part = word[:index]
            regular_part = word[index:]
            
            # Calculate width of bold part
            bold_width = fitz.get_text_length(bold_part, fontname=bold_font, fontsize=font_size)
            # Place bold text
            page.insert_text((cursor_x, cursor_y), bold_part, fontname=bold_font, fontsize=font_size)
            cursor_x += bold_width
            
            # Calculate width of regular part
            regular_width = fitz.get_text_length(regular_part, fontname=regular_font, fontsize=font_size)
            # Place regular text
            page.insert_text((cursor_x, cursor_y), regular_part, fontname=regular_font, fontsize=font_size)
            cursor_x += regular_width

                # Add space after the word before processing the next one
            space_width = fitz.get_text_length(" ", fontname=regular_font, fontsize=font_size)
            cursor_x += space_width

            # If cursor_x exceeds page width, reset cursor_x and increment cursor_y to start a new line
            if cursor_x > page.rect.width - 72:
                cursor_x = 72
                cursor_y += font_size * 1.5  # Moving cursor to the next line; 1.5 is line spacing factor

        cursor_x = 72
        cursor_y += font_size * 2
    
    if cursor_y == 72:
        del new_pdf[-1]

    return new_pdf

def bionic_pdf(pdf_path):
    # pdf_path = './test/sample-text-3.pdf'
    extracted_text = extract_text(pdf_path)  # Use the new extract_text function

    # Create a new bionic PDF with the extracted text
    new_pdf = make_bionic(extracted_text, 11)

    directory, original_filename = os.path.split(pdf_path)
    basename, ext = os.path.splitext(original_filename)
    new_filename = f"{basename}-bionic{ext}"
    new_pdf_path = os.path.join(directory, new_filename)

    # Save the new PDF
    new_pdf.save(new_pdf_path)
    new_pdf.close()

    return new_pdf_path

def main(page: ft.Page):
    page.title = "Bionic Text Converter"

    info_text = Text()

    def file_picked(e: FilePickerResultEvent):
        if e.files:
            uploaded_file = e.files[0]
            new_pdf_path = bionic_pdf(uploaded_file.path)
            subprocess.call(['open', new_pdf_path])
        else:
            info_text.value = "Please upload a PDF file."
        page.update()

    file_picker = FilePicker(on_result=file_picked)
    
    drop_zone = ElevatedButton(
        text="Click here to select a PDF file.",
        icon=icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(),
    )

    col = Column(
            controls=[drop_zone, file_picker, info_text],
            alignment=MainAxisAlignment.CENTER,
        )
    row = Row(
            controls=[col],
            alignment=MainAxisAlignment.CENTER,
            expand=True,
            )
    page.add(row)

if __name__ == "__main__":
    ft.app(target=main)
