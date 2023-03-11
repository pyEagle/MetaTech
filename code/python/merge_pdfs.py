# -*- coding:utf-8 -*-

from PyPDF2 import PdfReader, PdfWriter


pdf1 = ''
pdf2 = ''
merge_pdf = ''

pdf_file = PdfWriter()
pdf_file.append(PdfReader(pdf1))
pdf_file.append(PdfReader(pdf2))
pdf_file.write(merge_pdf)
