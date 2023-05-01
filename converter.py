from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io


def pdf_to_text(input_file, output):
    i_f = open(input_file, 'rb')
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr, retData, laparams=LAParams())
    interpreter = PDFPageInterpreter(resMgr, TxtConverter)
    for page in PDFPage.get_pages(i_f):
        interpreter.process_page(page)

    txt = retData.getvalue()
    print(txt)
    with open(output, 'w') as of:
        of.write(txt)


input_pdf = 'registry_cures.pdf'
output_txt = 'sample.txt'
pdf_to_text(input_pdf, output_txt)