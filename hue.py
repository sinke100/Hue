import os
import numpy as np
import PIL.Image as im
from io import BytesIO as by
import PySimpleGUI as sg
class Window:
	def __init__(self, filelist):
		self.filelist = [i for i in filelist if i[-3:] in 'jpg png bmp PNG'.split(' ')]
		self.image = b''
		self.image_display = b''
		self.name = ''
		self.number = 1
		self.grey = False
		self.info = 0
		
	def layout(self, x):
		column = [[sg.Listbox(self.filelist, size=(50, 25),font='Courier` 15', change_submits=True, key='-list-'), sg.Image(key='display')]]
		layout1 = [[sg.Column(column)], [sg.Text('Red', font='Courier` 15'), sg.Input(size=(3, 1), key='red', font='Courier` 15'), sg.Text('Green', font='Courier` 15'), sg.Input(size=(3, 1), key='green', font='Courier` 15'), sg.Text('Blue', font='Courier` 15'), sg.Input(size=(3, 1), key='blue', font='Courier` 15')], [sg.Button('    ', font=('Arial'), key='grey'), sg.Text('Grayscale', font='Courier` 15')], [sg.Button('Transform', font='Courier` 15')]]
		layout2 = [[sg.Image(self.image_display)], [sg.Button('Save', font='Courier` 15'), sg.Button('Again', font='Courier` 15')], [sg.Text(key='info', font='Courier` 15')]]
		return vars()[f'layout{x}']
	
	def start(self):
		if self.number == 1: sg.theme('Topanga')
		else: sg.theme('Black')
		win = sg.Window(self.name, self.layout(self.number))
		grey = False
		numbers = [str(i) for i in range(256)]
		while True:
			e, v = win.read()
			if e == None:
				win.close()
				return e
			if e == '-list-':
				img = im.open(v['-list-'][0], 'r')
				thumb = self.picture(img)
				win['display'].update(thumb)
			if e == 'grey':
				if grey == False:
					win['grey'].update('🌑')            
					grey = not(grey)
				else:
					win['grey'].update('    ')
					grey = not(grey)
			if e == 'Transform':
				red, green, blue = v['red'], v['green'], v['blue'] 
				if red not in numbers or green not in numbers or blue not in numbers: continue
				else:
					red, green, blue = int(red), int(green), int(blue)
					self.grey = grey
					try:
						file = v['-list-'][0]
					except IndexError: continue 

					if self.grey == True:
						img = img.convert('LA')
					w, h, = img.size 
					img_list = list(img.getdata())
					img = self.transform(img_list, red, green, blue, img.mode)
					mode, kanali = 'RGBA', 4
					img_list = np.array(img)
					img_list = img_list.reshape((h,w, kanali))
					result = im.fromarray(img_list.astype('uint8'), mode)
					result_display = self.picture(result, 'big')
					with by() as output:
						result_display.save(output, 'PNG')
						data = output.getvalue()
					self.image_display = data
					with by() as output:
						result.save(output, 'PNG')
						data = output.getvalue()
					self.image = data
					if self.grey:
						self.info = f'{file[:-4]}_({red},{green},{blue})_greyscale.png'
					else:
						self.info = f'{file[:-4]}_({red},{green},{blue}).png'
					win.close()
					return e
			if e == 'Save':
				dest = os.path.abspath(".")+'/transform/'+self.info
				os.makedirs(os.path.dirname(dest), exist_ok=True)
				with open(dest, 'wb') as f: f.write(self.image)
				win['info'].update(self.info)
			if e == 'Again':
				win.close()
				return e
			
	def picture(self, pic, x='small'):
		w, h = pic.size
		while w*h > 500000:
			w*=0.9
			h*=0.9
			w,h = int(w),int(h)
		pic = pic.resize((w,h))
		if x == 'big':
			return pic
		else:
			pic = pic.resize((w//2,h//2))
			with by() as output:
				pic.save(output,'PNG')
				pic = output.getvalue()
			return pic
		
	def transform(self, pic, r, g, b, mode):
		r, g, b = r/255, g/255, b/255
		if mode == 'RGB': image = [(i[0]*r, i[1]*g,i[2]*b,255) for i in pic]
		elif mode == 'RGBA': image = [(i[0]*r, i[1]*g,i[2]*b,i[3]) for i in pic]
		else: image = [(i[0]*r, i[0]*g,i[0]*b,i[1]) for i in pic]
		return image
	
	def run(self):
		window = True
		while window:
			if window == 'Again': self.number = 1
			elif window == 'Transform': self.number = 2
			window = self.start()

if __name__ == '__main__':
    files = os.listdir()
    main = Window(files)
    main.run()
