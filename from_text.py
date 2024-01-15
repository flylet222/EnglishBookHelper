import fitz
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from gpt import translate_by_box


def english_book_helper(pdf_path, pdf_save):
    c = canvas.Canvas(pdf_save)
    pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic.ttf'))
    for page_layout in extract_pages(pdf_path):
        c.setPageSize((page_layout.width, page_layout.height))
        text_list, coord_list = extract_txt_one_page(page_layout)
        translated = translate_by_box(text_list)

        for text, coord in zip(translated, coord_list):
            styles = getSampleStyleSheet()
            custom_style = ParagraphStyle('CustomStyle', parent=styles['Normal'], fontName='NanumGothic', fontSize=9)
            p = Paragraph(text, custom_style)
            p.wrapOn(c, coord[2]-coord[0] + 10, coord[3]-coord[1])
            p.drawOn(c, coord[0], coord[1])
        c.showPage()
    c.save()
    

def extract_txt_one_page(page_layout):
    text_list = []
    coord_list = []
    current_coord = (10000, 10000, 10000, 10000)
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            if len(element.get_text()) > 100:
                if -5 < current_coord[0] - element.bbox[0] < 5 and current_coord[1] - element.bbox[3] < 3:
                    text_list[-1] += " " + element.get_text()
                    coord_list[-1] = (element.bbox[0], element.bbox[1], current_coord[2], current_coord[3])
                else:
                    text_list.append(element.get_text())
                    coord_list.append(element.bbox) # (x0, y0, x1, y1) = bbox
                current_coord = element.bbox
    return text_list, coord_list


def merge_pdfs_with_margin(file1, file2, output_file, margin=10):
    pdf1 = fitz.open(file1)
    pdf2 = fitz.open(file2)

    output_pdf = fitz.open()

    for i in range(pdf1.page_count):
        page1 = pdf1.load_page(i)
        page2 = pdf2.load_page(i)

        rect1 = page1.rect
        rect2 = page2.rect

        new_width = rect1.width + rect2.width + margin
        new_height = rect1.height

        new_page = output_pdf.new_page(width=new_width, height=new_height)

        new_page.show_pdf_page(rect1, pdf1, i)
        new_page.show_pdf_page(fitz.Rect(rect1.width + margin, rect1[1], new_width, rect1[3]), pdf2, i)

    output_pdf.save(output_file)

    pdf1.close()
    pdf2.close()
    output_pdf.close()

