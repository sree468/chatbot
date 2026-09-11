from fpdf import FPDF

def create_pdf(question: str, answer: str, language: str) -> bytes:
    """Generates a downloadable PDF report."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Document Header
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"Gemini AI Query Report ({language})", ln=True)
    pdf.ln(4)
    
    # Prompt Section
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "User Question:", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, question.encode("latin-1", "replace").decode("latin-1"))
    pdf.ln(4)
    
    # Response Section
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"Response ({language}):", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, answer.encode("latin-1", "replace").decode("latin-1"))
    
    return bytes(pdf.output())