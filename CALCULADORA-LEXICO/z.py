import tkinter as tk
from tkinter import filedialog

def guardar_archivo():
    archivo_guardado = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if archivo_guardado is not None:
        contenido = texto.get('1.0', tk.END)
        archivo_guardado.write(contenido)
        archivo_guardado.close()

def abrir_archivo():
    archivo_abierto = filedialog.askopenfile(mode='r')
    if archivo_abierto is not None:
        contenido = archivo_abierto.read()
        texto.delete('1.0', tk.END)
        texto.insert(tk.END, contenido)
        archivo_abierto.close()

ventana = tk.Tk()
ventana.title("Bloc de Notas")

texto = tk.Text(ventana)
texto.pack()

menu = tk.Menu(ventana)
ventana.config(menu=menu)

archivo_menu = tk.Menu(menu)
menu.add_cascade(label="Archivo", menu=archivo_menu)
archivo_menu.add_command(label="Abrir", command=abrir_archivo)
archivo_menu.add_command(label="Guardar", command=guardar_archivo)

ventana.mainloop()
