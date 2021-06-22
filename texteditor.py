from tkinter import *
from tkinter.filedialog import *
import tkinter.font
import subprocess
editor = Tk()
editor.title('Text Editor')
editor.configure()
editor['bg'] = 'black'
text_area = Text()
text_area.configure(bg = 'black',foreground = 'white',insertbackground = 'white',relief=RAISED,cursor='arrow',selectbackground = 'yellow')
text_area.pack()
path_ = ''
def execute(event):
    result = f'python {path_}'
    process = subprocess.Popen(result,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=TRUE)
    result,error = process.communicate()
    output.insert(END,result)
    output.insert(END,error)
    #code = text_area.get('1.0',END)
    #exec(code)
editor.bind('<Control-Return>',execute)
def file_path(path):
    global path_
    path_ = path
def open_(event):
    path = askopenfilename(filetypes=[('Python Files','*.py')])
    with open(path,'r') as file:
        code = file.read()
        text_area.delete('1.0',END)
        text_area.insert('1.0',code)
        file_path(path)
editor.bind('<Control-o>',open_)
def save(event):
    if path_ == '':
        path = asksaveasfilename(filetypes=[('Python Files','*.py')])
    else:
        path = path_
        with open(path,'w') as file:
            code = text_area.get('1.0',END)
            file.write(code)
            file_path(path)
editor.bind('<Control-s>',save)
#def execute_selected(event):
   #code = text_area.selection_get()
  #  result_selected = f'python {code}'
   # process = subprocess.Popen(result_selected,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=TRUE)
    #result_selected,error_selected = process.communicate()
    #output.insert(END,result_selected)
    #output.insert(END,error_selected)
def execute_selected(event):
    selection = text_area.tag_ranges(tkinter.SEL)
    if selection:
        print('Selected text is %r' % text_area.get(*selection))
    else:
        print('No selected text')
editor.bind('<Control-Shift-Return>',execute_selected)
output = Text(height=5)
output.configure(bg='black',foreground='white')
output.pack()
editor.mainloop()