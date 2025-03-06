import sys
import os
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.units import mm
import base64
import io
import zipfile
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

# Add fonts that support Turkish characters with bold and italic variations
pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', 'DejaVuSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Italic', 'DejaVuSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSerif-BoldItalic', 'DejaVuSerif-BoldItalic.ttf'))

# Create font family
pdfmetrics.registerFontFamily('DejaVuSerif', normal='DejaVuSerif', bold='DejaVuSerif-Bold',
                             italic='DejaVuSerif-Italic', boldItalic='DejaVuSerif-BoldItalic')

def is_zip_file(file_path):
    """Check if the file is a valid ZIP file"""
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            return True
    except zipfile.BadZipFile:
        return False

def get_alignment_style(alignment_value):
    """Convert alignment value from XML to reportlab alignment constant"""
    if alignment_value == "1":
        return TA_CENTER
    elif alignment_value == "3":
        return TA_JUSTIFY
    elif alignment_value == "2":
        return TA_RIGHT
    else:
        return TA_LEFT

def udf_to_pdf(udf_file, pdf_file):
    root = None
    
    # Check if the file is a ZIP file
    if is_zip_file(udf_file):
        # Process as a ZIP file
        with zipfile.ZipFile(udf_file, 'r') as z:
            if 'content.xml' in z.namelist():
                with z.open('content.xml') as content_file:
                    tree = ET.parse(content_file, parser=ET.XMLParser(encoding='utf-8'))
                    root = tree.getroot()
            else:
                print("The 'content.xml' file could not be found in the UDF file.")
                exit()
    else:
        # Process as an XML file directly
        try:
            tree = ET.parse(udf_file, parser=ET.XMLParser(encoding='utf-8'))
            root = tree.getroot()
        except ET.ParseError:
            print(f"The file {udf_file} is neither a valid ZIP nor a valid XML file.")
            exit()

    if root is None:
        print("Failed to parse the file.")
        exit()

    # Retrieve content text
    content_element = root.find('content')
    if content_element is not None:
        content_text = content_element.text
        if content_text.startswith('<![CDATA[') and content_text.endswith(']]>'):
            content_text = content_text[9:-3]
    else:
        print("'content' could not be found in the XML.")
        exit()

    # Process the 'elements' section
    elements_element = root.find('elements')
    if elements_element is not None:
        # Create the PDF document
        pdf = SimpleDocTemplate(pdf_file, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Define a base style that supports Turkish characters
        base_style = ParagraphStyle('CustomNormal', 
                                   parent=styles['Normal'],
                                   fontName='DejaVuSerif',
                                   encoding='utf-8')
        
        # Define styles for bold and italic text
        bold_style = ParagraphStyle('CustomBold',
                                   parent=base_style,
                                   fontName='DejaVuSerif-Bold')
        
        italic_style = ParagraphStyle('CustomItalic',
                                     parent=base_style,
                                     fontName='DejaVuSerif-Italic')
        
        bold_italic_style = ParagraphStyle('CustomBoldItalic',
                                         parent=base_style,
                                         fontName='DejaVuSerif-BoldItalic')

        content_buffer = content_text

        for elem in elements_element:
            if elem.tag == 'paragraph':
                # Get paragraph alignment
                alignment = elem.get('Alignment', '0')
                alignment_style = get_alignment_style(alignment)
                
                # Create a custom style for this paragraph with the right alignment
                para_style = ParagraphStyle(
                    f'Style{alignment}',
                    parent=base_style,
                    alignment=alignment_style
                )
                
                # Process the paragraph content
                paragraph_text = ''
                for child in elem:
                    if child.tag == 'content':
                        # Get and format the text
                        start_offset = int(child.get('startOffset', '0'))
                        length = int(child.get('length', '0'))
                        text = content_buffer[start_offset:start_offset+length]

                        # Get font size if specified
                        if child.get('size'):
                            font_size = float(child.get('size'))
                            para_style.fontSize = font_size

                        # Get style information
                        bold = child.get('bold', 'false') == 'true'
                        italic = child.get('italic', 'false') == 'true'
                        
                        # Set font properties based on style
                        current_style = para_style.clone('temp_style')
                        if bold and italic:
                            current_style.fontName = 'DejaVuSerif-BoldItalic'
                            paragraph_text += f"<b><i>{text}</i></b>"
                        elif bold:
                            current_style.fontName = 'DejaVuSerif-Bold'
                            paragraph_text += f"<b>{text}</b>"
                        elif italic:
                            current_style.fontName = 'DejaVuSerif-Italic'
                            paragraph_text += f"<i>{text}</i>"
                        else:
                            paragraph_text += text
                    elif child.tag == 'field':
                        # Process field element (labels like DAVACI, VEKİLİ, etc.)
                        field_name = child.get('fieldName', '')
                        
                        # Get the text from the content buffer if startOffset and length are provided
                        if child.get('startOffset') and child.get('length'):
                            start_offset = int(child.get('startOffset', '0'))
                            length = int(child.get('length', '0'))
                            field_text = content_buffer[start_offset:start_offset+length]
                        else:
                            # Use the fieldName as fallback
                            field_text = field_name
                        
                        # Apply styling 
                        style = ''
                        if child.get('bold', 'false') == 'true':
                            style += '<b>'
                        if child.get('italic', 'false') == 'true':
                            style += '<i>'
                        
                        paragraph_text += f"{style}{field_text}"
                        
                        # Closing tags
                        if 'i' in style:
                            paragraph_text += '</i>'
                        if 'b' in style:
                            paragraph_text += '</b>'
                    elif child.tag == 'space':
                        paragraph_text += ' '
                    elif child.tag == 'image':
                        # Add the image
                        image_data = child.get('imageData')
                        if image_data:
                            image_bytes = base64.b64decode(image_data)
                            image_stream = io.BytesIO(image_bytes)
                            img = Image(image_stream)
                            elements.append(img)

                # Add the paragraph with correct alignment
                elements.append(Paragraph(paragraph_text, para_style))
                elements.append(Spacer(1, 5))
            elif elem.tag == 'table':
                # Create the table
                table_data = []
                rows = elem.findall('row')
                for row in rows:
                    row_data = []
                    cells = row.findall('cell')
                    for cell in cells:
                        cell_text = ''
                        paragraphs = cell.findall('paragraph')
                        for para in paragraphs:
                            # Get paragraph alignment
                            alignment = para.get('Alignment', '0')
                            alignment_style = get_alignment_style(alignment)
                            
                            # Create a custom style for this cell with the right alignment
                            cell_style = ParagraphStyle(
                                f'CellStyle{alignment}',
                                parent=base_style,
                                alignment=alignment_style
                            )
                            
                            for child in para:
                                if child.tag == 'content':
                                    start_offset = int(child.get('startOffset', '0'))
                                    length = int(child.get('length', '0'))
                                    text = content_buffer[start_offset:start_offset+length]

                                    # Get font size if specified
                                    if child.get('size'):
                                        font_size = float(child.get('size'))
                                        cell_style.fontSize = font_size

                                    # Get style information
                                    bold = child.get('bold', 'false') == 'true'
                                    italic = child.get('italic', 'false') == 'true'
                                    
                                    # Set font properties based on style
                                    current_style = cell_style.clone('temp_cell_style')
                                    if bold and italic:
                                        current_style.fontName = 'DejaVuSerif-BoldItalic'
                                        cell_text += f"<b><i>{text}</i></b>"
                                    elif bold:
                                        current_style.fontName = 'DejaVuSerif-Bold'
                                        cell_text += f"<b>{text}</b>"
                                    elif italic:
                                        current_style.fontName = 'DejaVuSerif-Italic'
                                        cell_text += f"<i>{text}</i>"
                                    else:
                                        cell_text += text
                                elif child.tag == 'field':
                                    # Process field element for table cells
                                    field_name = child.get('fieldName', '')
                                    
                                    # Get the text from the content buffer
                                    if child.get('startOffset') and child.get('length'):
                                        start_offset = int(child.get('startOffset', '0'))
                                        length = int(child.get('length', '0'))
                                        field_text = content_buffer[start_offset:start_offset+length]
                                    else:
                                        # Use the fieldName as fallback
                                        field_text = field_name
                                    
                                    # Apply styling 
                                    style = ''
                                    if child.get('bold', 'false') == 'true':
                                        style += '<b>'
                                    if child.get('italic', 'false') == 'true':
                                        style += '<i>'
                                    
                                    cell_text += f"{style}{field_text}"
                                    
                                    # Closing tags
                                    if 'i' in style:
                                        cell_text += '</i>'
                                    if 'b' in style:
                                        cell_text += '</b>'
                                elif child.tag == 'space':
                                    cell_text += ' '
                                elif child.tag == 'image':
                                    # Images may not be supported inside tables
                                    pass
                        row_data.append(Paragraph(cell_text, cell_style))
                    table_data.append(row_data)
                # Set the table style
                table_style = TableStyle([
                    ('GRID', (0,0), (-1,-1), 1, colors.black),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ])
                table = Table(table_data)
                table.setStyle(table_style)
                elements.append(table)
                elements.append(Spacer(1, 5))
        # Build the PDF document
        pdf.build(elements)
        print(f"PDF file created: {pdf_file}")
    else:
        print("'elements' could not be found in the XML.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python udf_to_pdf.py input.udf")
        exit()

    udf_file = sys.argv[1]

    if not os.path.isfile(udf_file):
        print(f"Input file not found: {udf_file}")
        exit()

    filename, ext = os.path.splitext(udf_file)

    if ext.lower() == '.udf':
        pdf_file = filename + '.pdf'
        udf_to_pdf(udf_file, pdf_file)
    else:
        print("Please provide a .udf file.")

if __name__ == '__main__':
    main()