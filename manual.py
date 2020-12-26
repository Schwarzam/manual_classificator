# sudo apt-get install python3-tk
# sudo apt-get install python3-pil python3-pil.imagetk

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import pandas as pd
import requests 
from io import BytesIO

requests.packages.urllib3.disable_warnings()

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

DFROW = ''
new_df = ''
dflabel = ''
my_label = ''
splusim = ''
ROWNUM = 0
df = ''
startbutton = ''
loadbutton = ''
labels = ''
output_path = ''
input_path = ''
rownum = ''

class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		container = tk.Frame(self)

		container.grid()

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}


		frame = Frontend(container, self)
		self.frames[Frontend] = frame
		frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(Frontend)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()


class Frontend(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		global ROWNUM
		global df
		global loadbutton
		global startbutton
		global labels
		global output_path
		global rownum
		global input_path

		ROWNUM = 0

		label = tk.Label(self, text="Input CSV catalog path (or GitHub Raw link): ")
		label.grid(row=1, column=0)
		input_path = Entry(master=self)
		input_path.grid(row=1, column=2)


		label = tk.Label(self, text="Output CSV catalog path: ")
		label.grid(row=5, column=0)
		output_path = Entry(master=self)
		output_path.grid(row=5, column=2)

		label = tk.Label(self, text="Start from row number: ")
		label.grid(row=6, column=0)
		rownum = Entry(master=self)
		rownum.grid(row=6, column=2)

		label = tk.Label(self, text="Labels separated by commas")
		label.grid(row=7, column=0)
		labels = Entry(master=self)
		labels.grid(row=7, column=2)

		loadbutton = tk.Button(self, text="Load Catalog", command=lambda:open_csv())
		loadbutton.grid(row=50, column=2, padx=10, pady=10)

		startbutton = tk.Button(self, text="Start", command=lambda:classificate())
		startbutton.grid(row=49, column=2, padx=10, pady=10)

		# button = tk.Button(self, text="Next", command=lambda:self.next())
		# button.grid(row=48, column=2, padx=10, pady=10)

def open_csv():
	global new_df
	global df
	global output_path
	global input_path


	df = pd.read_csv(input_path.get())

	print('Input CSV loaded')

	try:
		new_df = pd.read_csv(output_path.get())
	except:
		new_df = pd.DataFrame(columns= ['ID', 'RA', 'DEC', 'Class'])


def classificate():
	global dflabel
	global my_label
	global splusim
	global DFROW
	global ROWNUM
	global df
	global loadbutton
	global startbutton
	global rownum

	startbutton.destroy()
	loadbutton.destroy()

	ROWNUM = int(rownum.get())

	line = df.iloc[ROWNUM]
	dflabel = tk.Label(text=f"{ROWNUM}")
	dflabel.grid(row=53, column=0, pady=50, padx=40)
	dflabel = tk.Label(text=f"ID: {line['ID']}")
	dflabel.grid(row=8, column=0, pady=50, padx=40)
	dflabel = tk.Label(text=f"RA: {line['RA']}")
	dflabel.grid(row=8, column=1, pady=50, padx=40)
	dflabel = tk.Label(text=f"DEC: {line['DEC']}")
	dflabel.grid(row=8, column=2, pady=50, padx=40)

	try:
		req = requests.get(f"http://splus.cloud/media/jpgsGRI/{line['ID'].split('.')[1]}/{line['ID']}.jpg")
		image = Image.open(BytesIO(req.content))
		image = ImageOps.flip(image)
		my_img = ImageTk.PhotoImage(image)

		splusim = Label(image=my_img)
		splusim.image = my_img
		splusim.grid(row = 10)
	except:
		print('Splus image server down!')

	try:
		req = requests.get(f"https://www.legacysurvey.org/viewer/cutout.jpg?ra={line['RA']}&dec={line['DEC']}&layer=dr8&pixscale=0.2")
		image = Image.open(BytesIO(req.content))
		image = image.resize((200, 200))
		my_img = ImageTk.PhotoImage(image)
		my_label = Label(image=my_img)
		my_label.image = my_img
		my_label.grid(row = 11)
	except:
		print('Legacy image server down!')

	
	DFROW = line
	labels_buttons(line)

	ROWNUM = int(rownum.get()) + 1

def next():
	global dflabel
	global my_label
	global splusim
	global DFROW
	global ROWNUM
	global df

	dflabel.destroy()
	my_label.destroy()
	splusim.destroy()

	line = df.iloc[ROWNUM]
	dflabel = tk.Label(text=f"{ROWNUM}")
	dflabel.grid(row=53, column=0, pady=50, padx=40)
	dflabel = tk.Label(text=f"ID: {line['ID']}")
	dflabel.grid(row=8, column=0, pady=50, padx=40)
	dflabel = tk.Label(text=f"RA: {line['RA']}")
	dflabel.grid(row=8, column=1, pady=50, padx=40)
	dflabel = tk.Label(text=f"DEC: {line['DEC']}")
	dflabel.grid(row=8, column=2, pady=50, padx=40)

	try:
		req = requests.get(f"http://splus.cloud/media/jpgsGRI/{line['ID'].split('.')[1]}/{line['ID']}.jpg")
		image = Image.open(BytesIO(req.content))
		image = ImageOps.flip(image)
		my_img = ImageTk.PhotoImage(image)
		splusim = Label(image=my_img)
		splusim.image = my_img
		splusim.grid(row = 10)
	except:
		print('Splus image server down!')

	try:
		req = requests.get(f"https://www.legacysurvey.org/viewer/cutout.jpg?ra={line['RA']}&dec={line['DEC']}&layer=dr8&pixscale=0.2")
		image = Image.open(BytesIO(req.content))
		image = image.resize((200, 200))
		my_img = ImageTk.PhotoImage(image)

		my_label = Label(image=my_img)
		my_label.image = my_img
		my_label.grid(row = 11)
	except:
		print('Legacy image server down!')

	global DFROW
	DFROW = line
	labels_buttons(line)

	ROWNUM = ROWNUM + 1


def labels_buttons(line):
	global labels

	labs = labels.get()
	labs = labs.split(',')

	row = 14
	column = 0


	for lab in labs:

		com = f"""{lab.strip(' ')} = tk.Button(text=f"{lab.strip(' ')}", command=lambda:[append_label_df("{lab.strip(' ')}"), next()])"""
		com2 = f"""{lab.strip(' ')}.grid(row={row}, column={column}, padx=10, pady=10)"""

		exec(com)
		exec(com2)

		column = column + 1

		

		
def append_label_df(lab):
	global new_df
	global output_path
	global input_path
	global DFROW

	classification = {'ID': [DFROW['ID']], 'RA': [DFROW['RA']], 'DEC': [DFROW['DEC']], 'Class': [str(lab)]}
	part = pd.DataFrame(classification, columns= ['ID', 'RA', 'DEC', 'Class'])

	new_df = new_df.append(part)
	new_df.to_csv(output_path.get(), index=False)


app = App()
app.mainloop()
