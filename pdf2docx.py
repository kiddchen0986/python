from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
# from reportlab import *
# from reportlab.lib.utils import cm
from PyPDF2 import PdfFileWriter, PdfFileReader


def create_watermark(content):
    file_path = r"E:\WorkSpace\Python\test\file\mark.pdf"
    c = canvas.Canvas(file_path, pagesize=(30*cm, 30*cm))
    c.translate(0*cm, 0*cm)
    c.setFontSize(90)
    c.rotate(40)
    c.setFillColorRGB(float(237/255), float(18/255), float(84/255), 0.1)
    c.drawString(9*cm, 5*cm, content)
    c.setFillAlpha(0.9)
    c.save()
    return file_path


def add_watermark(pdf_file_in, pdf_file_out, pdf_file_mark):
    pdf_out = PdfFileWriter()
    input_stream = open(pdf_file_in, "rb")
    pdf_in = PdfFileReader(input_stream, strict=False)

    # 获取pdf的页数
    pageNum = pdf_in.getNumPages()

    # 获取有水印的PDF
    pdf_mark = PdfFileReader(open(pdf_file_mark, "rb"), strict=False)
    for i in range(pageNum):
        page = pdf_in.getPage(i)
        page.mergePage(pdf_mark.getPage(0))
        page.compressContentStreams()
        pdf_out.addPage(page)
    pdf_out.write(open(pdf_file_out, "wb"))


if __name__ == "__main__":
    pdf_file_in = r"E:\WorkSpace\Python\test\file\OTP Memory Layout Specification_(Doc-3732).pdf"
    pdf_file_out = r"E:\WorkSpace\Python\test\file\marked.pdf"
    pdf_file_mark = create_watermark("FPC Internal")
    add_watermark(pdf_file_in, pdf_file_out, pdf_file_mark)
