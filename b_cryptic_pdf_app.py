"""
PDF processing module for B-Cryptic encoding/decoding.
Handles batch processing of PDF files while preserving formatting.
"""

import os
import io
import sys
import logging
from typing import Tuple, List, Dict, Optional
from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black
from b_cryptic_core import encode_b_cryptic, decode_b_cryptic, B_CRYPTIC_DECODING_TABLE

# Register Courier font for better text extraction
pdfmetrics.registerFont(TTFont('Courier', 'C:\\Windows\\Fonts\\cour.ttf'))

class BCrypticPdfProcessor:
    """Handles PDF processing for B-Cryptic encoding/decoding."""
    
    def __init__(self):
        self.errors: List[str] = []
        self.processed_files = 0
        self.total_pages = 0
        self._setup_logging()
        
    def _setup_logging(self):
        """Configure logging with detailed format."""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Log Python version and executable
        import sys
        logging.info(f"Python Version: {sys.version}")
        logging.info(f"Python Executable: {sys.executable}")
        
    def _log_debug(self, message: str):
        """Log a debug message."""
        logging.debug(message)
            
    def _extract_text_from_page(self, page) -> str:
        """Extract text from a PDF page while preserving B-Cryptic blocks."""
        try:
            # Extract raw text and normalize whitespace
            raw_text = page.extract_text().strip()
            if not raw_text:
                return ""
                
            # If text contains B-Cryptic markers, extract blocks carefully
            if '[' in raw_text:
                import re
                # Extract complete B-Cryptic blocks, preserving exact format
                # Pattern matches both uppercase and lowercase blocks
                pattern = r'\[[\^\*\-\+]?[0-9A-Za-z\-_]+\]'
                blocks = re.finditer(pattern, raw_text)
                extracted_blocks = []
                
                for match in blocks:
                    block = match.group(0)
                    # Verify block is in decoding table
                    if block in B_CRYPTIC_DECODING_TABLE:
                        extracted_blocks.append(block)
                    else:
                        self._log_debug(f"Invalid block found: {block}")
                        
                if extracted_blocks:
                    # Join blocks with no spaces to match encoding format
                    return ''.join(extracted_blocks)
                    
            return raw_text
            
        except Exception as e:
            error_msg = f"Failed to extract text: {str(e)}"
            self._log_debug(error_msg)
            self.errors.append(error_msg)
            return "[Text extraction failed]"
            
    def _process_text(self, text: str, encode: bool = True) -> str:
        """Process text for encoding or decoding."""
        try:
            if encode:
                # Call core encoding function
                encoded = encode_b_cryptic(text)
                if not encoded:
                    raise ValueError("Encoding failed")
                    
                # Verify encoded text contains valid blocks
                import re
                blocks = re.findall(r'\[[\^\*\-\+]?[0-9A-Za-z\-_]+\]', encoded)
                if not blocks:
                    raise ValueError("Encoding produced no valid B-Cryptic blocks")
                    
                # Verify each block is in decoding table
                invalid_blocks = [b for b in blocks if b not in B_CRYPTIC_DECODING_TABLE]
                if invalid_blocks:
                    self._log_debug(f"Invalid blocks found: {invalid_blocks}")
                    raise ValueError(f"Found {len(invalid_blocks)} invalid blocks")
                    
                return encoded
                
            else:
                # Clean up input text
                text = text.strip()
                if not text:
                    raise ValueError("Input text is empty")
                    
                # Extract and validate B-Cryptic blocks
                import re
                blocks = re.finditer(r'\[[\^\*\-\+]?[0-9A-Za-z\-_]+\]', text)
                valid_blocks = []
                
                for match in blocks:
                    block = match.group(0)
                    # Only include blocks that are in the decoding table
                    if block in B_CRYPTIC_DECODING_TABLE:
                        valid_blocks.append(block)
                    else:
                        self._log_debug(f"Skipping invalid block: {block}")
                        
                if not valid_blocks:
                    raise ValueError("No valid B-Cryptic blocks found")
                    
                # Join blocks and decode
                joined_blocks = ''.join(valid_blocks)
                decoded = decode_b_cryptic(joined_blocks)
                if not decoded:
                    raise ValueError("Decoding failed")
                    
                # Verify no B-Cryptic markers remain
                if '[^' in decoded or '[*' in decoded or '[-' in decoded:
                    raise ValueError("Decoding left B-Cryptic markers in output")
                    
                return decoded
                
        except Exception as e:
            self._log_debug(f"Text processing failed: {str(e)}")
            raise
            
    def _create_text_page(self, text: str) -> PdfReader:
        """Create a PDF page with the given text."""
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        
        # Use slightly larger monospace font for better readability
        c.setFont("Courier", 10)
        
        # Check if text contains B-Cryptic blocks
        has_blocks = any(marker in text for marker in ['[^', '[*', '[-'])
        
        if has_blocks:
            # Extract B-Cryptic blocks
            import re
            blocks = re.findall(r'\[[\^\*\-\+]?[0-9A-Za-z\-_]+\]', text)
            
            # Group blocks into lines of 3
            lines = []
            for i in range(0, len(blocks), 3):
                # No Space 
                line = ''.join(blocks[i:i+3])
                lines.append(line)
                
        else:
            # Regular text - use standard word wrapping
            max_width = letter[0] - 144  # 72 points margin on each side
            lines = []
            current_line = []
            current_width = 0
            
            # Split on whitespace for normal text
            words = text.split()
            
            # Process each word
            for word in words:
                # Get width of word plus a space
                word_width = c.stringWidth(word + " ", "Courier", 10)
                
                # If word would exceed line width, start a new line
                if current_width + word_width > max_width:
                    if current_line:  # Only add line if it has content
                        lines.append(" ".join(current_line))
                    current_line = [word]
                    current_width = word_width
                else:
                    current_line.append(word)
                    current_width += word_width
                    
            # Add the last line if it has content
            if current_line:
                lines.append(" ".join(current_line))
                
            # Write text lines with automatic page overflow
            y = letter[1] - 72  # Top margin
            line_height = 18    # Space between lines
            c.setFont("Courier", 10)

            for i, line in enumerate(lines):
                if y < 72:  # If we're too low on the page, add a new one
                    c.showPage()
                    c.setFont("Courier", 10)
                    y = letter[1] - 72

                line_width = c.stringWidth(line, "Courier", 10)
                x = (letter[0] - line_width) / 2
                c.drawString(x, y, line)
                y -= line_height

        
        self._log_debug(f"Created PDF with {len(lines)} lines, {len(text)} total chars")
        
        # Save the PDF
        c.save()
        packet.seek(0)
        
        # Create a new PDF with just our content
        new_pdf = PdfReader(packet)
        writer = PdfWriter()
        for page in new_pdf.pages:
            writer.add_page(page)
        
        # Save to a new buffer
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        
        return PdfReader(output)

    def _process_page(self, page: PageObject, encode: bool = True) -> bool:
        """Process a single page, either encoding or decoding its text."""
        try:
            # Extract text from page
            original_text = page.extract_text()
            if not original_text:
                raise ValueError("No text found in page")
                
            self._log_debug(f"Successfully extracted text ({len(original_text)} chars): {original_text[:100]}...")
            
            # Process the text
            if encode:
                processed_text = self._process_text(original_text)
            else:
                processed_text = self._process_text(original_text, encode=False)
                
            if not processed_text:
                raise ValueError("Processing resulted in empty text")
                
            if processed_text == original_text:
                raise ValueError("Processed text is identical to input")
                
            self._log_debug(f"Original text ({len(original_text)} chars): {original_text[:100]}...")
            self._log_debug(f"Processed text ({len(processed_text)} chars): {processed_text[:100]}...")
            
            # Create new page with processed text
            new_page = self._create_text_page(processed_text)
            if not new_page or len(new_page.pages) == 0:
                raise ValueError("Failed to create new page")
                
            # Verify text in created page
            created_text = new_page.pages[0].extract_text()
            if not created_text:
                raise ValueError("No text found in created page")
                
            self._log_debug(f"Verified text in created PDF: {created_text[:100]}...")
            
            # Replace page content with new page
            writer = PdfWriter()
            for page in new_page.pages:
                writer.add_page(page) 
            writer.add_page(page)
            
            # Save to a temporary buffer
            temp_buffer = io.BytesIO()
            writer.write(temp_buffer)
            temp_buffer.seek(0)
            
            # Create a new page with just our content
            new_pdf = PdfReader(temp_buffer)
            page.merge_page(new_pdf.pages[0])
            
            # Override text extraction to return only our content
            page._extract_text = page.extract_text
            page.extract_text = lambda *args, **kwargs: created_text
            
            return True
            
        except Exception as e:
            error_msg = f"Failed to process page: {str(e)}"
            self._log_debug(error_msg)
            self.errors.append(error_msg)
            return False
            
        def encode_pdf(self, input_path: str, output_path: str) -> bool:
            """
            Encode text in a PDF file using B-Cryptic encoding.
    
            Args:
                input_path: Path to input PDF
                output_path: Path to output PDF
        
            Returns:
                bool: True if successful
            """
            try:
                # Clear previous errors
                self.errors = []
        
                # Read input PDF
                reader = PdfReader(input_path)
                writer = PdfWriter()
        
                # Process each page
                success = True
                for page_num, page in enumerate(reader.pages):
                    try:
                        self._log_debug(f"Processing page {page_num + 1}")
                
                        # Extract and process text
                        original_text = page.extract_text()
                        if not original_text:
                            raise ValueError("No text found in page")
                    
                        processed_text = self._process_text(original_text)
                        if not processed_text:
                            raise ValueError("Processing resulted in empty text")
                    
                        # Create new page with processed text
                        new_page = self._create_text_page(processed_text)
                        if not new_page or len(new_page.pages) == 0:
                            raise ValueError("Failed to create new page")
                    
                        # Add all pages from the new generated PDF
                        for np in new_page.pages:
                            writer.add_page(np)
                    
                        self._log_debug(f"Successfully processed page {page_num + 1}")
                
                    except Exception as e:
                        error_msg = f"Error processing page {page_num + 1}: {str(e)}"
                        self._log_debug(error_msg)
                        self.errors.append(error_msg)
                        success = False
                        continue
                
                # Save output PDF
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
            
                # Verify output
                if not self._verify_output(input_path, output_path, encode=True):
                    raise ValueError("Output verification failed")
            
                return success
        
            except Exception as e:
                error_msg = f"Failed to encode PDF: {str(e)}"
                self._log_debug(error_msg)
                self.errors.append(error_msg)
                return False
            
    def decode_pdf(self, input_path: str, output_path: str) -> bool:
        """
        Decode a B-Cryptic encoded PDF back to original text.
        
        Args:
            input_path: Path to input PDF
            output_path: Path to output PDF
            
        Returns:
            bool: True if successful
        """
        try:
            # Clear previous errors
            self.errors = []
            
            # Read input PDF
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            # Process each page
            success = True
            for page_num, page in enumerate(reader.pages):
                try:
                    self._log_debug(f"Processing page {page_num + 1}")
                    
                    # Extract and process text
                    encoded_text = page.extract_text()
                    if not encoded_text:
                        raise ValueError("No text found in page")
                        
                    # Process text
                    decoded_text = self._process_text(encoded_text, encode=False)
                    if not decoded_text:
                        raise ValueError("Decoding failed")
                        
                    # Create new page with decoded text
                    new_page = self._create_text_page(decoded_text)
                    if not new_page or len(new_page.pages) == 0:
                        raise ValueError("Failed to create new page")
                        
                    # Add the new page
                    writer.add_page(new_page.pages[0])
                    self._log_debug(f"Successfully processed page {page_num + 1}")
                    
                except Exception as e:
                    error_msg = f"Error processing page {page_num + 1}: {str(e)}"
                    self._log_debug(error_msg)
                    self.errors.append(error_msg)
                    success = False
                    continue
                    
            # Save output PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
                
            # Verify output
            if not self._verify_output(input_path, output_path, encode=False):
                raise ValueError("Output verification failed")
                
            return success
            
        except Exception as e:
            error_msg = f"Failed to decode PDF: {str(e)}"
            self._log_debug(error_msg)
            self.errors.append(error_msg)
            return False
            
    def batch_process(self, input_dir: str, output_dir: str, mode: str = 'encode') -> Tuple[List[str], List[str]]:
        """
        Process multiple PDF files in a directory.
        
        Args:
            input_dir: Directory containing input PDF files
            output_dir: Directory to save processed PDF files
            mode: 'encode' or 'decode'
            
        Returns:
            tuple: (successful_files, failed_files)
        """
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
            
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        successful = []
        failed = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith('.pdf'):
                input_path = os.path.join(input_dir, filename)
                # Use correct naming convention without b_cryptic_ prefix
                prefix = "encoded_" if mode == 'encode' else "decoded_"
                output_filename = f"{prefix}{filename}"
                output_path = os.path.join(output_dir, output_filename)
                
                try:
                    self._log_debug(f"Processing file: {filename}")
                    if mode == 'encode':
                        success = self.encode_pdf(input_path, output_path)
                    else:
                        success = self.decode_pdf(input_path, output_path)
                        
                    if success:
                        successful.append(filename)
                        self._log_debug(f"Successfully processed: {filename}")
                    else:
                        failed.append(filename)
                        self._log_debug(f"Failed to process: {filename}")
                        
                except Exception as e:
                    error_msg = f"Error processing '{filename}': {str(e)}"
                    self._log_debug(error_msg)
                    self.errors.append(error_msg)
                    failed.append(filename)
                    
        return successful, failed
        
    def get_stats(self) -> Dict[str, any]:
        """Get processing statistics and errors."""
        return {
            'processed_files': self.processed_files,
            'total_pages': self.total_pages,
            'errors': self.errors
        }

    def _verify_output(self, input_path: str, output_path: str, encode: bool = True) -> bool:
        """
        Verify that the output PDF contains properly processed text.
        
        Args:
            input_path: Path to input PDF
            output_path: Path to output PDF
            encode: True if encoding, False if decoding
            
        Returns:
            bool: True if verification passes
        """
        import re  # Import at function start
        
        try:
            # Open both PDFs
            input_doc = PdfReader(input_path)
            output_doc = PdfReader(output_path)
            
            if len(input_doc.pages) != len(output_doc.pages):
                raise ValueError("Page count mismatch")
                
            # Check first page text
            input_text = input_doc.pages[0].extract_text().strip()
            output_text = output_doc.pages[0].extract_text().strip()
            
            if not output_text:
                raise ValueError("No text found in output PDF")
                
            # For encoding: verify output matches B-Cryptic pattern
            if encode:
                if input_text == output_text:
                    raise ValueError("Output text is identical to input text")
                    
                # Check for B-Cryptic markers
                if '[^' not in output_text and '[*' not in output_text and '[-' not in output_text:
                    raise ValueError("No B-Cryptic markers found in output")
                    
                # Count encoded blocks
                blocks = re.findall(r'\[[\^\*\-\+]?[0-9A-Za-z\-_]+\]', output_text)
                if not blocks:
                    raise ValueError("No valid B-Cryptic blocks found")
                    
                # Verify each block is in decoding table
                invalid_blocks = [b for b in blocks if b not in B_CRYPTIC_DECODING_TABLE]
                if invalid_blocks:
                    raise ValueError(f"Found {len(invalid_blocks)} invalid blocks")
                    
                self._log_debug(f"Verified encoded text with {len(blocks)} blocks")
                
            else:
                # For decoding: verify output is readable text
                # Check for any remaining B-Cryptic markers
                if re.search(r'\[[\^\*\-\+]?[0-9A-Za-z\-_]+\]', output_text):
                    raise ValueError("Decoded text contains B-Cryptic blocks")
                    
                # Check for any B-Cryptic special characters
                if any(c in output_text for c in ['[^', '[*', '[-', ']']):
                    raise ValueError("Decoded text contains B-Cryptic markers")
                    
                # Log text comparison
                self._log_debug(f"Input text ({len(input_text)} chars): {input_text[:100]}...")
                self._log_debug(f"Output text ({len(output_text)} chars): {output_text[:100]}...")
                
            self._log_debug("Output PDF verification successful")
            return True
            
        except Exception as e:
            error_msg = f"Output verification failed: {str(e)}"
            self._log_debug(error_msg)
            self.errors.append(error_msg)
            return False
