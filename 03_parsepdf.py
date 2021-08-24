# from https://towardsdatascience.com/extracting-text-from-scanned-pdf-using-pytesseract-open-cv-cd670ee38052
from pdf2image import convert_from_path

pdfs = r"MN25 2016 Form 7.pdf"
pages = convert_from_path(pdfs, 350)

i = 1
for i, page in enumerate(pages):
    if i >= 1:
        break
    image_name = "Page_" + str(i) + ".jpg"  
    page.save(image_name, "JPEG")


