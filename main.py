import fitz

def make_bionic(text, font_size):
    # Create new PDF
    new_pdf = fitz.open()
    page = new_pdf.new_page(width=595, height=842)  # A4 size in points

    bold_font = "Times-Bold"
    regular_font = "Times-Roman"
    cursor_x = 72  # Starting x position for the text
    cursor_y = 72  # Starting y position for the text

    words = text.strip().split()

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

    return new_pdf

def main():
    # Open the existing PDF and extract text
    pdf = fitz.open("./test/sample-text-2.pdf")
    extracted_text = ""
    for page in pdf:
        extracted_text += page.get_text("text")

    # Close the original PDF file
    pdf.close()

    # Create a new bionic PDF with the extracted text
    new_pdf = make_bionic(extracted_text, 11)

    # Save the new PDF
    new_pdf.save("./test/bionic-text.pdf")
    new_pdf.close()

if __name__ == "__main__":
    main()
