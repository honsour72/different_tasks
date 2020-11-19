import os
import win32com.client
import comtypes.client
from win32com import client
import win32api
from PIL import Image
from fpdf import FPDF
import img2pdf
import sys

errors = 0
wrong_files = []

def identifier(file):
	global errors
	global final_folder
	global folder_data
	global wrong_files	
	file_ending = file.split(".")[-1]
	try:
		if (file_ending == "doc"):
			wdFormatPDF = 17
			file_type = "doc"
			word = win32com.client.Dispatch('Word.Application')
			word_doc = word.Documents.Open(folder_data + "\\" + file)
			new_pdf_word = file.replace(file_type, r"pdf")
			word_doc.SaveAs(final_folder + "\\" + new_pdf_word, FileFormat=wdFormatPDF)
			word_doc.Close()

		if (file_ending == "docx"):
			wdFormatPDF = 17
			file_type = "docx"
			word = win32com.client.Dispatch('Word.Application')
			word_doc = word.Documents.Open(folder_data + "\\" + file)
			new_pdf_word = file.replace(file_type, r"pdf")
			word_doc.SaveAs(final_folder + "\\" + new_pdf_word, FileFormat=wdFormatPDF)
			word_doc.Close()

		if (file_ending == "xls"):
			file_type = 'xls'
			excel = client.DispatchEx("Excel.Application")
			new_pdf_excel = file.replace(file_type, r"pdf")
			excel_doc = excel.Workbooks.Open(folder_data + "\\" + file)
			excel_doc.SaveAs(final_folder + "\\" + new_pdf_excel, FileFormat=57)
			excel_doc.Close()

		if (file_ending == "xlsx"):
			file_type = 'xlsx'
			excel = client.DispatchEx("Excel.Application")
			new_pdf_excel = file.replace(file_type, r"pdf")
			excel_doc = excel.Workbooks.Open(folder_data + "\\" + file)
			excel_doc.SaveAs(final_folder  + "\\" + new_pdf_excel, FileFormat=57)
			excel_doc.Close()

		if file_ending == "html":
			wdFormatPDF = 17
			file_type = "html"
			html = win32com.client.Dispatch('Word.Application')
			new_pdf_html = file.replace(file_type, r"pdf")
			html_doc = html.Documents.Open(folder_data + "\\" + file)
			html_doc.SaveAs(final_folder + "\\" + new_pdf_html, FileFormat=wdFormatPDF)
			html_doc.Close()

		if file_ending == "bmp":
			file_type = "bmp"
			img = Image.open(folder_data + "\\" + file)
			new_pdf_bmp = file.replace(file_type, r"pdf")
			new_img = img.resize((800, 800))
			new_img.save(final_folder + "\\" + new_pdf_bmp)

		if (file_ending == "jpg"):
			pdf = FPDF()
			pdf.add_page()
			pdf.set_font('Arial', 'B', 16)
			pdf.image(folder_data + "\\" + file, 3, 3, 204)
			new_pdf_jpg = file[0:-4]
			pdf.output(final_folder + "\\" + new_pdf_jpg + ".pdf", 'F')

		if (file_ending == "jpeg"):
			pdf = FPDF()
			pdf.add_page()
			pdf.set_font('Arial', 'B', 16)
			pdf.image(folder_data + "\\" + file, 3, 3, 204)
			new_pdf_jpg = file[0:-4]
			pdf.output(final_folder + "\\" + new_pdf_jpg + ".pdf", 'F')

		if file_ending == "csv":
			file_type = "csv"
			new_pdf_csv = file.replace(file_type, r"pdf")
			f = open(final_folder + "\\" + new_pdf_csv, "w")
			f.close()


	except:
		wrong_files.append(file)
		errors += 1
		return ("The file you tried to convert is beaten or consists of bad bytes")

folder = input("getting files from folder:")
fin_folder = input("Create folder for converted files:")

address = sys.argv[0][:-16] # c:\Users\Михаил\Desktop\Python\Marina\task_11\  -- без названия скрипта адрес
folder_data = address + folder
print("Files founded:", len(os.listdir(folder_data))-2)

os.mkdir(folder_data + "\\" + fin_folder)
final_folder = folder_data + "\\" + fin_folder # c:\Users\Михаил\Desktop\Python\Marina\task_11\Исходники\\ + fin_folder

list_of_formats = ["doc", "docx", "html", "xls", "xlsx", "bmp", "jpg", "jpeg", "csv"]

for file in os.listdir(folder_data):
	file_ending = file.split(".")[-1]
	if file == fin_folder: continue 
	elif not (file_ending in list_of_formats):
		print("Unsupported file type:", file)
	identifier(file)

for el in range(len(wrong_files)):
	print("Unconverted file:", wrong_files[el])

print("Amount of errors",errors)