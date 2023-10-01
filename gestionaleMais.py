import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from tkinter.messagebox import showerror, showwarning, showinfo

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring

import csv

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import datetime


class InsertLoad(tk.Toplevel):
	
	def get_save_data(self):
		tk.Toplevel.cognome = self.var.get()
		tk.Toplevel.tmpVerde = self.verdeEntry.get()
		tk.Toplevel.tmpUmidita = self.umid.get()
		tk.Toplevel.tmp14 = self.ess.get()
		tk.Toplevel.tmpSecco = self.seccoEntry.get()
		tk.Toplevel.tmpCosto = self.costoEntry.get()
		app.salva_lavoro()
		app.init_lavori()
		showinfo(title='Conferma',message='Salvataggio effettuato correttamente.',parent=self)
		self.destroy()
	
	def calc_secco(self):
		self.seccoEntry.delete(0,tk.END)
		tmpUmidita = eval(self.umid.get())
		tmpVerde = eval(self.verdeEntry.get())
		for i in range (0, len (self.tmpCoefficienti)):
			if self.tmpCoefficienti[i][0]==tmpUmidita:
				if self.prcEss == 13:
					self.tmpSecco = tmpVerde*self.tmpCoefficienti[i][1]
				else:
					self.tmpSecco = tmpVerde*self.tmpCoefficienti[i][2]
				break
		self.seccoEntry.insert(0,self.tmpSecco)
	
	def essicazione_changed (self):
		if (self.ess.get()=='1'):
			self.prcEss = 14
		else:
			self.prcEss = 13
	
	def __init__(self, parent):
		super().__init__(parent)
		self.title('Gestisci clienti')
		self.geometry("730x250")
		mainframe = ttk.Frame(self, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		
		self.tmpCoefficienti = parent.coefficienti
		
		self.prcEss = 13
		
		self.tmpSecco=0

		self.labelStyle = font.Font(family='Helvetica', size=16, weight=font.BOLD)
		
		self.aziendaLabel=tk.Label(mainframe, text="Azienda", font=self.labelStyle)
		self.aziendaLabel.grid(column=2, row=1, sticky=tk.W)
		
		self.var = tk.StringVar()
		self.combobox=ttk.Combobox(mainframe, textvariable = self.var)
		self.combobox['state'] = 'normal'
		self.combobox.grid(column=4, row=1, sticky=tk.W)
		self.combo_list = []
		self.tmpAnag = parent.anagrafiche
		for i in range (0, len (self.tmpAnag)):
			self.combo_list.append(self.tmpAnag[i]['cognome'])
		self.combobox['values']=(self.combo_list)
		self.combobox.current()
		
		self.verdeLabel=tk.Label(mainframe, text="Verde (q)", font=self.labelStyle)
		self.verdeLabel.grid(column=2, row=2, sticky=tk.W)
		self.verdeEntry = tk.Entry(mainframe, font=self.labelStyle)	
		self.verdeEntry.grid(column=4, row=2, sticky=tk.W)
		
		self.mainButtonStyle = font.Font(family='Helvetica', size=24, weight=font.BOLD)
		
		self.umiditaLabel=tk.Label(mainframe, text="Umidità", font=self.labelStyle)
		self.umiditaLabel.grid(column=2, row=3, sticky=tk.W)
		
		self.umid = tk.StringVar()
		self.umiditaBox=ttk.Combobox(mainframe, textvariable = self.umid)
		self.umiditaBox['state'] = 'normal'
		self.umiditaBox.grid(column=4, row=3, sticky=tk.W)
		self.umidList = []
		self.tmpCoeff = parent.coefficienti
		for i in range (0, len (self.tmpCoeff)):
			self.umidList.append(self.tmpCoeff[i][0])
		self.umiditaBox['values']=(self.umidList)
		self.umiditaBox.current()
		
		self.ess = tk.StringVar()
		self.checkEss=ttk.Checkbutton(mainframe, text='14%', command=self.essicazione_changed, variable=self.ess, onvalue='1', offvalue='0')
		self.checkEss.grid(column=5, row=3, sticky=tk.W)
        		
		self.calcolaButton=tk.Button(mainframe, text="CALCOLA", font=self.mainButtonStyle, command=self.calc_secco, bg='#ff00ff', fg='#ffffff')
		self.calcolaButton.grid(column=5, row=4, sticky=tk.W)
		
		self.seccoLabel=tk.Label(mainframe, text="Secco", font=self.labelStyle)
		self.seccoLabel.grid(column=2, row=4, sticky=tk.W)
		self.seccoEntry = tk.Entry(mainframe,font=self.labelStyle)
		self.seccoEntry.grid(column=4, row=4, sticky=tk.W)
		
		self.costoLabel=tk.Label(mainframe, text="Costo(euro)", font=self.labelStyle)
		self.costoLabel.grid(column=2, row=5, sticky=tk.W)
		self.costoEntry = tk.Entry(mainframe,font=self.labelStyle)
		self.costoEntry.grid(column=4, row=5, sticky=tk.W)
		
		self.confermaButton=tk.Button(mainframe, text="CONFERMA", font=self.mainButtonStyle, command=self.get_save_data, bg='#00ff00', fg='#ffffff')
		self.confermaButton.grid(column=2, row=8, sticky=tk.W)	
		
		self.annullaButton=tk.Button(mainframe, text="ANNULLA", font=self.mainButtonStyle, command=self.destroy, bg='#ff0000', fg='#ffffff')
		self.annullaButton.grid(column=4, row=8, sticky=tk.W)
			
		#self.mainloop()

class InsertCustomer(tk.Toplevel):
	
	def get_save_data(self):
		tk.Toplevel.cognome = self.cognomeEntry.get()
		tk.Toplevel.nome = self.nomeEntry.get()
		tk.Toplevel.telefono = self.telefonoEntry.get()			
		if tk.Toplevel.cognome != "":
			app.salva_anagrafica()
			app.init_anagrafiche()
		showinfo(title='Conferma',message='Salvataggio effettuato correttamente.',parent=self)
		self.destroy()
	
	def __init__(self, parent):
		super().__init__(parent)
		self.title('Inserisci nuovo cliente')
		self.geometry("600x200")
		mainframe = ttk.Frame(self, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.labelStyle = font.Font(family='Helvetica', size=16, weight=font.BOLD)
		tk.Label(mainframe, text="Cognome / Ragione Sociale", font=self.labelStyle).grid(column=2, row=1, sticky=tk.W)
		self.cognomeEntry = tk.Entry(mainframe,font=self.labelStyle)
		self.cognomeEntry.grid(column=3, row=1, sticky=tk.W)
		tk.Label(mainframe, text="Nome", font=self.labelStyle).grid(column=2, row=2, sticky=tk.W)
		self.nomeEntry = tk.Entry(mainframe,font=self.labelStyle)
		self.nomeEntry.grid(column=3, row=2, sticky=tk.W)		
		tk.Label(mainframe, text="Telefono", font=self.labelStyle).grid(column=2, row=3, sticky=tk.W)
		self.telefonoEntry = tk.Entry(mainframe,font=self.labelStyle)
		self.telefonoEntry.grid(column=3, row=3, sticky=tk.W)
		self.mainButtonStyle = font.Font(family='Helvetica', size=24, weight=font.BOLD)
		self.confermaButton=tk.Button(mainframe, text="CONFERMA", font=self.mainButtonStyle, command=self.get_save_data, bg='#00ff00', fg='#ffffff')
		self.confermaButton.grid(column=2, row=8, sticky=tk.W)	
		self.annullaButton=tk.Button(mainframe, text="ANNULLA", font=self.mainButtonStyle, command=self.destroy, bg='#ff0000', fg='#ffffff')
		self.annullaButton.grid(column=3, row=8, sticky=tk.W)
		
		for child in mainframe.winfo_children(): 
			child.grid_configure(padx=5, pady=5)
		
		#self.mainloop()


class ManageLoad(tk.Toplevel):

	def set_load_entries(self, parent):
		self.umidita_box['values']=[]
		self.umidita_box.current()
		self.verde_entry.delete(0, tk.END)
		self.secco_entry.delete(0, tk.END)
		self.costo_entry.delete(0, tk.END)
		self.ess.set(0)

		self.combo_load.set('')
		vuota = []
		self.combo_list = []
		self.combo_load['values']=vuota
		self.combo_load.current()
		for i in range (0, len (self.tmp_load)):
			if self.tmp_load[i]['cognome']==self.anag_sel.get():
				stringa = self.tmp_load[i]['verde']+"-"+self.tmp_load[i]['secco']+"-"+self.tmp_load[i]['costo']
				self.combo_list.append(stringa)
				self.combo_load['values']=(self.combo_list)
		self.combo_load.current()

	def set_load_detail(self, parent):
		self.umidita_box['values']=[]
		self.umidita_box.current()
		self.verde_entry.delete(0, tk.END)
		self.secco_entry.delete(0, tk.END)
		self.costo_entry.delete(0, tk.END)
		self.ess.set(0)
		dettagli = []
		dettagli = self.combo_load.get().split("-")
		for i in range (0, len (self.tmp_load)):
			if (self.tmp_load[i]['cognome']==self.anag_sel.get()) and (self.tmp_load[i]['verde']==dettagli[0]) and (self.tmp_load[i]['secco']==dettagli[1]) and (self.tmp_load[i]['costo']==dettagli[2]):
				tmp_verde_entry=self.tmp_load[i]['verde']
				tmp_secco_entry=self.tmp_load[i]['secco']
				tmp_costo_entry=self.tmp_load[i]['costo']
				tmp_umidita = self.tmp_load[i]['umidita']
				tmp_14 = self.tmp_load[i]['prc14']
				
				self.verde_entry.insert(0,tmp_verde_entry)
				self.secco_entry.insert(0,tmp_secco_entry)
				self.costo_entry.insert(0,tmp_costo_entry)
				self.umidita_box.set(tmp_umidita)
				if tmp_14=='1':
					self.ess.set(1)
				else:
					self.ess.set(0)
				break
		self.umidita_box['values']= (self.umid_list)

	def delete_load (self):
		tk.Toplevel.cognome = self.anag_sel.get()
		tk.Toplevel.verde = self.verde_entry.get()
		tk.Toplevel.secco = self.secco_entry.get()
		tk.Toplevel.costo = self.costo_entry.get()
		tk.Toplevel.umidita = self.umid.get()
		app.elimina_carico()
		app.init_lavori()	
		showinfo(title='Conferma',message='Eliminazione effettuata correttamente.',parent=self)
		self.destroy()

	def calc_secco(self):
		self.secco_entry.delete(0,tk.END)
		tmp_umidita = eval(self.umid.get())
		tmp_verde = eval(self.verde_entry.get())
		for i in range (0, len (self.tmp_coefficienti)):
			if self.tmp_coefficienti[i][0]==tmp_umidita:
				if self.ess.get() == '0':
					self.tmp_secco = tmp_verde*self.tmp_coefficienti[i][1]
				else:
					self.tmp_secco = tmp_verde*self.tmp_coefficienti[i][2]
				break
		self.secco_entry.insert(0,self.tmp_secco)

	def modify_load (self):
		tk.Toplevel.dettagli = self.combo_load.get().split("-")
		tk.Toplevel.cognome=self.anag_sel.get()
		tk.Toplevel.verde = self.verde_entry.get()
		tk.Toplevel.secco = self.secco_entry.get()
		tk.Toplevel.costo = self.costo_entry.get()
		tk.Toplevel.umidita = self.umid.get()
		tk.Toplevel.tmp14 = self.ess.get()
		app.modifica_lavoro()
		app.init_lavori()
		showinfo(title='Conferma',message='Modifica effettuata correttamente.',parent=self)
		self.destroy()
		
	def essicazione_changed (self):
		if (self.ess.get()=='1'):
			self.prcEss = 14
		else:
			self.prcEss = 13

	def __init__(self, parent):
		super().__init__(parent)
		self.title('Gestisci carichi')
		self.geometry("750x400")
		mainframe = ttk.Frame(self, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		
		self.label_style = font.Font(family='Helvetica', size=16, weight=font.BOLD)
			
		self.azienda_label=tk.Label(mainframe, text="Azienda", font=self.label_style)
		self.azienda_label.grid(column=2, row=1, sticky=tk.W)
		
		self.anag_sel = tk.StringVar()
		self.combo_anag=ttk.Combobox(mainframe, textvariable = self.anag_sel)
		self.combo_anag['state'] = 'normal'
		self.combo_anag.grid(column=4, row=1, sticky=tk.W)
		self.combo_anag_list = []
		self.tmp_anag = parent.anagrafiche
		for i in range (0, len (self.tmp_anag)):
			self.combo_anag_list.append(self.tmp_anag[i]['cognome'])
		self.combo_anag['values']=(self.combo_anag_list)
		self.combo_anag.current()
		
		self.load_label=tk.Label(mainframe, text="Carico", font=self.label_style)
		self.load_label.grid(column=2, row=2, sticky=tk.W)
		
		self.load_sel = tk.StringVar()
		self.combo_load=ttk.Combobox(mainframe, textvariable = self.load_sel)
		self.combo_load['state'] = 'normal'
		self.combo_load.grid(column=4, row=2, sticky=tk.W)
		self.tmp_load = parent.lavori
			
		self.combo_anag.bind("<<ComboboxSelected>>", self.set_load_entries)
		self.combo_load.bind("<<ComboboxSelected>>", self.set_load_detail)
		
		self.verde_label=tk.Label(mainframe, text="Verde", font=self.label_style)
		self.verde_label.grid(column=2, row=3, sticky=tk.W)
		self.verde_entry = tk.Entry(mainframe, font=self.label_style)	
		self.verde_entry.grid(column=4, row=3, sticky=tk.W)

		self.umidita_label=tk.Label(mainframe, text="Umidità", font=self.label_style)
		self.umidita_label.grid(column=2, row=4, sticky=tk.W)
		
		self.tmp_coefficienti = parent.coefficienti
		self.umid = tk.StringVar()
		self.umidita_box=ttk.Combobox(mainframe, textvariable = self.umid)
		self.umidita_box['state'] = 'normal'
		self.umidita_box.grid(column=4, row=4, sticky=tk.W)
		self.umid_list = []
		self.tmp_coeff = parent.coefficienti
		for i in range (0, len (self.tmp_coeff)):
			self.umid_list.append(self.tmp_coeff[i][0])
		self.umidita_box['values']=(self.umid_list)
		self.umidita_box.current()
		
		self.ess = tk.StringVar()
		self.check_ess=ttk.Checkbutton(mainframe, text='14%', command=self.essicazione_changed, variable=self.ess, onvalue='1', offvalue='0')
		self.check_ess.grid(column=5, row=3, sticky=tk.W)
		
		self.main_button_style = font.Font(family='Helvetica', size=24, weight=font.BOLD)		
		self.calcolaButton=tk.Button(mainframe, text="CALCOLA", font=self.main_button_style, command=self.calc_secco, bg='#ff00ff', fg='#ffffff')
		self.calcolaButton.grid(column=5, row=4, sticky=tk.W)

		self.secco_label=tk.Label(mainframe, text="Secco", font=self.label_style)
		self.secco_label.grid(column=2, row=5, sticky=tk.W)
		self.secco_entry = tk.Entry(mainframe,font=self.label_style)
		self.secco_entry.grid(column=4, row=5, sticky=tk.W)
		
		self.costo_label=tk.Label(mainframe, text="Costo", font=self.label_style)
		self.costo_label.grid(column=2, row=6, sticky=tk.W)
		self.costo_entry = tk.Entry(mainframe,font=self.label_style)
		self.costo_entry.grid(column=4, row=6, sticky=tk.W)		
				
		self.annulla_button=tk.Button(mainframe, text="ANNULLA", font=self.main_button_style, command=self.destroy, bg='#0000ff', fg='#ffffff')
		self.annulla_button.grid(column=2, row=8, sticky=tk.W)
		self.eliminaButton=tk.Button(mainframe, text="ELIMINA", font=self.main_button_style, command=self.delete_load, bg='#ff0000', fg='#ffffff')
		self.eliminaButton.grid(column=4, row=8, sticky=tk.W)
		self.modificaButton=tk.Button(mainframe, text="MODIFICA", font=self.main_button_style, command=self.modify_load, bg='#00ff00', fg='#ffffff')
		self.modificaButton.grid(column=5, row=8, sticky=tk.W)
		
		for child in mainframe.winfo_children(): 
			child.grid_configure(padx=5, pady=5)


class PrintLoad (tk.Toplevel):
	
	def sistema(self,stringa):
		stringa=stringa.replace(",",".")
		stringa=eval(stringa)
		stringa=round(stringa,2)
		stringa=str(stringa)
		stringa=stringa.replace(".",",")
		return stringa
		
	def print_load(self):
		tmp_cognome = self.var.get()
		dir = "stampe/"
		path = dir + tmp_cognome + "- carichi.pdf"
		
		c = canvas.Canvas(path, pagesize=A4)
		c.save()
		
		c = canvas.Canvas(path, pagesize=A4)  # alternatively use bottomup=False
		
		width, height = A4
		styles = getSampleStyleSheet()
		
		stile_t = ParagraphStyle(name='Heading2', fontName='Helvetica-Bold', fontSize=18,)
		title = "Calcolo Secco"
		t1 = Paragraph(title, style=stile_t)
		t1.wrapOn(c, 80*mm, 50*mm)
		t1.drawOn(c, 110*mm, 290*mm)
		
		stile_c1 = ParagraphStyle(name='Heading2', fontName='Helvetica', fontSize=13,)
		ctext1 = "Azienda:"
		c1 = Paragraph(ctext1, style=stile_c1)
		c1.wrapOn(c, 80*mm, 50*mm)
		c1.drawOn(c, 100*mm, 275*mm)
		stile_c2 = ParagraphStyle(name='Heading2', fontName='Helvetica-Bold', fontSize=13,)
		ctext2 = tmp_cognome.upper()
		c2 = Paragraph(ctext2, style=stile_c2)
		c2.wrapOn(c, 80*mm, 50*mm)
		c2.drawOn(c, 130*mm, 275*mm)
		
		
		ptext1 = "ABC snc" 
		ptext2 = "di DEF C."
		ptext3 = "46100 Mantova (MN)"
		ptext4 = "Via Roma 1 Tel/Fax 0376 12345"
		ptext5 = "P.IVA e CF 00001111111"
		stile_h = ParagraphStyle(name='Normal', fontName='Helvetica-Bold', fontSize=12,)

		p1 = Paragraph(ptext1, style=stile_h)
		p2 = Paragraph(ptext2, style=stile_h)
		p3 = Paragraph(ptext3, style=stile_h)
		p4 = Paragraph(ptext4, style=stile_h)
		p5 = Paragraph(ptext5, style=stile_h)
		p1.wrapOn(c, 80*mm, 50*mm)  # size of 'textbox' for linebreaks etc.
		p1.drawOn(c, 10*mm, 275*mm)    # position of text / where to draw
		p2.wrapOn(c, 80*mm, 50*mm)  # size of 'textbox' for linebreaks etc.
		p2.drawOn(c, 10*mm, 270*mm)    # position of text / where to draw
		p3.wrapOn(c, 80*mm, 50*mm)  # size of 'textbox' for linebreaks etc.
		p3.drawOn(c, 10*mm, 265*mm)    # position of text / where to draw
		p4.wrapOn(c, 80*mm, 50*mm)  # size of 'textbox' for linebreaks etc.
		p4.drawOn(c, 10*mm, 260*mm)    # position of text / where to draw
		p5.wrapOn(c, 80*mm, 50*mm)  # size of 'textbox' for linebreaks etc.
		p5.drawOn(c, 10*mm, 255*mm)    # position of text / where to draw
		
		c.setLineWidth(3)
		c.line(10*mm,250*mm,width-10*mm,250*mm)
		
		data = []
		col_title = ["Verde (Q)", "Umidità (%)", "Secco (Q)", "Costo TOT", "Costo al Q."]
		data.append(col_title)
		tot_verde=0
		tot_secco=0
		tot_costo=0
		righe_stampate = 0
		for i in range (0, len (self.tmp_lavori)):
			tmp = []
			if self.tmp_lavori[i]['cognome']==tmp_cognome:
				righe_stampate = righe_stampate+1
				tmp.append(self.sistema(self.tmp_lavori[i]['verde']))
				tmp.append(self.sistema(self.tmp_lavori[i]['umidita']))
				tmp.append(self.sistema(self.tmp_lavori[i]['secco']))
				tmp.append( round( eval(self.tmp_lavori[i]['costo'].replace(",","."))*eval(self.tmp_lavori[i]['verde'].replace(",",".")) ,2 ) )
				tmp.append(self.sistema(self.tmp_lavori[i]['costo']))
				tot_verde = tot_verde+eval(self.tmp_lavori[i]['verde'].replace(",","."))
				tot_secco = tot_secco+eval(self.tmp_lavori[i]['secco'].replace(",","."))
				tot_costo = tot_costo+eval(self.tmp_lavori[i]['costo'].replace(",","."))*eval(self.tmp_lavori[i]['verde'].replace(",","."))
				data.append(tmp)
		
		tot_verde=self.sistema(str(tot_verde))
		tot_secco=self.sistema(str(tot_secco))
		# il costo è il costo al quintale per il verde
		tot_costo=self.sistema(str(tot_costo))
		col_vuota = ["","","",""]
		data.append(col_vuota)
		col_fine = [str(tot_verde), "", str(tot_secco), str(tot_costo)]
		data.append(col_fine)
		col_fine_title = ["TOTALE VERDE", "", "TOTALE SECCO", "TOTALE COSTO", ""]
		data.append(col_fine_title)
		
		table = Table(data, colWidths=38*mm)
		table.setStyle(TableStyle([('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,0), 14), ('ALIGN',(0,0), (-1,0),'CENTER'), ('FONTNAME', (0,1), (-1,-3), 'Helvetica'), ('FONTSIZE', (0,1), (-1,-3), 13), ('FONTNAME', (0,-2), (-1,-1), 'Helvetica-Bold'), ('FONTSIZE', (0,-2), (-1,-1), 11) , ('LINEABOVE',(0,-2),(-1,-2),1,colors.black), ('ALIGN',(0,-2),(-1,-2),'CENTER') ]))
		table.wrapOn(c, width, height)
		w, h = table.wrap(0, 0)
		table.drawOn(c, 10*mm, 690-h)

		showinfo(title='Conferma',message='Documento prodotto correttamente.',parent=self)
				
		c.save()
	
	def __init__(self, parent):
		super().__init__(parent)
		self.title('Stampa lavori')
		self.geometry("500x150")
		mainframe = ttk.Frame(self, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.tmp_lavori = parent.lavori
		self.label_style = font.Font(family='Helvetica', size=16, weight=font.BOLD)
			
		self.azienda_label=tk.Label(mainframe, text="Azienda", font=self.label_style)
		self.azienda_label.grid(column=2, row=1, sticky=tk.W)
		
		self.var = tk.StringVar()
		self.combobox=ttk.Combobox(mainframe, textvariable = self.var)
		self.combobox['state'] = 'normal'
		self.combobox.grid(column=4, row=1, sticky=tk.W)
		self.combo_list = []
		self.tmp_anag = parent.anagrafiche
		for i in range (0, len (self.tmp_anag)):
			self.combo_list.append(self.tmp_anag[i]['cognome'])
		self.combobox['values']=(self.combo_list)
		self.combobox.current()
		
		self.main_button_style = font.Font(family='Helvetica', size=24, weight=font.BOLD)		
		self.annulla_button=tk.Button(mainframe, text="ANNULLA", font=self.main_button_style, command=self.destroy, bg='#0000ff', fg='#ffffff')
		self.annulla_button.grid(column=2, row=3, sticky=tk.W)
		self.print_button=tk.Button(mainframe, text="STAMPA LAVORI", font=self.main_button_style, command=self.print_load, height=1, width=15, bg='#ff00ff', fg='#ffffff')
		self.print_button.grid(column=4, row=3, sticky=tk.W)

		for child in mainframe.winfo_children(): 
			child.grid_configure(padx=5, pady=5)

class ManageCustomer(tk.Toplevel):
	
	def deleteAnag(self):
		tk.Toplevel.cognome = self.cognomeEntry.get()
		tk.Toplevel.nome = self.nomeEntry.get()
		app.elimina_anagrafica()
		app.init_anagrafiche()	
		showinfo(title='Conferma',message='Eliminazione effettuato correttamente.',parent=self)
		self.destroy()

	def modifyAnag(self):
		tk.Toplevel.cognome=self.var.get()
		tk.Toplevel.tmpcognome = self.cognomeEntry.get()
		tk.Toplevel.tmpnome = self.nomeEntry.get()
		tk.Toplevel.tmptelefono = self.telEntry.get()
		app.modifica_anagrafica()
		app.init_anagrafiche()	
		showinfo(title='Conferma',message='Modifica effettuata correttamente.',parent=self)
		self.destroy()
	
	def setEntries(self, parent):
		self.cognomeEntry.delete(0, tk.END)
		self.nomeEntry.delete(0, tk.END)
		self.telEntry.delete(0, tk.END)
		
		self.cognomeEntry.insert(0,self.var.get())
		for i in range (0, len (self.tmpAnag)):
			if(self.tmpAnag[i]['cognome']==self.var.get()):
				tmpNomeEntry=self.tmpAnag[i]['nome']
				tmpTelEntry=self.tmpAnag[i]['telefono']
				break
		self.nomeEntry.insert(0,tmpNomeEntry)
		self.telEntry.insert(0,tmpTelEntry)
		
	
	def __init__(self, parent):
		super().__init__(parent)
		self.title('Gestisci clienti')
		self.geometry("800x250")
		mainframe = ttk.Frame(self, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		
		self.labelStyle = font.Font(family='Helvetica', size=16, weight=font.BOLD)
			
		self.aziendaLabel=tk.Label(mainframe, text="Azienda", font=self.labelStyle)
		self.aziendaLabel.grid(column=2, row=1, sticky=tk.W)
		
		self.var = tk.StringVar()
		self.combobox=ttk.Combobox(mainframe, textvariable = self.var)
		self.combobox['state'] = 'normal'
		self.combobox.grid(column=4, row=1, sticky=tk.W)
		self.combo_list = []
		self.tmpAnag = parent.anagrafiche
		for i in range (0, len (self.tmpAnag)):
			self.combo_list.append(self.tmpAnag[i]['cognome'])
		self.combobox['values']=(self.combo_list)
		self.combobox.current()
		
		self.cognomeLabel=tk.Label(mainframe, text="Cognome / Ragione Sociale", font=self.labelStyle)
		self.cognomeLabel.grid(column=2, row=3, sticky=tk.W)
		self.cognomeEntry = tk.Entry(mainframe, font=self.labelStyle)	
		self.cognomeEntry.grid(column=4, row=3, sticky=tk.W)
		
		self.nomeLabel=tk.Label(mainframe, text="Nome", font=self.labelStyle)
		self.nomeLabel.grid(column=2, row=4, sticky=tk.W)
		self.nomeEntry = tk.Entry(mainframe,font=self.labelStyle)
		self.nomeEntry.grid(column=4, row=4, sticky=tk.W)
		
		self.telLabel=tk.Label(mainframe, text="Telefono", font=self.labelStyle)
		self.telLabel.grid(column=2, row=5, sticky=tk.W)
		self.telEntry = tk.Entry(mainframe,font=self.labelStyle)
		self.telEntry.grid(column=4, row=5, sticky=tk.W)
		
		self.combobox.bind("<<ComboboxSelected>>", self.setEntries)
		

		self.mainButtonStyle = font.Font(family='Helvetica', size=24, weight=font.BOLD)		
		self.annullaButton=tk.Button(mainframe, text="ANNULLA", font=self.mainButtonStyle, command=self.destroy, bg='#0000ff', fg='#ffffff')
		self.annullaButton.grid(column=2, row=8, sticky=tk.W)
		self.eliminaButton=tk.Button(mainframe, text="ELIMINA", font=self.mainButtonStyle, command=self.deleteAnag, bg='#ff0000', fg='#ffffff')
		self.eliminaButton.grid(column=4, row=8, sticky=tk.W)
		self.modificaButton=tk.Button(mainframe, text="MODIFICA", font=self.mainButtonStyle, command=self.modifyAnag, bg='#00ff00', fg='#ffffff')
		self.modificaButton.grid(column=6, row=8, sticky=tk.W)
		
		for child in mainframe.winfo_children(): 
			child.grid_configure(padx=5, pady=5)
				
class GestionaleMais (tk.Tk):
	
	def close(self):
		self.quit()
		
	def salva_anagrafica(self):
		tree = ET.parse(self.anag_filename)
		xmlRoot = ET.parse(self.anag_filename).getroot()	
		child = ET.Element("Anagrafica")
		b = ET.SubElement(child, "Cognome")
		b.text = tk.Toplevel.cognome
		if b.text=="":
			b.text = "-"
		c = ET.SubElement(child, "Nome")
		c.text = tk.Toplevel.nome
		if c.text=="":
			c.text = "-"
		d = ET.SubElement(child, "Telefono")
		d.text = tk.Toplevel.telefono
		if d.text=="":
			d.text = "-"
		xmlRoot.append(child)
		#t = tostring(tree)
		# #print(tostring(xmlRoot, encoding='utf8').decode('utf8'))
		tree = ET.ElementTree(xmlRoot)
		tree.write(self.anag_filename)	

	def salva_lavoro(self):
		tree = ET.parse(self.lavori_filename)
		xmlRoot = ET.parse(self.lavori_filename).getroot()	
		child = ET.Element("Lavoro")
		b = ET.SubElement(child, "Cognome")
		b.text = tk.Toplevel.cognome
		
		c = ET.SubElement(child, "Verde")
		c.text = tk.Toplevel.tmpVerde
		if c.text=="":
			c.text = "0"
		d = ET.SubElement(child, "Umidita")
		d.text = tk.Toplevel.tmpUmidita
		prc14 = ET.SubElement(child, "prc14")
		prc14.text=tk.Toplevel.tmp14
		
		e = ET.SubElement(child, "Secco")
		e.text = tk.Toplevel.tmpSecco
		if e.text=="":
			e.text = "0"		
		f = ET.SubElement(child, "Costo")
		f.text = tk.Toplevel.tmpCosto
		if f.text=="":
			f.text = "0"		
		xmlRoot.append(child)
		#t = tostring(tree)
		#print(tostring(xmlRoot, encoding='utf8').decode('utf8'))
		tree = ET.ElementTree(xmlRoot)
		tree.write(self.lavori_filename)	

	
	
	def modifica_anagrafica(self):
		tree = ET.parse(self.anag_filename)
		xmlRoot = ET.parse(self.anag_filename).getroot()	

		#elimino
		for anagrafica in xmlRoot.findall('Anagrafica'):
			cognome = anagrafica.find('Cognome').text			
			if cognome==tk.Toplevel.cognome:			
				xmlRoot.remove(anagrafica)

		#aggiungo
		child = ET.Element("Anagrafica")
		b = ET.SubElement(child, "Cognome")
		b.text = tk.Toplevel.tmpcognome
		c = ET.SubElement(child, "Nome")
		c.text = tk.Toplevel.tmpnome
		d = ET.SubElement(child, "Telefono")
		d.text = tk.Toplevel.tmptelefono
		xmlRoot.append(child)
		
		tree = ET.ElementTree(xmlRoot)
		tree.write(self.anag_filename)			

	def modifica_lavoro(self):
		tree = ET.parse(self.lavori_filename)
		xmlRoot = ET.parse(self.lavori_filename).getroot()	

		#elimino
		for lavoro in xmlRoot.findall('Lavoro'):
			del_cognome = lavoro.find('Cognome').text
			del_verde = lavoro.find('Verde').text
			del_secco = lavoro.find('Secco').text
			del_costo = lavoro.find('Costo').text
			
			if del_cognome==tk.Toplevel.cognome and eval(del_verde)==eval(tk.Toplevel.dettagli[0]) and eval(del_secco)==eval(tk.Toplevel.dettagli[1]) and eval(del_costo)==eval(tk.Toplevel.dettagli[2]):			
				xmlRoot.remove(lavoro)

		#aggiungo
		child = ET.Element("Lavoro")
		b = ET.SubElement(child, "Cognome")
		b.text = tk.Toplevel.cognome
		
		c = ET.SubElement(child, "Verde")
		c.text = tk.Toplevel.verde
		if c.text=="":
			c.text = "0"
		d = ET.SubElement(child, "Umidita")
		d.text = tk.Toplevel.umidita
		prc14 = ET.SubElement(child, "prc14")
		prc14.text=tk.Toplevel.tmp14
		
		e = ET.SubElement(child, "Secco")
		e.text = tk.Toplevel.secco
		if e.text=="":
			e.text = "0"		
		f = ET.SubElement(child, "Costo")
		f.text = tk.Toplevel.costo
		if f.text=="":
			f.text = "0"		
		xmlRoot.append(child)

		tree = ET.ElementTree(xmlRoot)
		tree.write(self.lavori_filename)			
	
	
	
	def elimina_anagrafica(self):
		tree = ET.parse(self.anag_filename)
		xmlRoot = ET.parse(self.anag_filename).getroot()	
		for anagrafica in xmlRoot.findall('Anagrafica'):
			cognome = anagrafica.find('Cognome').text
			nome = anagrafica.find('Nome').text
			if cognome==tk.Toplevel.cognome and nome==tk.Toplevel.nome:			
				xmlRoot.remove(anagrafica)
		tree = ET.ElementTree(xmlRoot)
		tree.write(self.anag_filename)		
	
	def elimina_carico(self):
		tree = ET.parse(self.lavori_filename)
		xmlRoot = ET.parse(self.lavori_filename).getroot()	
		for lavoro in xmlRoot.findall('Lavoro'):
			cognome = lavoro.find('Cognome').text
			verde = lavoro.find('Verde').text
			secco = lavoro.find('Secco').text
			umidita = lavoro.find('Umidita').text
			if cognome==tk.Toplevel.cognome and verde==tk.Toplevel.verde  and umidita==tk.Toplevel.umidita and secco==tk.Toplevel.secco:			
				xmlRoot.remove(lavoro)
		tree = ET.ElementTree(xmlRoot)
		tree.write(self.lavori_filename)		
	
	def init_anagrafiche(self):
		self.anagrafiche.clear()
		tree = ET.parse(self.anag_filename)
		root = tree.getroot()
		for customer in root.findall('Anagrafica'):
			anag_data = {}
			anag_data['nome']=customer.find('Nome').text
			anag_data['cognome']=customer.find('Cognome').text
			anag_data['telefono'] = customer.find('Telefono').text
			self.anagrafiche.append(anag_data)

	def init_lavori(self):
		self.lavori.clear()
		tree = ET.parse(self.lavori_filename)
		root = tree.getroot()
		for work in root.findall('Lavoro'):
			load_data = {}
			load_data['cognome']=work.find('Cognome').text
			
			load_data['verde']=work.find('Verde').text
			
			if work.find('prc14')==None:
				load_data['prc14']=0
			else:
				load_data['prc14']=work.find('prc14').text
			
			load_data['umidita'] = work.find('Umidita').text
			load_data['secco'] = work.find('Secco').text
			load_data['costo'] = work.find('Costo').text
			self.lavori.append(load_data)

	def init_coefficienti(self):
		with open(self.coeff_filename, newline='') as csvfile:
			csv_reader = csv.reader(csvfile, delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count==0:
					line_count=line_count+1
					continue
				coeff = []
				coeff.append(eval(row[0].replace(",", ".")))
				coeff.append(eval(row[1].replace(",", ".")))
				coeff.append(eval(row[2].replace(",", ".")))
				self.coefficienti.append(coeff)
		
		
	def __init__(self):
		super().__init__()
		
		self.anag_filename = "anagrafica.xml"
		self.lavori_filename = "lavori.xml"
		self.coeff_filename = "secco.csv"
		
		self.anagrafiche = []
		self.init_anagrafiche()
		
		self.lavori = []
		self.init_lavori()
		
		self.coefficienti = []
		self.init_coefficienti()
		
		self.title("Gestionale Mais")
		# da usare sotto Linux
		# self.geometry("330x410")
		# da usare sotto Windows per Vanna
		self.geometry("330x550")
		mainframe = ttk.Frame(self, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		
		self.myFont = font.Font(size=30, family='Helvetica')
		self.mainButtonStyle = font.Font(family='Helvetica', size=24, weight=font.BOLD)

		tk.Button(mainframe, text="CLIENTE", font=self.mainButtonStyle, command=self.open_insert_customer, height=1, width=15, bg='#0000ff', fg='#ffffff').grid(column=1, row=1, sticky=tk.W)
		tk.Button(mainframe, text="GESTISCI CLIENTI", font=self.mainButtonStyle, command=self.open_manage_customer, height=1, width=15, bg='#0000ff', fg='#ffffff').grid(column=1, row=2, sticky=tk.W)
		tk.Button(mainframe, text="CARICO", font=self.mainButtonStyle, command=self.open_insert_load, height=1, width=15, bg='#0000ff', fg='#ffffff').grid(column=1, row=3, sticky=tk.W)
		tk.Button(mainframe, text="GESTISCI CARICHI", font=self.mainButtonStyle, command=self.open_manage_load, height=1, width=15, bg='#0000ff', fg='#ffffff').grid(column=1, row=4, sticky=tk.W)
		tk.Button(mainframe, text="STAMPA CLIENTI", font=self.mainButtonStyle, command=self.print_customer, height=1, width=15, bg='#ff00ff', fg='#ffffff').grid(column=1, row=5, sticky=tk.W)
		tk.Button(mainframe, text="STAMPA LAVORI", font=self.mainButtonStyle, command=self.open_print_load, height=1, width=15, bg='#ff00ff', fg='#ffffff').grid(column=1, row=6, sticky=tk.W)
		tk.Button(mainframe, text="ESCI", font=self.mainButtonStyle, command=self.close, height=1, width=15, bg='#ff0000', fg='#ffffff').grid(column=1, row=7, sticky=tk.W)

		for child in mainframe.winfo_children(): 
			child.grid_configure(padx=5, pady=5)

	def open_insert_customer(self):
		w = InsertCustomer(self)
		w.grab_set()
	
	def open_manage_customer(self):
		w = ManageCustomer(self)
		w.grab_set()

	def open_manage_load(self):
		w = ManageLoad(self)
		w.grab_set()

	def open_insert_load(self):
		w = InsertLoad(self)
		w.grab_set()

	def open_print_load(self):
		w = PrintLoad(self)
		w.grab_set()

	def print_customer(self):
		dir = "stampe/"
		path = dir+"elenco_aziende.pdf"
		
		c = canvas.Canvas(path, pagesize=A4)  # alternatively use bottomup=False
		
		width, height = A4
		styles = getSampleStyleSheet()
		
		ptext1 = "ABC snc" 
		ptext2 = "di DEF C."
		ptext3 = "46100 Mantova (MN)"
		ptext4 = "Via Roma 1 Tel/Fax 0376 12345"
		ptext5 = "P.IVA e CF 00001111111"

		stile_h = ParagraphStyle(name='Normal', fontName='Helvetica-Bold', fontSize=12,)

		p1 = Paragraph(ptext1, style=stile_h)
		p2 = Paragraph(ptext2, style=stile_h)
		p3 = Paragraph(ptext3, style=stile_h)
		p4 = Paragraph(ptext4, style=stile_h)
		p5 = Paragraph(ptext5, style=stile_h)
		p1.wrapOn(c, 80*mm, 50*mm)  # size of 'textbox' for linebreaks etc.
		p1.drawOn(c, 10*mm, 275*mm)    # position of text / where to draw
		p2.wrapOn(c, 80*mm, 50*mm)  # size of 'textbox' for linebreaks etc.
		p2.drawOn(c, 10*mm, 270*mm)    # position of text / where to draw
		p3.wrapOn(c, 80*mm, 50*mm)  # size of 'textbox' for linebreaks etc.
		p3.drawOn(c, 10*mm, 265*mm)    # position of text / where to draw
		p4.wrapOn(c, 80*mm, 50*mm)  # size of 'textbox' for linebreaks etc.
		p4.drawOn(c, 10*mm, 260*mm)    # position of text / where to draw
		p5.wrapOn(c, 80*mm, 50*mm)  # size of 'textbox' for linebreaks etc.
		p5.drawOn(c, 10*mm, 255*mm)    # position of text / where to draw
		
		c.setLineWidth(3)
		c.line(10*mm,250*mm,180*mm,250*mm)
		
		data = []
		
		for i in range (0, len (self.anagrafiche)):
			tmp = []
			tmp.append(self.anagrafiche[i]['cognome'])
			tmp.append(self.anagrafiche[i]['nome'])
			tmp.append(self.anagrafiche[i]['telefono'])
			data.append(tmp)
		
		table = Table(data, colWidths=50*mm)
		table.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), 'Helvetica'), ('FONTSIZE', (0,0), (-1,-1), 12)]))
		table.wrapOn(c, width, height)
		table.drawOn(c, 20*mm, (250-7.5*len (self.anagrafiche))*mm)
				
		c.save()
		showinfo(title='Conferma',message='Documento prodotto correttamente.',parent=self)

app = GestionaleMais()
app.mainloop()
