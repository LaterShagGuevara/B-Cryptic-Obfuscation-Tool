"""
B-Cryptic Encoder/Decoder GUI Application
Provides a user-friendly interface for B-Cryptic text and PDF processing.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
from b_cryptic_core import encode_b_cryptic, decode_b_cryptic, B_CRYPTIC_ENCODING_TABLE  # Import from b_cryptic_core
from b_cryptic_pdf_app import BCrypticPdfProcessor

class BCrypticApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title(" B-Cryptic™ Obsfuscation Tool   0.2.8.52a")
        self.geometry("1200x850")
        
        self.pdf_processor = BCrypticPdfProcessor()
        self.create_widgets()
        self.create_footer()

    def create_footer(self):
        footer_frame = ttk.Frame(self)
        footer_frame.pack(side="bottom", fill="x", pady=15)  

        footer_label = ttk.Label(
            footer_frame, 
            text="Visit My Website:", 
            foreground="black",   
        )
        footer_label.pack(side="left", padx=5)

        website_link = ttk.Label(
            footer_frame, 
            text="B-Ready Studios LLC", #hyperlink text
            foreground="black",  
            cursor="hand2",
            background="light grey"  
        )
        website_link.pack(side="left")

        # Open the website in the default browser
        website_link.bind("<Button-1>", lambda e: os.system("start https://breadystudios.com/"))

    def create_widgets(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Text processing tab
        text_frame = ttk.Frame(notebook)
        notebook.add(text_frame, text="Text Processing")
        
        # Input text area
        input_label = ttk.Label(text_frame, text="Input Text:")
        input_label.pack(pady=5)
        
        self.input_text = scrolledtext.ScrolledText(text_frame, height=10)
        self.input_text.pack(fill='both', expand=True, padx=5)
        
        # Buttons frame
        button_frame = ttk.Frame(text_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Encode", command=self.encode_text).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Decode", command=self.decode_text).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_text).pack(side='left', padx=5)
        
        # Output text area
        output_label = ttk.Label(text_frame, text="Output:")
        output_label.pack(pady=5)
        
        self.output_text = scrolledtext.ScrolledText(text_frame, height=10)
        self.output_text.pack(fill='both', expand=True, padx=5)
        
        # PDF processing tab
        pdf_frame = ttk.Frame(notebook)
        notebook.add(pdf_frame, text="PDF Processing")
        
        # PDF controls
        pdf_controls = ttk.Frame(pdf_frame)
        pdf_controls.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(pdf_controls, text="Select Input PDF", command=self.select_input_pdf).pack(side='left', padx=5)
        ttk.Button(pdf_controls, text="Select Output Directory", command=self.select_output_dir).pack(side='left', padx=5)
        
        # Processing options
        options_frame = ttk.LabelFrame(pdf_frame, text="Processing Options")
        options_frame.pack(fill='x', padx=5, pady=5)
        
        self.batch_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Batch Processing", variable=self.batch_var).pack(side='left', padx=5)
        
        self.mode_var = tk.StringVar(value="encode")
        ttk.Radiobutton(options_frame, text="Encode", variable=self.mode_var, value="encode").pack(side='left', padx=5)
        ttk.Radiobutton(options_frame, text="Decode", variable=self.mode_var, value="decode").pack(side='left', padx=5)
        
        # Process button
        ttk.Button(pdf_frame, text="Process PDF", command=self.process_pdf).pack(pady=10)
        
        # Status area
        self.status_text = scrolledtext.ScrolledText(pdf_frame, height=10)
        self.status_text.pack(fill='both', expand=True, padx=5, pady=5)

    # Dark Mode Toggle Button
        self.is_dark_mode = False  # Tracks current mode

        self.dark_mode_button = tk.Button(
            self,
            text="Dark Mode",
            bg="black",
            fg="grey",
            command=self.toggle_dark_mode,
            font=("Arial", 10, "bold")
        )
        self.dark_mode_button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)  # Top-right corner

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        dark = self.is_dark_mode

        # Update colors
        bg_color = "#1e1e1e" if dark else "SystemButtonFace"
        fg_color = "#ffffff" if dark else "black"
        text_bg = "#2b2b2b" if dark else "white"
        text_fg = "#ffffff" if dark else "black"

        self.configure(bg=bg_color)
        self.dark_mode_button.configure(
            text="Light Mode" if dark else "Dark Mode",
            bg="white" if dark else "black",
            fg="black" if dark else "white"
        )

        # Loop through main child widgets
        for widget in self.winfo_children():
            if isinstance(widget, (tk.Frame, ttk.Frame, tk.Label, ttk.Label, tk.Button, ttk.Button)):
                try:
                    widget.configure(bg=bg_color, fg=fg_color)
                except:
                    pass

        # Update text boxes
        for text_widget in [self.input_text, self.output_text, self.status_text]:
            text_widget.configure(bg=text_bg, fg=text_fg, insertbackground=text_fg)

    ### 
    def encode_text(self):
        try:
            input_text = self.input_text.get("1.0", "end-1c")
            encoded = encode_b_cryptic(input_text)  # Call function from b_cryptic_core
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", encoded)
        except Exception as e:
            messagebox.showerror("Error", f"Encoding failed: {str(e)}")

    def decode_text(self):
        try:
            input_text = self.input_text.get("1.0", "end-1c").strip()  # Ensure full input is captured
            decoded = decode_b_cryptic(input_text)

            if not decoded:
                decoded = "[Decoding failed: No recognizable tokens]"

            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", decoded)

        except Exception as e:
            messagebox.showerror("Error", f"Decoding failed: {str(e)}")

    def clear_text(self):
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")

    def select_input_pdf(self):
        if self.batch_var.get():
            path = filedialog.askdirectory(title="Select Input Directory")
        else:
            path = filedialog.askopenfilename(
                title="Select PDF File",
                filetypes=[("PDF files", "*.pdf")]
            )
        if path:
            self.input_path = path
            self.log_status(f"Selected input: {path}")

    def select_output_dir(self):
        path = filedialog.askdirectory(title="Select Output Directory")
        if path:
            self.output_path = path
            self.log_status(f"Selected output directory: {path}")

    def process_pdf(self):
        if not hasattr(self, 'input_path') or not hasattr(self, 'output_path'):
            messagebox.showerror("Error", "Please select input and output locations")
            return
            
        try:
            if self.batch_var.get():
                successful, failed = self.pdf_processor.batch_process(
                    self.input_path,
                    self.output_path,
                    self.mode_var.get()
                )
                self.log_status(f"Batch processing complete\nSuccessful: {len(successful)}\nFailed: {len(failed)}")
            else:
                output_file = os.path.join(
                    self.output_path,
                    f"b_cryptic_{os.path.basename(self.input_path)}"
                )
                if self.mode_var.get() == "encode":
                    success = self.pdf_processor.encode_pdf(self.input_path, output_file)
                else:
                    success = self.pdf_processor.decode_pdf(self.input_path, output_file)
                    
                if success:
                    self.log_status("PDF processing completed successfully")
                else:
                    self.log_status("PDF processing failed")
                    
        except Exception as e:
            messagebox.showerror("Error", f"PDF processing failed: {str(e)}")

    def log_status(self, message):
        self.status_text.insert("end", f"{message}\n")
        self.status_text.see("end")

if __name__ == "__main__":
    app = BCrypticApplication()
    app.mainloop()
