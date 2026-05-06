# LEARNING.md — OCR Document Pipeline

Personal notes on what I built, what broke, and what I learned.

---

## What I Built

A 3-stage pipeline: preprocess image → extract text → parse structured fields.
Works on both images (JPG/PNG) and PDFs.

---

## Bugs I Fixed and Why

### 1. `clean_text` stripping `/`
```python
# Wrong — removes slashes
text = re.sub(r'[^\w\s.,$%-]', '', text)

# Fixed — keep slashes for date patterns
text = re.sub(r'[^\w\s.,$%\-/]', '', text)
```
Lesson: Text cleaning and regex extraction interact. Clean too aggressively and patterns break.

### 2. European price format
```python
# Wrong — only matches dot decimal
price_pattern = r'\$?\s?\b\d+\.\d{2}\b'

# Fixed — matches both comma and dot
price_pattern = r'\$?\s?\b\d+[\.,]\d{2}\b'
```
Lesson: Always test on real-world data. Assumed US format, invoice used EU format.

### 3. `pytesseract` couldn't find Tesseract
```python
# Fix — explicit path
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
```
Lesson: Tesseract is a system binary, not a Python package. PATH not always set in Codespaces.

---

## What the Regex Can and Cannot Do

| Field | Works | Limitation |
|---|---|---|
| Date | DD/MM/YYYY, Month DD YYYY | Misses unusual formats |
| Address | City, ST ZIP anchor | Only captures last line, not full address block |
| Products | Numbered line items | Depends on OCR preserving numbering |
| Prices | Both `.` and `,` decimals | Cannot distinguish price from quantity |
| Descriptions | Text before price | Catches noise words like "each" |

---

## Where Regex Fails — The Real Problem

Quantities (`3,00`) and prices (`209,00`) have identical format.
Regex has no concept of position/column in the document.

**Real solution:** LayoutLM — a transformer model trained on document images that understands both text AND spatial position. It would know that column 3 = quantity, column 5 = price.

This is Project 12/13 territory.

---

## Tesseract PSM Modes — What I Learned

| PSM | Use case |
|---|---|
| 3 | Fully automatic (default) |
| 6 | Uniform block of text — best for invoices |
| 11 | Sparse text, no specific order |

PSM 6 gave best results for structured invoices with clear layout.

---

## CLAHE vs Simple Histogram Equalization

Simple equalization applies same correction to whole image.
CLAHE (Contrast Limited Adaptive Histogram Equalization) works on small tiles — handles uneven lighting in phone-clicked documents much better.

`clipLimit=2.0, tileGridSize=(8,8)` — good defaults for A4 documents.

---

## Tools Used

| Tool | Purpose |
|---|---|
| `opencv-python-headless` | Image processing |
| `deskew` | Detect and correct skew angle |
| `pytesseract` | Python wrapper for Tesseract OCR |
| `pdf2image` | Convert PDF pages to PIL images |
| `pandas` | Handle structured OCR data output |
| `matplotlib` | Visualize preprocessing steps |
| `imageio` | Save demo frames |

---

## What's Next

- **LayoutLM / Donut** — document understanding with spatial awareness
- **Named Entity Recognition** — extract entities without rigid regex patterns
- **Table extraction** — Tesseract struggles with multi-column tables; `camelot` or `pdfplumber` handle this better
- **Confidence-based fallback** — if avg confidence < threshold, try different PSM mode automatically