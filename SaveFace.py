import os
import cv2
import tkinter as tk
from tkinter import ttk
import PIL.Image, PIL.ImageTk

class SaveFace:
    def __init__(self, master, principal):
        self.principal = principal
        self.master = master
        self.master.title("Ventana de la Cámara")

        # Variables
        self.save_path = ""
        self.capture_images = False
        self.count = 0

        self.camera_frame = ttk.Frame(self.master)
        self.camera_frame.grid(row=0, column=0)

        self.cap = cv2.VideoCapture(0)
        ret, frame = self.cap.read()

        if ret:
            self.height, self.width = frame.shape[:2]
            self.canvas = tk.Canvas(self.camera_frame, width=self.width, height=self.height)
            self.canvas.grid(row=0, column=0)

            self.update_camera()

    def update_camera(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') # type: ignore
        ret, frame = self.cap.read()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            if self.capture_images:
                self.rec_Camera(frame, face_cascade)
            
        self.master.after(10, self.update_camera)
    
    def rec_Camera(self, frame, face_cascade):
        self.principal.info_label("captura #"+str(self.count+1))
        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar rostros
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Mostrar el frame con los rostros detectados
        # Capturar y guardar imágenes
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            roi_color = frame[y:y+h, x:x+w]
            roi_color = cv2.resize(roi_color, (150, 150), interpolation=cv2.INTER_CUBIC)  # Redimensionar a 150x150

            img_name = os.path.join(self.save_path, f"rostro_{self.count:03d}.jpg")
            cv2.imwrite(img_name, roi_color)

            self.count += 1
            if self.count >= 200:
                self.capture_images = False
                self.count = 0
                self.principal.finish_rec()

    # Crear una carpeta para guardar las imágenes si no existe
    def save_Path(self, emotion):
        self.save_path = "data/emotions/"+emotion
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def close_camera(self):
        if self.cap:
            self.cap.release()
        self.master.destroy()