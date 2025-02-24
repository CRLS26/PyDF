import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PIL import Image
import threading

icone = os.path.join(os.path.dirname(__file__), 'PyDF.ico')
class PyDF(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("PyDF - Manipulador de PDF")
        self.geometry("600x700")
        self.configure(bg='#f0f0f0')
        
        try:
            if os.path.exists(icone):
                self.iconbitmap(icone)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")
        
        self.init_variables()
        self.create_interface()
        
    def init_variables(self):
        self.input_pdf = None
        self.output_dir = None
        self.selected_files = []
        
    def create_interface(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        title = ttk.Label(main_frame, 
                         text="PyDF - Manipulador de PDF", 
                         font=('Helvetica', 16, 'bold'))
        title.pack(pady=10)

        operations_frame = ttk.LabelFrame(main_frame, text="Operações Disponíveis")
        operations_frame.pack(fill='x', pady=5)
        
        ttk.Button(operations_frame,
                  text="Dividir PDF",
                  command=self.split_pdf_dialog,
                  padding=(20, 10)).pack(fill='x', padx=5, pady=2)
        
        ttk.Button(operations_frame,
                  text="Unir PDFs",
                  command=self.merge_pdfs_dialog,
                  padding=(20, 10)).pack(fill='x', padx=5, pady=2)
        
        ttk.Button(operations_frame,
                  text="Converter PNG para PDF",
                  command=self.png_to_pdf_dialog,
                  padding=(20, 10)).pack(fill='x', padx=5, pady=2)
        
        ttk.Button(operations_frame,
                  text="Converter PDF para PNG",
                  command=self.pdf_to_png_dialog,
                  padding=(20, 10)).pack(fill='x', padx=5, pady=2)

        log_frame = ttk.LabelFrame(main_frame, text="Log de Operações")
        log_frame.pack(fill='both', expand=True, pady=5)
        
        self.log_text = tk.Text(log_frame, height=15, width=50)
        self.log_text.pack(padx=5, pady=5, fill='both', expand=True)
        
        self.progress = ttk.Progressbar(main_frame, 
                                      mode='determinate',
                                      length=400)
        self.progress.pack(pady=10)

    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.update_idletasks()

    def show_error(self, title, message):
        try:
            if os.path.exists(icone):
                messagebox.showerror(title, message, icon=icone)
            else:
                messagebox.showerror(title, message)
        except:
            messagebox.showerror(title, message)

    def show_info(self, title, message):
        try:
            if os.path.exists(icone):
                messagebox.showinfo(title, message, icon=icone)
            else:
                messagebox.showinfo(title, message)
        except:
            messagebox.showinfo(title, message)

    def split_pdf_dialog(self):
        self.input_pdf = filedialog.askopenfilename(
            title="Selecione o PDF para dividir",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if self.input_pdf:
            self.output_dir = filedialog.askdirectory(
                title="Selecione o diretório de saída"
            )
            if self.output_dir:
                threading.Thread(target=self.split_pdf).start()

    def split_pdf(self):
        try:
            reader = PdfReader(self.input_pdf)
            total_pages = len(reader.pages)
            
            self.log(f"Dividindo o PDF em {total_pages} partes...")
            self.progress['value'] = 0
            
            for i in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                
                output_path = os.path.join(self.output_dir, f"pagina_{i+1}.pdf")
                with open(output_path, "wb") as output_pdf:
                    writer.write(output_pdf)
                
                self.log(f"Página {i+1} salva em: {output_path}")
                self.progress['value'] = ((i + 1) / total_pages) * 100
            
            self.log("Divisão concluída!")
            self.show_info("Sucesso", "PDF dividido com sucesso!")
            
        except Exception as e:
            self.log(f"Erro: {str(e)}")
            self.show_error("Erro", f"Ocorreu um erro: {str(e)}")
        
        finally:
            self.progress['value'] = 0

    def merge_pdfs_dialog(self):
        self.selected_files = filedialog.askopenfilenames(
            title="Selecione os PDFs para unir",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if self.selected_files:
            output_path = filedialog.asksaveasfilename(
                title="Salvar PDF unificado como",
                defaultextension=".pdf",
                filetypes=[("Arquivos PDF", "*.pdf")]
            )
            if output_path:
                threading.Thread(target=lambda: self.merge_pdfs(output_path)).start()

    def merge_pdfs(self, output_path):
        try:
            merger = PdfMerger()
            total_files = len(self.selected_files)
            
            self.log("Iniciando união dos PDFs...")
            self.progress['value'] = 0
            
            for i, pdf in enumerate(self.selected_files):
                merger.append(pdf)
                self.log(f"Adicionado: {os.path.basename(pdf)}")
                self.progress['value'] = ((i + 1) / total_files) * 100
            
            with open(output_path, "wb") as output_file:
                merger.write(output_file)
            
            self.log("União concluída!")
            self.show_info("Sucesso", "PDFs unidos com sucesso!")
            
        except Exception as e:
            self.log(f"Erro: {str(e)}")
            self.show_error("Erro", f"Ocorreu um erro: {str(e)}")
        
        finally:
            self.progress['value'] = 0

    def png_to_pdf_dialog(self):
        self.selected_files = filedialog.askopenfilenames(
            title="Selecione as imagens PNG",
            filetypes=[("Imagens PNG", "*.png")]
        )
        if self.selected_files:
            output_path = filedialog.asksaveasfilename(
                title="Salvar PDF como",
                defaultextension=".pdf",
                filetypes=[("Arquivos PDF", "*.pdf")]
            )
            if output_path:
                threading.Thread(target=lambda: self.png_to_pdf(output_path)).start()

    def png_to_pdf(self, output_path):
        try:
            images = []
            total_files = len(self.selected_files)
            
            self.log("Convertendo imagens para PDF...")
            self.progress['value'] = 0
            
            for i, png in enumerate(self.selected_files):
                image = Image.open(png)
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                images.append(image)
                self.log(f"Convertido: {os.path.basename(png)}")
                self.progress['value'] = ((i + 1) / total_files) * 100
            
            if images:
                images[0].save(output_path, save_all=True, append_images=images[1:])
                self.log("Conversão concluída!")
                self.show_info("Sucesso", "Imagens convertidas para PDF com sucesso!")
            
        except Exception as e:
            self.log(f"Erro: {str(e)}")
            self.show_error("Erro", f"Ocorreu um erro: {str(e)}")
        
        finally:
            self.progress['value'] = 0

    def pdf_to_png_dialog(self):
        self.input_pdf = filedialog.askopenfilename(
            title="Selecione o PDF para converter",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if self.input_pdf:
            self.output_dir = filedialog.askdirectory(
                title="Selecione o diretório para salvar as imagens"
            )
            if self.output_dir:
                threading.Thread(target=self.pdf_to_png).start()

    def pdf_to_png(self):
        try:
            self.log("Convertendo PDF para imagens...")
            self.progress['value'] = 0
            reader = PdfReader(self.input_pdf)
            total_pages = len(reader.pages)
            for i in range(total_pages):
                page = reader.pages[i]
                for image_file_object in page.images:
                    output_path = os.path.join(self.output_dir, f"pagina_{i+1}.png")
                    with open(output_path, "wb") as image_file:
                        image_file.write(image_file_object.data)
                    self.log(f"Página {i+1} salva como: {output_path}")
                    self.progress['value'] = ((i + 1) / total_pages) * 100
            
            self.log("Conversão concluída!")
            self.show_info("Sucesso", "PDF convertido para imagens com sucesso!")
            
        except Exception as e:
            self.log(f"Erro: {str(e)}")
            self.show_error("Erro", f"Ocorreu um erro: {str(e)}")
        
        finally:
            self.progress['value'] = 0

if __name__ == "__main__":
    app = PyDF()
    app.mainloop()
