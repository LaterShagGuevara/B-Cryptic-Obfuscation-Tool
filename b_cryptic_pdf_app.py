"""
PDF processing module for B-Cryptic encoding/decoding.
Handles batch processing of PDF files while preserving formatting.
"""

import os
import io
import re
import logging
from typing import List
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black
from b_cryptic_core import encode_b_cryptic, decode_b_cryptic, B_CRYPTIC_DECODING_TABLE

pdfmetrics.registerFont(TTFont('Courier', 'C:\\Windows\\Fonts\\cour.ttf'))

class BCrypticPdfProcessor:
    def __init__(self):
        self.errors: List[str] = []
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(f"Python Version: {os.sys.version}")
        logging.info(f"Python Executable: {os.sys.executable}")

    def _log_debug(self, msg): logging.debug(msg)

    def _create_text_page(self, text: str) -> PdfReader:
        from math import ceil
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        c.setFont("Courier", 10)

        has_blocks = any(m in text for m in ['[^', '[*', '[-', '[+'])
        lines = []

        if has_blocks:
            blocks = re.findall(r'\[[\^\*\-\+]?[0-9A-Za-z\-_]+\]', text)
            for i in range(0, len(blocks), 3):
                lines.append(''.join(blocks[i:i+3]))
        else:
            max_width = letter[0] - 144
            current_line, current_width = [], 0
            for word in text.split():
                word_width = c.stringWidth(word + " ", "Courier", 10)
                if current_width + word_width > max_width:
                    if current_line:
                        lines.append(" ".join(current_line))
                    current_line = [word]
                    current_width = word_width
                else:
                    current_line.append(word)
                    current_width += word_width
            if current_line:
                lines.append(" ".join(current_line))

        line_height = 18
        lines_per_page = int((letter[1] - 144) / line_height)
        total_pages = ceil(len(lines) / lines_per_page)

        for i in range(total_pages):
            page_lines = lines[i * lines_per_page:(i + 1) * lines_per_page]
            y = letter[1] - 72
            for line in page_lines:
                x = (letter[0] - c.stringWidth(line, "Courier", 10)) / 2
                c.drawString(x, y, line)
                y -= line_height
            if i < total_pages - 1:
                c.showPage()
                c.setFont("Courier", 10)

        self._log_debug(f"Created PDF with {len(lines)} lines across {total_pages} page(s)")
        c.save()
        packet.seek(0)
        return PdfReader(packet)

    def _process_text(self, text: str, encode=True) -> str:
        text = text.strip()
        if not text:
            raise ValueError("Text is empty")
        if encode:
            encoded = encode_b_cryptic(text)
            blocks = re.findall(r'\[[\^\*\-\+]?[0-9A-Za-z\-_]+\]', encoded)
            if not blocks or any(b not in B_CRYPTIC_DECODING_TABLE for b in blocks):
                raise ValueError("Invalid encoded output")
            return encoded
        else:
            blocks = re.findall(r'\[[\^\*\-\+]?[0-9A-Za-z\-_]+\]', text)
            clean_blocks = [b for b in blocks if b in B_CRYPTIC_DECODING_TABLE]
            return decode_b_cryptic(''.join(clean_blocks)) if clean_blocks else ""

    def encode_pdf(self, input_path: str, output_path: str) -> bool:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        success = True

        for page_num, page in enumerate(reader.pages):
            try:
                original_text = page.extract_text()
                if not original_text:
                    raise ValueError("Empty page text")
                processed_text = self._process_text(original_text, encode=True)
                new_pdf = self._create_text_page(processed_text)
                for np in new_pdf.pages:
                    writer.add_page(np)
            except Exception as e:
                self._log_debug(f"Page {page_num+1} failed: {e}")
                success = False

        with open(output_path, 'wb') as f:
            writer.write(f)
        return success

    def decode_pdf(self, input_path: str, output_path: str) -> bool:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        success = True

        for page_num, page in enumerate(reader.pages):
            try:
                encoded_text = page.extract_text()
                if not encoded_text:
                    raise ValueError("Empty page text")
                decoded_text = self._process_text(encoded_text, encode=False)
                new_pdf = self._create_text_page(decoded_text)
                for np in new_pdf.pages:
                    writer.add_page(np)
            except Exception as e:
                self._log_debug(f"Page {page_num+1} failed: {e}")
                success = False

        with open(output_path, 'wb') as f:
            writer.write(f)
        return success
