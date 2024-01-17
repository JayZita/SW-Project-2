import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from SPDbSqlite import SPDbSqlite
from PIL import Image, ImageTk

class SPGuiCtk(customtkinter.CTk):

    def __init__(self, dataBase=SPDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

         # Load background image
        bg_image = Image.open("bgimage.jpg")    
        bg_image = bg_image.resize((1450, 700), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        self.title('RPG Game')
        self.geometry('1450x700')
        self.config(bg='#161C25')
        self.resizable(False, False)

        self.font1 = ('Arial', 20, 'bold')
        self.font2 = ('Arial', 12, 'bold')

        # Data Entry Form
        # 'ID' Label and Entry Widgets
        self.id_label = self.newCtkLabel('ID')
        self.id_label.place(x=20, y=40)
        self.id_entry = self.newCtkEntry()
        self.id_entry.place(x=100, y=40)

        # 'Name' Label and Entry Widgets
        self.name_label = self.newCtkLabel('Name')
        self.name_label.place(x=20, y=100)
        self.name_entry = self.newCtkEntry()
        self.name_entry.place(x=100, y=100)

        # 'Job' Label and Combo Box Widgets
        self.job_label = self.newCtkLabel('Job')
        self.job_label.place(x=20, y=160)
        self.job_cboxVar = StringVar()
        self.job_cboxOptions = ['Swordsman', 'Ranger', 'Mage', 'Assassin', 'Blacksmith', 'Priest']
        self.job_cbox = self.newCtkComboBox(options=self.job_cboxOptions, 
                                    entryVariable=self.job_cboxVar)
        self.job_cbox.place(x=100, y=160)

        # 'Level' Label and Entry Widgets
        self.level_label = self.newCtkLabel('Level')
        self.level_label.place(x=20, y=220)
        self.level_entry = self.newCtkEntry()
        self.level_entry.place(x=100, y=220)

        # 'Status' Label and Combo Box Widgets
        self.status_label = self.newCtkLabel('Status')
        self.status_label.place(x=20, y=280)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['Finding Quest', 'On Quest', 'Finished Quest']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=100, y=280)


        self.add_button = self.newCtkButton(text='Add Character',
                                onClickHandler=self.add_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=50,y=350)

        self.new_button = self.newCtkButton(text='New Character',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=50,y=400)

        self.update_button = self.newCtkButton(text='Update Character',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=50,y=450)

        self.delete_button = self.newCtkButton(text='Delete Character',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404',
                                    hoverColor='#AE0000',
                                    borderColor='#E40404')
        self.delete_button.place(x=50,y=500)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.export_button.place(x=50,y=550)

        self.import_button = self.newCtkButton(text='Import from CSV', 
                                    onClickHandler=self.import_to_csv,)
        self.import_button.place(x=50, y=600) 

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#fff',
                        background='#000',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('ID', 'Name', 'Job', 'Level', 'Status')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.CENTER, width=10)
        self.tree.column('Name', anchor=tk.CENTER, width=150)
        self.tree.column('Job', anchor=tk.CENTER, width=150)
        self.tree.column('Level', anchor=tk.CENTER, width=10)
        self.tree.column('Status', anchor=tk.CENTER, width=150)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Job', text='Job')
        self.tree.heading('Level', text='Level')
        self.tree.heading('Status', text='Status')

        self.tree.place(x=370, y=40, width=1000, height=500)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#161C25'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=250
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        border_color=widget_BorderColor,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly')
        
        # set default value to 1st option
        widget.set(options[0])

        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=260
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
                                        width=widget_Width)
       
        return widget

    # Handles
    def add_to_treeview(self):
        characters = self.db.fetch_characters()
        self.tree.delete(*self.tree.get_children())
        for character in characters:
            print(character)
            self.tree.insert('', END, values=character)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.id_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.job_cboxVar.set('Swordsman')
        self.level_entry.delete(0, END)
        self.status_cboxVar.set('Finding Quest')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.id_entry.insert(0, row[0])
            self.name_entry.insert(0, row[1])
            self.job_cboxVar.set(row[2])
            self.level_entry.insert(0, row[3])
            self.status_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        id=self.id_entry.get()
        name=self.name_entry.get()
        job=self.job_cboxVar.get()
        level=self.level_entry.get()
        status=self.status_cboxVar.get()

        if not (id and name and job and level and status):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.id_exists(id):
            messagebox.showerror('Error', 'ID already exists')
        else:
            self.db.insert_character(id, name, job, level, status)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an employee to delete')
        else:
            id = self.id_entry.get()
            self.db.delete_character(id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an employee to update')
        else:
            id=self.id_entry.get()
            name=self.name_entry.get()
            job=self.job_cboxVar.get()
            level=self.level_entry.get()
            status=self.status_cboxVar.get()
            self.db.update_character(name, job, level, status, id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')

    def import_to_csv(self):
        csv_filename = 'SPDb.csv'
        self.db.import_csv(csv_filename)
        self.add_to_treeview()
        messagebox.showinfo('Success', f'Data imported from {self.db.dbName}')

    





