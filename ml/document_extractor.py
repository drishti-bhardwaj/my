import os
import io
import re
import tempfile
from pathlib import Path
from typing import Any, Dict, List

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None

try:
    import pytesseract
except ImportError:
    pytesseract = None

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".csv",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".xlsx",
    ".xls",
}


def is_binary_garbage(text: str) -> bool:
    """
    Check if a text string is actually raw binary file headers (PNG, JPEG, PDF)
    or corrupt non-printable control characters.
    """
    if not text:
        return False

    if text.startswith("\x89PNG") or text.startswith("%PDF") or text.startswith("\xff\xd8\xff"):
        return True

    upper_sample = text[:200].upper()
    if any(sig in upper_sample for sig in ["IHDR", "SRGB", "GAMA", "PHYS", "IDAT", "IEND", "JFIF"]):
        return True

    non_printable = sum(1 for c in text if ord(c) < 32 and c not in "\n\r\t")
    replacement_chars = text.count("\ufffd") + text.count("\x00")
    total_len = len(text)

    if total_len > 0 and (non_printable + replacement_chars) / float(total_len) > 0.15:
        return True

    return False


def clean_text(text: str) -> str:
    """
    Clean extracted OCR/PDF text while preserving
    engineering numbers and units.
    """
    if not text:
        return ""
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text_from_txt(file_path: str) -> str:
    path = Path(file_path)
    return clean_text(
        path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
    )


def extract_text_from_csv(file_path: str) -> str:
    path = Path(file_path)
    return clean_text(
        path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
    )


def setup_tesseract_cmd():
    """Locate Tesseract-OCR binary executable on Windows if present."""
    if not pytesseract:
        return
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"),
        os.path.expanduser(r"~\AppData\Local\Tesseract-OCR\tesseract.exe"),
        r"C:\tools\tesseract\tesseract.exe",
    ]
    for p in possible_paths:
        if os.path.exists(p):
            pytesseract.pytesseract.tesseract_cmd = p
            break

setup_tesseract_cmd()


def extract_text_from_image(file_path: str) -> str:
    """Extract all text visible in the uploaded image using native Windows OCR and PyTesseract engines."""
    text = ""
    
    # 1. Native Windows Media OCR Engine (WinOCR)
    if Image:
        try:
            import winocr
            img = Image.open(file_path)
            if img.mode != "RGB":
                img = img.convert("RGB")
            res = winocr.recognize_pil_sync(img)
            if isinstance(res, dict) and "text" in res:
                text = res["text"]
            elif hasattr(res, "text"):
                text = res.text
        except Exception:
            text = ""

    # 2. Try PyTesseract
    if not text and pytesseract and Image:
        try:
            image = Image.open(file_path)
            if image.mode != "RGB":
                image = image.convert("RGB")
            text = pytesseract.image_to_string(image)
        except Exception:
            text = ""

    # 3. Try RapidOCR if available
    if not text:
        try:
            from rapidocr_onnxruntime import RapidOCR
            engine = RapidOCR()
            result, _ = engine(file_path)
            if result:
                lines = [res[1] for res in result if res and len(res) > 1 and res[1]]
                if lines:
                    text = "\n".join(lines)
        except Exception:
            pass

    # 4. Fallback: PyMuPDF page text
    if not text and fitz:
        try:
            document = fitz.open(file_path)
            chunks = []
            for page in document:
                p_text = page.get_text()
                if p_text:
                    chunks.append(p_text)
            document.close()
            if chunks:
                text = "\n".join(chunks)
        except Exception:
            pass

    res = clean_text(text)
    return res if res else "No readable text detected from uploaded image."


def extract_text_from_pdf(file_path: str) -> str:
    """
    First attempt native PDF text extraction.
    If the PDF contains little/no text, render its pages
    and use OCR as a fallback for scanned documents.
    """
    native_chunks: List[str] = []

    if PdfReader:
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    native_chunks.append(text)
        except Exception:
            native_chunks = []

    native_text = clean_text("\n".join(native_chunks))
    if len(native_text) >= 40:
        return native_text

    # OCR fallback
    ocr_chunks: List[str] = []
    if fitz and pytesseract and Image:
        try:
            document = fitz.open(file_path)
            try:
                for page in document:
                    pixmap = page.get_pixmap(
                        matrix=fitz.Matrix(2, 2),
                        alpha=False,
                    )
                    image_bytes = pixmap.tobytes("png")
                    image = Image.open(io.BytesIO(image_bytes))
                    text = pytesseract.image_to_string(image)
                    if text:
                        ocr_chunks.append(text)
            finally:
                document.close()
        except Exception:
            pass

    ocr_text = clean_text("\n".join(ocr_chunks))
    return ocr_text or native_text


def extract_document_text(file_path: str) -> Dict[str, Any]:
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    if extension == ".txt":
        text = extract_text_from_txt(file_path)
    elif extension == ".csv":
        text = extract_text_from_csv(file_path)
    elif extension in {".png", ".jpg", ".jpeg"}:
        text = extract_text_from_image(file_path)
    elif extension == ".pdf":
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_txt(file_path)

    return {
        "filename": path.name,
        "extension": extension,
        "text": text,
        "character_count": len(text),
        "has_content": bool(text) and text != "No readable text detected from uploaded image.",
    }


def extract_document_text_from_bytes(raw_bytes: bytes, filename: str) -> Dict[str, Any]:
    """Process raw bytes safely using temporary file disk writing and native extractors."""
    import tempfile
    import os
    ext = "." + filename.rsplit(".", 1)[1].lower() if "." in filename else ".txt"
    if ext not in SUPPORTED_EXTENSIONS:
        ext = ".txt"

    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(raw_bytes)
        tmp_path = tmp.name

    try:
        res = extract_document_text(tmp_path)
        res["filename"] = filename
        return res
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass


# =========================================================
# ENGINEERING PARAMETER EXTRACTION
# =========================================================

def first_float(patterns: List[str], text: str):
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except (ValueError, TypeError):
                pass
    return None


def find_first(patterns: List[str], text: str):
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def detect_category(text: str) -> str:
    normalized = text.upper()
    if any(token in normalized for token in ["BALL VALVE", "BALL-VALVE"]):
        return "BALL_VALVE"
    if any(token in normalized for token in ["BEARING", "ROLLER BEARING", "BALL BEARING"]):
        return "BEARING"
    if any(token in normalized for token in ["PIPE", "SEAMLESS PIPE", "ERW PIPE"]):
        return "PIPE"
    if any(token in normalized for token in ["BOLT", "HEX BOLT", "HEXAGONAL BOLT"]):
        return "BOLT"
    if any(token in normalized for token in ["GASKET"]):
        return "GASKET"
    if any(token in normalized for token in ["FLANGE", "FLANGED"]):
        return "FLANGE"
    return "UNKNOWN"


def detect_material_grade(text: str):
    normalized = text.upper()
    grades = [
        "SS316L", "SS316", "SS304L", "SS304", "A105",
        "A182 F316", "A182 F304", "EN8", "EN19",
        "MONEL 400", "INCONEL 625",
    ]
    for grade in grades:
        if grade in normalized:
            return grade

    match = re.search(r"\bSS[\s-]?(\d{3,4}L?)\b", normalized)
    if match:
        return "SS" + match.group(1)
    return None


def detect_diameter(text: str):
    return first_float(
        [
            r"\bM\s*(\d+(?:\.\d+)?)\b",
            r"\bDIA(?:METER)?\s*[:=]?\s*(\d+(?:\.\d+)?)\s*MM\b",
            r"\bD\s*[:=]?\s*(\d+(?:\.\d+)?)\s*MM\b",
        ],
        text,
    )


def detect_length(text: str):
    return first_float(
        [
            r"\bX\s*(\d+(?:\.\d+)?)\s*MM\b",
            r"\bLENGTH\s*[:=]?\s*(\d+(?:\.\d+)?)\s*MM\b",
            r"\bL\s*[:=]?\s*(\d+(?:\.\d+)?)\s*MM\b",
        ],
        text,
    )


def detect_wall_thickness(text: str):
    return first_float(
        [
            r"\bWT\s*[:=]?\s*(\d+(?:\.\d+)?)\s*MM\b",
            r"\bWALL\s*THICKNESS\s*[:=]?\s*(\d+(?:\.\d+)?)\s*MM\b",
            r"\bTHK\s*[:=]?\s*(\d+(?:\.\d+)?)\s*MM\b",
        ],
        text,
    )


def detect_pressure(text: str):
    return first_float(
        [
            r"\b(\d+(?:\.\d+)?)\s*PSI\b",
            r"\bPRESSURE\s*[:=]?\s*(\d+(?:\.\d+)?)\s*PSI\b",
            r"\bCLASS\s*(\d+(?:\.\d+)?)\b",
        ],
        text,
    )


def detect_pipe_type(text: str):
    normalized = text.upper()
    if "SEAMLESS" in normalized:
        return "SEAMLESS"
    if "ERW" in normalized:
        return "ERW"
    if "WELDED" in normalized:
        return "WELDED"
    return None


def detect_connection_type(text: str):
    normalized = text.upper()
    if "FLANGED" in normalized:
        return "FLANGED"
    if "THREADED" in normalized:
        return "THREADED"
    if "SOCKET WELD" in normalized:
        return "SOCKET_WELD"
    if "BUTT WELD" in normalized:
        return "BUTT_WELD"
    return None


def detect_bearing_number(text: str):
    match = re.search(r"\b(\d{4,6}[A-Z]?)\b", text.upper())
    if match:
        return match.group(1)
    return None


def detect_seal_type(text: str):
    normalized = text.upper()
    for seal in ["2RS", "2RS1", "ZZ", "2Z", "OPEN", "SEALED"]:
        if seal in normalized:
            return seal
    return None


def extract_engineering_attributes(text: str) -> Dict[str, Any]:
    text = clean_text(text)
    category = detect_category(text)

    attributes: Dict[str, Any] = {
        "category": category,
        "material": detect_material_grade(text),
        "diameter_mm": detect_diameter(text),
        "length_mm": detect_length(text),
        "wall_thickness_mm": detect_wall_thickness(text),
        "pressure_rating_psi": detect_pressure(text),
        "connection_type": detect_connection_type(text),
        "pipe_type": detect_pipe_type(text),
        "bearing_number": detect_bearing_number(text) if category == "BEARING" else None,
        "seal_type": detect_seal_type(text) if category == "BEARING" else None,
    }

    return {k: v for k, v in attributes.items() if v is not None}


def build_extraction_result(file_path: str) -> Dict[str, Any]:
    document = extract_document_text(file_path)
    attributes = extract_engineering_attributes(document["text"])
    return {
        **document,
        "attributes": attributes,
    }