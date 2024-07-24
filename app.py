import tkinter as tk
from tkinter import filedialog
import os
from reportlab.pdfgen import canvas
from PIL import Image

class Imgtopdfconverter:
    def __init__(self, root):
        self.root = root
        self.img_path = []
        self.output_pdf_name = tk.StringVar()
        self.selected_img_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.initialize_ui()

    def initialize_ui(self):
        title = tk.Label(self.root, text="Image To PDF Converter", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        select_images_button = tk.Button(self.root, text="Select Images", command=self.selected_images)
        select_images_button.pack(pady=(0, 10))

        self.selected_img_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        label = tk.Label(self.root, text="Enter output PDF name:")
        label.pack()

        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify="center")
        pdf_name_entry.pack()

        convert_button = tk.Button(self.root, text="Convert To PDF", command=self.convert_img_pdf)
        convert_button.pack(pady=(20, 40))

    def selected_images(self):
        self.img_path = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        self.selected_img_listbox.delete(0, tk.END)

        for images_path in self.img_path:
            _, images_path = os.path.split(images_path)
            self.selected_img_listbox.insert(tk.END, images_path)

    def convert_img_pdf(self):
        if not self.img_path:
            return

        output_pdf = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"

        pdf = canvas.Canvas(output_pdf, pagesize=(612, 792))

        for image_path in self.img_path:
            img = Image.open(image_path)
            available_width = 540
            available_height = 720
            scale_factor = min(available_width / img.width, available_height / img.height)
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor
            x_center = (612 - new_width) / 2
            y_center = (792 - new_height) / 2

            pdf.setFillColorRGB(1, 1, 1)
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawInlineImage(img, x_center, y_center, width=new_width, height=new_height)
            pdf.showPage()

        pdf.save()

def main():
    root = tk.Tk()
    root.title("Image To PDF Converter")
    converter = Imgtopdfconverter(root)
    root.geometry("400x600")
    root.mainloop()

if __name__ == "__main__":
    main()
