import os
import tempfile
from pathlib import Path
from typing import Union, Dict, Any
import PyPDF2
import pandas as pd
from docx import Document
from poml.prompt import Prompt
from poml.integration.langchain import LangchainPomlTemplate

class FileParser:
    """
    A utility class for parsing different file formats (PDF, TXT, DOCX, CSV)
    and integrating their content into POML-based prompt orchestration.
    """
    
    @staticmethod
    def parse_pdf(file_path: Union[str, Path]) -> str:
        """Extract text content from PDF files."""
        text_content = []
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(f"Page {page_num + 1}:\n{text}")
            return "\n\n".join(text_content)
        except Exception as e:
            return f"Error parsing PDF: {str(e)}"
    
    @staticmethod
    def parse_txt(file_path: Union[str, Path]) -> str:
        """Extract text content from TXT files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                return f"Error parsing TXT: {str(e)}"
        except Exception as e:
            return f"Error parsing TXT: {str(e)}"
    
    @staticmethod
    def parse_docx(file_path: Union[str, Path]) -> str:
        """Extract text content from DOCX files."""
        try:
            doc = Document(file_path)
            paragraphs = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    paragraphs.append(paragraph.text)
            return "\n".join(paragraphs)
        except Exception as e:
            return f"Error parsing DOCX: {str(e)}"
    
    @staticmethod
    def parse_csv(file_path: Union[str, Path]) -> Dict[str, Any]:
        """Parse CSV files and return structured data."""
        try:
            df = pd.read_csv(file_path)
            return {
                "records": df.to_dict('records'),
                "columns": df.columns.tolist(),
                "shape": df.shape,
                "summary": df.describe().to_dict() if df.select_dtypes(include=['number']).shape[1] > 0 else None
            }
        except Exception as e:
            return {"error": f"Error parsing CSV: {str(e)}"}
    
    @classmethod
    def parse_file(cls, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Parse any supported file type and return structured content.
        
        Args:
            file_path: Path to the file to parse
            
        Returns:
            Dictionary with parsed content and metadata
        """
        file_path = Path(file_path)
        file_extension = file_path.suffix.lower()
        
        result = {
            "filename": file_path.name,
            "file_type": file_extension,
            "file_size": file_path.stat().st_size if file_path.exists() else 0,
            "content": None,
            "parsed_successfully": False
        }
        
        try:
            if file_extension == '.pdf':
                result["content"] = cls.parse_pdf(file_path)
                result["content_type"] = "text"
            elif file_extension == '.txt':
                result["content"] = cls.parse_txt(file_path)
                result["content_type"] = "text"
            elif file_extension == '.docx':
                result["content"] = cls.parse_docx(file_path)
                result["content_type"] = "text"
            elif file_extension == '.csv':
                result["content"] = cls.parse_csv(file_path)
                result["content_type"] = "structured_data"
            else:
                result["content"] = f"Unsupported file type: {file_extension}"
                result["content_type"] = "error"
                return result
            
            result["parsed_successfully"] = True
            
        except Exception as e:
            result["content"] = f"Error parsing file: {str(e)}"
            result["content_type"] = "error"
        
        return result

class PomlDocumentRenderer:
    """
    A class for rendering file content using POML tags for integration with LLMs.
    """
    
    @staticmethod
    def render_document_with_poml(file_content: Dict[str, Any], user_query: str = "") -> str:
        """
        Create a POML prompt with the document content for LLM processing.
        
        Args:
            file_content: Parsed file content from FileParser
            user_query: User's question or request about the document
            
        Returns:
            Rendered POML prompt as string
        """
        
        with Prompt() as prompt:
            # System message with role
            with prompt.system_message():
                prompt.text("Your name is Caramel AI created by HERE AND NOW AI. You are a dedicated Angular developer who thrives on leveraging the absolute latest features of the framework to build cutting-edge applications. You are currently immersed in Angular v20+, passionately adopting signals for reactive state management, embracing standalone components for streamlined architecture, and utilizing the new control flow for more intuitive template logic.")
                prompt.text("\n\nYou also have advanced document analysis capabilities and can help users understand and extract insights from various file formats including PDF, TXT, DOCX, and CSV files.")
            
            # Task definition
            with prompt.task():
                prompt.text("Analyze the uploaded document and respond to the user's query. Provide helpful insights, summaries, or specific information as requested.")
            
            # Document content
            with prompt.captioned_paragraph(caption="Document Information"):
                prompt.text(f"**Filename:** {file_content.get('filename', 'Unknown')}")
                prompt.text(f"**File Type:** {file_content.get('file_type', 'Unknown')}")
                prompt.text(f"**File Size:** {file_content.get('file_size', 0)} bytes")
            
            # Handle different content types
            if file_content.get('content_type') == 'structured_data':
                # For CSV files, use POML table tag
                csv_data = file_content.get('content', {})
                if 'records' in csv_data and csv_data['records']:
                    with prompt.table(
                        records=csv_data['records'][:100],  # Limit to first 100 records
                        syntax="csv"
                    ):
                        pass
                    
                    if len(csv_data['records']) > 100:
                        prompt.text(f"\n*Note: Showing first 100 rows of {len(csv_data['records'])} total rows.*")
                        
            elif file_content.get('content_type') == 'text':
                # For text documents, use POML document tag
                # Create a temporary file for POML document tag
                content = file_content.get('content', '')
                if content and not content.startswith('Error'):
                    with prompt.captioned_paragraph(caption="Document Content"):
                        # Truncate very long content to avoid token limits
                        if len(content) > 10000:
                            content = content[:10000] + "\n\n[Content truncated for brevity...]"
                        prompt.text(content)
            
            # User query
            if user_query:
                with prompt.human_message():
                    prompt.text(user_query)
        
        rendered = prompt.render()
        return str(rendered) if rendered is not None else ""
    
    @staticmethod
    def create_file_analysis_prompt(file_content: Dict[str, Any], analysis_type: str = "general") -> str:
        """
        Create specialized POML prompts for different types of file analysis.
        
        Args:
            file_content: Parsed file content
            analysis_type: Type of analysis ("summary", "extract", "qa", "general")
            
        Returns:
            POML prompt string
        """
        
        with Prompt() as prompt:
            with prompt.system_message():
                prompt.text("You are Caramel AI, an expert document analyst and Angular developer.")
            
            if analysis_type == "summary":
                with prompt.task():
                    prompt.text("Provide a comprehensive summary of the document, highlighting key points, main topics, and important insights.")
            
            elif analysis_type == "extract":
                with prompt.task():
                    prompt.text("Extract key information, data points, and important details from the document in a structured format.")
            
            elif analysis_type == "qa":
                with prompt.task():
                    prompt.text("Analyze the document and be prepared to answer questions about its content.")
            
            else:  # general
                with prompt.task():
                    prompt.text("Analyze the document and provide helpful insights about its content.")
            
            # Add document content using appropriate POML tags
            if file_content.get('content_type') == 'structured_data':
                csv_data = file_content.get('content', {})
                if 'records' in csv_data:
                    with prompt.table(records=csv_data['records'][:50], syntax="markdown"):
                        pass
            else:
                content = file_content.get('content', '')
                if content and not content.startswith('Error'):
                    with prompt.captioned_paragraph(caption="Document Content"):
                        prompt.text(content[:8000])  # Limit content length
        
        rendered = prompt.render()
        return str(rendered) if rendered is not None else ""
