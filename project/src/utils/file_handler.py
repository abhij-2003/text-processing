import PyPDF2
import docx2txt

class FileHandler:
    @staticmethod
    def extract_text_from_file(file):
        """Extract text from various file formats"""
        try:
            if hasattr(file, 'name'):
                file_extension = file.name.split('.')[-1].lower()
                
                if file_extension == 'pdf':
                    pdf_reader = PyPDF2.PdfReader(file)
                    return ' '.join(page.extract_text() for page in pdf_reader.pages)
                    
                elif file_extension == 'txt':
                    return file.getvalue().decode('utf-8')
                    
                elif file_extension == 'docx':
                    return docx2txt.process(file)
                    
                else:
                    raise ValueError("Unsupported file type")
            else:
                raise ValueError("Invalid file object")
                
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")