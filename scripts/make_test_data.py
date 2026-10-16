"""Draw the synthetic documents used by the showcase.

The pages are fictional. Every value printed here is also in
test_data/ground_truth.json. Re-run this script from the repo root after
editing a figure, then check the images before you trust the ground truth.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "test_data"

ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
COURIER = "/System/Library/Fonts/Supplemental/Courier New.ttf"
COURIER_BOLD = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"

INK = (28, 32, 30)
MUTED = (90, 98, 94)
LINE = (214, 220, 216)
GREEN = (28, 74, 48)
GREEN_SOFT = (236, 244, 236)
PAPER = (255, 255, 255)
RECEIPT_PAPER = (247, 243, 234)


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, face: ImageFont.FreeTypeFont, fill=INK) -> None:
    draw.text(xy, value, font=face, fill=fill)


def ground_truth() -> dict:
    return {
        "invoice": {
            "file": "invoice.png",
            "document_type": "tax_invoice",
            "vendor": "HARBOUR & CO. SUPPLIES",
            "vendor_vat": "4780123456",
            "invoice_number": "INV-20418",
            "invoice_date": "2026-03-12",
            "due_date": "2026-04-11",
            "purchase_order": "PO-7781",
            "currency": "ZAR",
            "bill_to": "Northwind Field Office",
            "line_items": [
                {
                    "sku": "NB-440",
                    "description": "Field notebook",
                    "quantity": 24,
                    "unit_price": 18.50,
                    "amount": 444.00,
                },
                {
                    "sku": "PL-12",
                    "description": "Plotter pen, black",
                    "quantity": 6,
                    "unit_price": 42.00,
                    "amount": 252.00,
                },
            ],
            "subtotal": 696.00,
            "vat_rate": 0.15,
            "vat_amount": 104.40,
            "total": 800.40,
        },
        "receipt": {
            "file": "receipt.png",
            "merchant": "KLOOF MARKET",
            "vat_number": "4099887766",
            "receipt_number": "R-19042",
            "sold_at": "2026-10-03T14:22:00",
            "currency": "ZAR",
            "line_items": [
                {"description": "Milk 2 L", "amount": 32.99},
                {"description": "Brown bread", "amount": 18.50},
                {"description": "Coffee 250 g", "amount": 89.00},
            ],
            "total": 140.49,
            "vat_included": 18.32,
            "tender": "card",
        },
        "return_request": {
            "file": "return_request.png",
            "customer": "Amina Naidoo",
            "order_number": "ORD-55210",
            "sku": "FJ-200",
            "description": "Field jacket",
            "category": "apparel",
            "purchase_date": "2026-09-20",
            "request_date": "2026-10-14",
            "reason": "Seam split at the left shoulder",
            "condition": "defective",
            "expected_decision": {
                "eligible": True,
                "days_since_purchase": 24,
                "policy_window_days": 30,
                "category": "apparel",
            },
        },
    }


def policies() -> dict:
    return {
        "apparel": {
            "window_days": 30,
            "defective_covered": True,
            "rule": "Apparel may be returned within 30 days of the purchase date. A defective item is accepted inside that window.",
        },
        "electronics": {
            "window_days": 14,
            "defective_covered": True,
            "rule": "Electronics may be returned within 14 days of the purchase date if unopened, or within 14 days if defective.",
        },
        "office": {
            "window_days": 7,
            "defective_covered": False,
            "rule": "Office supplies may be returned within 7 days of the purchase date if unopened. Defective office supplies are replaced by the maker, not refunded here.",
        },
    }


def draw_invoice() -> Image.Image:
    image = Image.new("RGB", (1240, 1680), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1240, 196), fill=GREEN)
    text(draw, (72, 48), "HARBOUR & CO. SUPPLIES", font(ARIAL_BOLD, 42), (255, 255, 255))
    text(draw, (72, 108), "14 Quay Street, Cape Town, 8001", font(ARIAL, 24), (214, 228, 216))
    text(draw, (72, 144), "VAT 4780123456", font(ARIAL, 24), (214, 228, 216))
    text(draw, (860, 56), "TAX INVOICE", font(ARIAL_BOLD, 36), (186, 214, 96))
    text(draw, (860, 112), "INV-20418", font(ARIAL_BOLD, 32), (255, 255, 255))

    draw.rounded_rectangle((56, 228, 1184, 430), radius=16, fill=GREEN_SOFT)
    text(draw, (80, 252), "Invoice date", font(ARIAL, 20), MUTED)
    text(draw, (80, 284), "12 March 2026", font(ARIAL_BOLD, 28))
    text(draw, (80, 340), "Due date", font(ARIAL, 20), MUTED)
    text(draw, (80, 372), "11 April 2026", font(ARIAL_BOLD, 28))
    text(draw, (460, 252), "Purchase order", font(ARIAL, 20), MUTED)
    text(draw, (460, 284), "PO-7781", font(ARIAL_BOLD, 28))
    text(draw, (460, 340), "Currency", font(ARIAL, 20), MUTED)
    text(draw, (460, 372), "ZAR", font(ARIAL_BOLD, 28))
    text(draw, (780, 252), "Bill to", font(ARIAL, 20), MUTED)
    text(draw, (780, 284), "Northwind Field Office", font(ARIAL_BOLD, 28))
    text(draw, (780, 340), "Address", font(ARIAL, 20), MUTED)
    text(draw, (780, 372), "88 Signal Road, Johannesburg", font(ARIAL, 26))

    headers = [("SKU", 80), ("Description", 250), ("Qty", 760), ("Unit price", 900), ("Amount", 1080)]
    table_top = 490
    draw.rectangle((56, table_top, 1184, table_top + 64), fill=GREEN)
    for label, x in headers:
        text(draw, (x, table_top + 16), label, font(ARIAL_BOLD, 22), (255, 255, 255))

    items = [
        ("NB-440", "Field notebook", "24", "18.50", "444.00"),
        ("PL-12", "Plotter pen, black", "6", "42.00", "252.00"),
    ]
    y = table_top + 64
    for index, item in enumerate(items):
        fill = (248, 250, 248) if index % 2 == 0 else PAPER
        draw.rectangle((56, y, 1184, y + 84), fill=fill)
        xs = [80, 250, 760, 900, 1080]
        for value, x in zip(item, xs):
            text(draw, (x, y + 26), value, font(ARIAL, 26))
        y += 84
    draw.rectangle((56, table_top, 1184, y), outline=LINE, width=2)

    totals = [
        ("Subtotal", "696.00", False),
        ("VAT 15%", "104.40", False),
        ("Total ZAR", "800.40", True),
    ]
    y += 36
    for label, amount, strong in totals:
        if strong:
            draw.rounded_rectangle((760, y - 8, 1184, y + 64), radius=10, fill=GREEN)
            text(draw, (788, y + 8), label, font(ARIAL_BOLD, 28), (255, 255, 255))
            text(draw, (1040, y + 8), amount, font(ARIAL_BOLD, 28), (186, 214, 96))
        else:
            text(draw, (788, y), label, font(ARIAL, 26), MUTED)
            text(draw, (1040, y), amount, font(ARIAL_BOLD, 26))
        y += 72

    text(draw, (72, 1500), "Payable by EFT. Quote INV-20418 as the payment reference.", font(ARIAL, 24), MUTED)
    text(draw, (72, 1552), "This is a synthetic invoice for a document-intelligence demo.", font(ARIAL, 20), MUTED)
    return image


def draw_receipt() -> Image.Image:
    image = Image.new("RGB", (720, 1280), RECEIPT_PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((36, 36, 684, 1244), outline=(190, 176, 150), width=3)
    text(draw, (150, 80), "KLOOF MARKET", font(COURIER_BOLD, 42))
    text(draw, (150, 140), "12 Vine Lane", font(COURIER, 26), MUTED)
    text(draw, (128, 178), "Durban, 4001", font(COURIER, 26), MUTED)
    text(draw, (116, 230), "VAT 4099887766", font(COURIER, 26))
    draw.line((80, 290, 640, 290), fill=(190, 176, 150), width=2)
    text(draw, (90, 320), "03 Oct 2026  14:22", font(COURIER, 28))
    text(draw, (90, 368), "Till 4", font(COURIER, 28))
    text(draw, (360, 368), "Receipt R-19042", font(COURIER_BOLD, 28))
    draw.line((80, 430, 640, 430), fill=(190, 176, 150), width=2)

    lines = [
        ("Milk 2 L", "32.99"),
        ("Brown bread", "18.50"),
        ("Coffee 250 g", "89.00"),
    ]
    y = 470
    for description, amount in lines:
        text(draw, (90, y), description, font(COURIER, 30))
        text(draw, (500, y), amount, font(COURIER, 30))
        y += 64
    draw.line((80, y + 10, 640, y + 10), fill=(190, 176, 150), width=2)
    y += 40
    text(draw, (90, y), "TOTAL ZAR", font(COURIER_BOLD, 34))
    text(draw, (460, y), "140.49", font(COURIER_BOLD, 34))
    y += 70
    text(draw, (90, y), "VAT included 15%", font(COURIER, 26), MUTED)
    text(draw, (470, y), "18.32", font(COURIER, 26), MUTED)
    y += 64
    text(draw, (90, y), "Tender", font(COURIER, 28))
    text(draw, (500, y), "CARD", font(COURIER_BOLD, 28))
    y += 90
    text(draw, (170, y), "Thank you", font(COURIER, 28), MUTED)
    text(draw, (110, 1160), "Synthetic receipt. Not a real sale.", font(COURIER, 22), MUTED)
    return image


def field(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, value: str, width: int) -> None:
    text(draw, (x, y), label, font(ARIAL, 20), MUTED)
    draw.rounded_rectangle((x, y + 34, x + width, y + 108), radius=10, outline=LINE, width=2, fill=(252, 253, 252))
    text(draw, (x + 20, y + 54), value, font(ARIAL_BOLD, 28))


def draw_return_request() -> Image.Image:
    image = Image.new("RGB", (1240, 1560), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1240, 150), fill=GREEN)
    text(draw, (72, 36), "NORTHWIND RETURNS", font(ARIAL_BOLD, 40), (255, 255, 255))
    text(draw, (72, 96), "Return request", font(ARIAL, 24), (214, 228, 216))
    text(draw, (860, 52), "14 October 2026", font(ARIAL_BOLD, 28), (255, 255, 255))

    field(draw, 72, 200, "Customer", "Amina Naidoo", 520)
    field(draw, 640, 200, "Order number", "ORD-55210", 520)
    field(draw, 72, 360, "SKU", "FJ-200", 250)
    field(draw, 360, 360, "Item", "Field jacket", 400)
    field(draw, 800, 360, "Category", "Apparel", 360)
    field(draw, 72, 520, "Purchase date", "20 September 2026", 520)
    field(draw, 640, 520, "Request date", "14 October 2026", 520)
    field(draw, 72, 680, "Reason", "Seam split at the left shoulder", 1088)
    field(draw, 72, 840, "Condition", "Defective", 520)

    draw.rounded_rectangle((72, 1020, 1168, 1280), radius=16, fill=GREEN_SOFT)
    text(draw, (100, 1052), "Desk instruction", font(ARIAL_BOLD, 24), GREEN)
    text(draw, (100, 1104), "Read the category on this form. Look up the return rule", font(ARIAL, 26))
    text(draw, (100, 1144), "for that category before deciding. Days since purchase", font(ARIAL, 26))
    text(draw, (100, 1184), "is the request date minus the purchase date.", font(ARIAL, 26))
    text(draw, (72, 1380), "Synthetic return form. The policy is not printed on this page.", font(ARIAL, 22), MUTED)
    return image


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    draw_invoice().save(OUT / "invoice.png", "PNG")
    draw_receipt().save(OUT / "receipt.png", "PNG")
    draw_return_request().save(OUT / "return_request.png", "PNG")
    (OUT / "ground_truth.json").write_text(json.dumps(ground_truth(), indent=2) + "\n")
    (OUT / "policies.json").write_text(json.dumps(policies(), indent=2) + "\n")
    print(f"wrote fixtures in {OUT}")


if __name__ == "__main__":
    main()
