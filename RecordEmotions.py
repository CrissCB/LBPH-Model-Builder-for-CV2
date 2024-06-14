import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import re

import TrainModel
from SaveFace import SaveFace

class RecordEmotions:
    def __init__(self):
        # Limpiar txt
        with open('data/emotion_List.txt', "w") as file:
            file.write("")

        # Crear ventana
        self.root = tk.Tk()
        self.root.title("Creación de Modelo")

        # Variables
        self.row_count = 0
        self.var_cam = True
        self.emotion_rec = []

        #contenedor MAIN
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)) # type: ignore

        # filas y columnas del contenedor main
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        # Fin contenedor MAIN

        #contenedor IZQUIERDO
        cont_izq = ttk.Frame(main_frame, padding="10", relief="solid")
        cont_izq.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)) # type: ignore

        #titulo
        titulo = ttk.Label(cont_izq, text="Creación del Modelo", anchor="center")
        titulo.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Input list
        opc_var = tk.StringVar()
        self.opc_list = ttk.Combobox(cont_izq, textvariable=opc_var, state="readonly")
        self.opc_list['values'] = ('Alegria', 'Asombro', 'Disgusto','Enojo', 'Miedo', 'Neutro', 'Tristeza')
        self.opc_list.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.opc_list.current(0)

        #botones
        self.btn1 = ttk.Button(cont_izq, text="Encender Cámara", command=self.btn_cam_click)
        self.btn1.grid(row=2, column=0, padx=(5, 2), pady=5, sticky=tk.E, ipadx=10)

        self.btn2 = ttk.Button(cont_izq, text="Grabar", command=self.btn_grabar_click)
        self.btn2.grid(row=2, column=1, padx=(2, 5), pady=5, sticky=tk.W, ipadx=10)
        self.btn2.configure(state='disabled')

        #checklist
        self.checklst = ttk.LabelFrame(cont_izq, text="Nombre ...", padding="5")
        self.checklst.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E)) # type: ignore

        #fin contenedor IZQUIERDO

        #contenedor DERECHO
        cont_der = ttk.Frame(main_frame, padding="10", relief="solid")
        cont_der.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S)) # type: ignore

        #input ruta
        self.input_rout = ttk.Entry(cont_der)
        self.input_rout.grid(row=0, column=0, padx=5, pady=5)
        self.input_rout.configure(state='disabled')

        #botón seleccionar ruta
        self.btn_rout = ttk.Button(cont_der, text="Seleccionar carpeta", command=self.seleccionar_carpeta)
        self.btn_rout.grid(row=0, column=1, padx=5, pady=5)
        self.btn_rout.configure(state='disabled')

        #input nombre del modelo
        self.name_model = ttk.Entry(cont_der)
        self.name_model.grid(row=1, column=0, padx=5, pady=5)
        self.name_model.configure(state='disabled')

        #label nombre del modelo
        self.label_name_rout = ttk.Label(cont_der, text='Nombre del archivo')
        self.label_name_rout.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E)) # type: ignore

        #botón para crear modelo
        self.btn_draw = ttk.Button(cont_der, text="Crear Modelo", command=self.btn_crear_click)
        self.btn_draw.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.btn_draw.configure(state='disabled')

        #label info
        self.label_info = ttk.Label(cont_der, text='')
        self.label_info.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        #fin contenedor Derecho

        self.root.mainloop()

    # funciones para el botón cámara
    def btn_cam_click(self):

        if self.var_cam:
            self.btn1.configure(text='Apagar Cámara')
            self.btn2.configure(state='enabled')
            self.var_cam = False

            self.camera_window = tk.Toplevel(self.root)
            self.camera_window.protocol("WM_DELETE_WINDOW", self.on_closing_secondary)
            self.camera_app = SaveFace(self.camera_window, self)

        else:
            self.btn1.configure(text='Encender Cámara')
            self.btn2.configure(state='disabled')
            self.var_cam = True

            self.camera_app.close_camera()

    # funciones para el botón grabar
    def btn_grabar_click(self):
        self.add_list(self.opc_list.get())
        self.camera_app.save_Path(self.opc_list.get())
        
        self.btn1.configure(state="disabled")
        self.btn2.configure(state="disabled")

        self.camera_app.capture_images = True

    # funciones para el botón crear
    def btn_crear_click(self):
        if self.validar_ruta():
            self.btn1.configure(state="disabled")
            self.btn2.configure(state="disabled")
            self.btn_draw.configure(state="disabled")
            self.btn_rout.configure(state='disabled')
            self.input_rout.configure(state='disabled')
            self.name_model.configure(state='disabled')

            self.camera_app.close_camera()

            # Leer el archivo de texto
            with open("data/emotion_List.txt", "r") as file:
                # Leer todas las líneas del archivo y dividir cada línea en emociones separadas por "|"
                emociones_lineas = [linea.strip().split("|") for linea in file.readlines()]

            # Eliminar el último elemento de cada línea (que será un espacio vacío)
            for linea in emociones_lineas:
                del linea[-1]

            # Convertir la lista de listas en un solo arreglo de emociones
            emociones = [emocion for linea in emociones_lineas for emocion in linea]
            print(emociones)

            TrainModel.init_model(emociones, self.input_rout.get(), self.name_model.get(), self)

            self.finish_rec()
        else:
            messagebox.showerror("Error", "La ruta seleccionada no es una carpeta válida o digite un nombre valido")
    
    # Captura de imagenes terminado
    def finish_rec(self):
        self.btn1.configure(state="enabled")
        self.btn2.configure(state="enabled")
        self.btn_draw.configure(state="enabled")
        self.btn_rout.configure(state='enabled')
        self.input_rout.configure(state='enabled')
        self.name_model.configure(state='enabled')

    # funcion agragar en la lista
    def add_list(self, emotion):
        if emotion in self.emotion_rec:
            pass
        else:
            checkbox = ttk.Checkbutton(self.checklst, text=emotion, variable=tk.BooleanVar())
            checkbox.grid(row=self.row_count, column=0, sticky=tk.W)
            checkbox.state(['disabled'])

            self.emotion_rec.append(emotion)
            with open('data/emotion_List.txt', "a") as file:
                file.write(emotion+'|')
            self.row_count += 1
    
    # funcion para seleccionar carpeta
    def seleccionar_carpeta(self):
        ruta_carpeta = filedialog.askdirectory(title="Seleccionar una carpeta")
        if ruta_carpeta:
            if os.path.isdir(ruta_carpeta):
                self.input_rout.delete(0, tk.END)  # Limpiar el contenido anterior del Entry
                self.input_rout.insert(0, ruta_carpeta)  # Insertar la ruta del archivo
            else:
                messagebox.showerror("Error", "La ruta seleccionada no es una carpeta válida")

    def validar_ruta(self):
        ruta_carpeta = self.input_rout.get()
        nombre_archivo = self.name_model.get()

        nombre_archivo = nombre_archivo.strip()
        nombre_archivo = re.sub(r'\s+', ' ', nombre_archivo)

        if os.path.isdir(ruta_carpeta) and nombre_archivo != "":
            return True
        else:
            return False
    
    def info_label(self, text_info):
        self.label_info.config(text=text_info)
        
    def on_closing_secondary(self):
        print("no se puede cerrar la ventana")

if __name__ == "__main__":
    app = RecordEmotions()