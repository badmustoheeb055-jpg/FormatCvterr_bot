import os
import subprocess
from pdf2docx import Converter

def convert_to_docx(pdf_path):
    """
    Convert PDF to DOCX using pdf2docx library
    """
    try:
        # Generate output filename
        output_path = pdf_path.rsplit('.', 1)[0] + '.docx'
        
        # Convert PDF to DOCX
        cv = Converter(pdf_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()
        
        return output_path
    except Exception as e:
        raise Exception(f"Error converting PDF to DOCX: {str(e)}")

def convert_to_pdf(input_path):
    """
    Convert various document formats to PDF using LibreOffice
    Supports: .doc, .docx, .odt, .txt, .rtf, .html, .xls, .xlsx, .ods, .csv, .ppt, .pptx, .odp
    """
    try:
        # Generate output filename
        output_path = input_path.rsplit('.', 1)[0] + '.pdf'
        
        # Use LibreOffice in headless mode
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(input_path),
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"LibreOffice error: {result.stderr}")
        
        return output_path
    except FileNotFoundError:
        raise Exception("LibreOffice is not installed on the system")
    except Exception as e:
        raise Exception(f"Error converting to PDF: {str(e)}")

def convertir_ppt_to_pdf_linux(ppt_path):
    """
    Specifically convert PowerPoint files to PDF on Linux
    Uses LibreOffice with additional options for better PowerPoint compatibility
    """
    try:
        output_path = ppt_path.rsplit('.', 1)[0] + '.pdf'
        
        # More specific command for PowerPoint
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(ppt_path),
            '--norestore',
            '--nologo',
            '--nodefault',
            '--nofirststartwizard',
            ppt_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"LibreOffice error: {result.stderr}")
        
        return output_path
    except FileNotFoundError:
        raise Exception("LibreOffice is not installed on the system")
    except Exception as e:
        raise Exception(f"Error converting PowerPoint to PDF: {str(e)}")

def get_file_size(file_path):
    """Get file size in MB"""
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)

def cleanup_temp_files(file_paths):
    """Remove temporary files"""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
