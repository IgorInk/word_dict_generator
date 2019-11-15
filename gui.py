import tkinter as tk
import tkinter.messagebox as msg
import threading
import tkinter.ttk
import tkinter.filedialog as filedlg
import os
import os.path


TITLE = 'WORD DICTIONARY GENERATOR'
TITLE_SHORT = 'WDG'
root = tk.Tk()
root.title(TITLE)
dict_dir = tk.StringVar()
dict_dir.set(os.getcwd())
filename = tk.StringVar()
filename.set('dict.txt')


def product(*args, repeat=1):
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    res_2 = []
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
        res_2.extend(filter(lambda x:len("".join(x)) == repeat,result))
        print(result)
    for prod in res_2:
        yield tuple(prod)


def add_symbols(s='a-z', txt: tk.Text = None):
    a, z = s.split('-')
    res = []
    for i in range(ord(a), ord(z) + 1):
        res.append(chr(i))
    if txt:
        r = txt.get(1.0, 'end').split()
        r.extend(res)
        r = sorted(list(set(r)), key=lambda x: (len(x), x))
        txt.delete(1.0, 'end')
        txt.insert(1.0, ' '.join(r))


def generate_psw(txt: tk.Text, left=8, right=8, pb=None):
    # msg.showinfo("", f"starting generate psw from {left} to {right}")
    inx = 0
    sp = set(txt.get(1.0, 'end').split())
    if ' ' in sp:
        sp.remove(' ')
    with open(os.path.join(dict_dir.get(),filename.get()), 'w') as file:
        for i in range(left, right + 1):
            for word in product(sp, repeat=i):
                file.write(''.join(word) + "\n")
                inx += 1
    if pb:
        pb.destroy()
    if msg.askokcancel(TITLE_SHORT,f'dict has been generated!\n {inx} rows. View the file?'):
        if os.name == 'posix':
                os.system(f'cat {os.path.join(dict_dir.get(),filename.get())}')
        else:
            os.system('notepad.exe {os.path.join(dict_dir.get(),filename.get())}')

    # msg.showinfo('dict gen', f'dict has been generated!\n {inx} rows')


def create_menu(txt:tk.Text,root:tk.Tk):
    menu_panel = tk.Menu(root)
    file_menu = tk.Menu(menu_panel,tearoff=0)
    menu_panel.add_cascade(label='File',menu=file_menu)
    menu_panel.add_command(label='info',
                           command=lambda : msg.showinfo(title=TITLE_SHORT,message='Add symbols and words in editor.\nChoose generated words length.\n Select file directory and namto save words.\nStart or start in background.\nSevVetApps no rights reserved:)'))
    menu_panel.add_command(label='example',command = lambda :show_example(txt,root))
    file_menu.add_command(label='choose dict directory', command=lambda :dict_dir.set(filedlg.askdirectory(initialdir=os.getcwd())))

    root['menu'] = menu_panel


def generate_psw_background(txt: tk.Text, left=8, right=8, progress_root: tk.Tk = None):
    pb = tk.ttk.Progressbar(progress_root, orient='h', mode='indeterminate')
    pb.pack(side='bottom', fill='x', expand=1)
    pb.start()
    thread = threading.Thread(target=generate_psw, args=(txt, left, right, pb))
    thread.start()

def show_example(txt:tk.Text, root:tk.Tk=None):
    txt.delete(1.0,'end')
    txt.insert(1.0,'admin 1 2 3 4 5')
    generate_psw_background(txt, 6,6,root)


root['bg'] ='darkgray'

left_pan = tk.Frame(root, bg = 'darkgray')
right_pan = tk.Frame(root, bg='darkgray')
left_pan.pack(side=tk.LEFT)

right_pan.pack(side=tk.LEFT, fill='both', expand=1)
txt = tk.Text(right_pan, bg='darkblue', fg='white', insertbackground='yellow')
create_menu(txt, root)
# panel with shortcuts to add symbols sets
right_pan_inner_top_pan = tk.Frame(right_pan,bg='darkgray')
btn_add_a_z = tk.Button(right_pan_inner_top_pan, text="a-z", command=lambda: add_symbols('a-z', txt))
btn_add_a_z.pack(side='left')
btn_add_A_Z = tk.Button(right_pan_inner_top_pan, text="A-Z", command=lambda: add_symbols('A-Z', txt))
btn_add_A_Z.pack(side='left')
btn_add_a_ya = tk.Button(right_pan_inner_top_pan, text="а-я", command=lambda: add_symbols('а-я', txt))
btn_add_a_ya.pack(side='left')
btn_add_A_YA = tk.Button(right_pan_inner_top_pan, text="А-Я", command=lambda: add_symbols('А-Я', txt))
btn_add_A_YA.pack(side='left')
btn_add_0_9 = tk.Button(right_pan_inner_top_pan, text="0-9", command=lambda: add_symbols('0-9', txt))
btn_add_0_9.pack(side='left')
btn_clear = tk.Button(right_pan_inner_top_pan, text="clear", command=lambda: txt.delete(1.0,'end'))
btn_clear.pack(side='left')


ed_filename = tk.Entry(right_pan_inner_top_pan, textvariable=filename)
ed_filename.pack(side='right')
tk.Label(right_pan_inner_top_pan,text='/').pack(side='right')
tk.Label(right_pan_inner_top_pan,textvariable=dict_dir).pack(side='right')
tk.Label(right_pan_inner_top_pan,text='path:').pack(side='right')
right_pan_inner_top_pan.pack(side='top', fill='x', expand=1)

tk.Label(right_pan, text='used symbols and words(use space to separate):', font='48', bg='black',fg='yellow').pack(side='top', fill='x')
txt.pack(side='top', fill='both')
right_pan_inner_down = tk.Frame(right_pan,bg='darkgray')
right_pan_inner_down.pack(side='top', fill='both', expand=1)
psw_symbols_from = tk.IntVar(value=6)
psw_symbols_to = tk.IntVar(value=6)
sp_from = tk.Spinbox(right_pan_inner_down, from_=1, to=255, textvariable=psw_symbols_from, width=4)
sp_to = tk.Spinbox(right_pan_inner_down, from_=1, to=255, textvariable=psw_symbols_to, width=4)
btn_start = tk.Button(right_pan_inner_down, text='START', fg='red', bg='black', relief='groove',
                      command=lambda: generate_psw(txt, psw_symbols_from.get(), psw_symbols_to.get()))

btn_start_background = tk.Button(right_pan_inner_down, text='START IN BACKGROUND', fg='red', bg='black',
                                 relief='groove',
                                 command=lambda: generate_psw_background(txt, psw_symbols_from.get(),
                                                                         psw_symbols_to.get(), right_pan_inner_top_pan))
tk.Label(right_pan_inner_down, text='symbols in password (from - to):', bg='black',fg='yellow').pack(side='left')
sp_from.pack(side='left')
sp_to.pack(side='left')

btn_start_background.pack(side='right')
btn_start.pack(side='right')
# print(*product(['a', 'b', 'cat'], repeat=4))
root.mainloop()
