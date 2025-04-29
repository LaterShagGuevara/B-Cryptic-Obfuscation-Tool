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

        self.title(" B-Cryptic™ Obsfuscation Tool   v0.3.8.5a")
        self.geometry("1200x850")

        self.is_dark_mode = False  # Dark mode tracking
        self.pdf_processor = BCrypticPdfProcessor()
        self.style = ttk.Style()

        self.create_widgets()
        self.create_footer()
        self.create_dark_mode_button()

    def create_footer(self):
        self.footer_frame = ttk.Frame(self)
        self.footer_frame.pack(side="bottom", fill="x", pady=15)

        self.footer_label = ttk.Label(
            self.footer_frame,
            text="Visit My Website:",
        )
        self.footer_label.pack(side="left", padx=5)

        self.website_link = ttk.Label(
            self.footer_frame,
            text="B-Ready Studios LLC", #hyperlink text
            cursor="hand2",
        )
        self.website_link.pack(side="left")
        self.website_link.bind("<Button-1>", lambda e: os.system("start https://breadystudios.com/"))

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)

        # Text processing tab
        self.text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_frame, text="Text Processing")

        # Input text area
        input_label = ttk.Label(self.text_frame, text="Input Text:")
        input_label.pack(pady=5)

        self.input_text = scrolledtext.ScrolledText(self.text_frame, height=10)
        self.input_text.pack(fill='both', expand=True, padx=5)

        # Buttons frame
        button_frame = ttk.Frame(self.text_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Encode", command=self.encode_text).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Decode", command=self.decode_text).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_text).pack(side='left', padx=5)

        # Output text area
        output_label = ttk.Label(self.text_frame, text="Output:")
        output_label.pack(pady=5)

        self.output_text = scrolledtext.ScrolledText(self.text_frame, height=10)
        self.output_text.pack(fill='both', expand=True, padx=5)

        # PDF processing tab
        self.pdf_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pdf_frame, text="PDF Processing")

        # PDF controls
        pdf_controls = ttk.Frame(self.pdf_frame)
        pdf_controls.pack(fill='x', padx=5, pady=5)

        ttk.Button(pdf_controls, text="Select Input PDF", command=self.select_input_pdf).pack(side='left', padx=5)
        ttk.Button(pdf_controls, text="Select Output Directory", command=self.select_output_dir).pack(side='left', padx=5)

        # Processing options
        options_frame = ttk.LabelFrame(self.pdf_frame, text="Processing Options")
        options_frame.pack(fill='x', padx=5, pady=5)

        self.batch_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Batch Processing", variable=self.batch_var).pack(side='left', padx=5)

        self.mode_var = tk.StringVar(value="encode")
        ttk.Radiobutton(options_frame, text="Encode", variable=self.mode_var, value="encode").pack(side='left', padx=5)
        ttk.Radiobutton(options_frame, text="Decode", variable=self.mode_var, value="decode").pack(side='left', padx=5)

        # Process button
        ttk.Button(self.pdf_frame, text="Process PDF", command=self.process_pdf).pack(pady=10)

        # Status area
        self.status_text = scrolledtext.ScrolledText(self.pdf_frame, height=10)
        self.status_text.pack(fill='both', expand=True, padx=5, pady=5)

        # Dark Mode Toggle Button
    def create_dark_mode_button(self):
        self.dark_mode_button = tk.Button(
            self,
            text="Dark Mode",
            bg="black",
            fg="light grey",
            command=self.toggle_dark_mode,
            font=("Arial", 10, "bold")
        )
        self.dark_mode_button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        dark = self.is_dark_mode

        bg_color = "#3a3a3a" if dark else "SystemButtonFace"
        btn_color = "#3a3a3a" if dark else "SystemButtonFace"
        fg_color = "#000000" if dark else "black"
        text_bg = "#2b2b2b" if dark else "white"
        text_fg = "#ffffff" if dark else "black"

        self.configure(bg=bg_color)

        # Update ttk style
        self.style.configure(".", background=bg_color, foreground=fg_color)
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", background=bg_color, foreground=fg_color)
        self.style.configure("TButton", background=btn_color, foreground=fg_color)
        self.style.configure("TNotebook", background=bg_color)
        self.style.configure("TNotebook.Tab", background=btn_color, foreground=fg_color)
        self.style.map("TButton", background=[('active', '#505050' if dark else 'lightgrey')], foreground=[('active', fg_color)])

        self.dark_mode_button.configure(
            text="Light Mode" if dark else "Dark Mode",
            bg="white" if dark else "black",
            fg="black" if dark else "white"
        )

        for widget in [self.input_text, self.output_text, self.status_text]:
            widget.configure(bg=text_bg, fg=text_fg, insertbackground=text_fg)

    def encode_text(self):
        try:
            input_text = self.input_text.get("1.0", "end-1c")
            encoded = encode_b_cryptic(input_text)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", encoded)
        except Exception as e:
            messagebox.showerror("Error", f"Encoding failed: {str(e)}")

    def decode_text(self):
        try:
            input_text = self.input_text.get("1.0", "end-1c").strip()
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
