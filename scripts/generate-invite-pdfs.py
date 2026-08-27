#!/usr/bin/env python3
"""Generate printable onboarding PDF invites (PT + EN) for WhatsApp / email sharing."""

from pathlib import Path

from fpdf import FPDF

SITE_URL = "https://luth3rmilla.github.io/yuki-fellipe-casamento/"
OUT_DIR = Path(__file__).resolve().parent.parent / "Convites"

BG = (243, 238, 233)
INK = (42, 36, 32)
GOLD = (154, 123, 79)
INK_SOFT = (92, 83, 76)


def spaced(text: str) -> str:
    return " ".join(text.upper())


INVITES = {
    "pt": {
        "filename": "OnBoard_CONVITE_YUKI-FELLIPE_PT.pdf",
        "month": "OUTUBRO",
        "year": "2 0 2 6",
        "weekday": "S E X T A",
        "day": "0 3",
        "blessing": "Com a bênção de Deus e das nossas famílias",
        "names": "Yuki & Fellipe",
        "invite_line1": "têm a honra de convidá-lo(a) ao seu",
        "invite_line2": "casamento a realizar-se aos",
        "date_full": "03 de Outubro de 2026",
        "ceremony": "Cerimônia religiosa e Copo d'Água · 14h",
        "venue": "Catembe Gallery Hotel · Maputo",
        "valid_for": "Convite válido para _____ pessoa(s)",
        "cta1": "Clique no botão abaixo para confirmar a sua presença",
        "cta2": "e obter mais informações!",
        "button": spaced("Abrir Convite"),
        "rsvp_note1": "Por favor, confirmar presença até o dia",
        "rsvp_note2": "03 de Outubro de 2026",
    },
    "en": {
        "filename": "OnBoard_CONVITE_YUKI-FELLIPE_EN.pdf",
        "month": "OCTOBER",
        "year": "2 0 2 6",
        "weekday": "F R I D A Y",
        "day": "0 3",
        "blessing": "With God's blessing and that of our families",
        "names": "Yuki & Fellipe",
        "invite_line1": "have the honour of inviting you to their",
        "invite_line2": "wedding on",
        "date_full": "October 3, 2026",
        "ceremony": "Religious ceremony & reception · 2:00 PM",
        "venue": "Catembe Gallery Hotel · Maputo",
        "valid_for": "Invitation valid for _____ guest(s)",
        "cta1": "Tap the button below to confirm your attendance",
        "cta2": "and see all the details!",
        "button": spaced("Open Invitation"),
        "rsvp_note1": "Please confirm your attendance by",
        "rsvp_note2": "October 3, 2026",
    },
}


class InvitePDF(FPDF):
    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=False)
        self.set_margins(22, 22, 22)


def center_text(pdf: InvitePDF, text: str, y: float, size: float = 11, style: str = "", color=INK):
    pdf.set_y(y)
    pdf.set_text_color(*color)
    pdf.set_font("Times", style, size)
    pdf.cell(0, size * 0.45, text, align="C", new_x="LMARGIN", new_y="NEXT")


def build_pdf(content: dict) -> InvitePDF:
    pdf = InvitePDF()
    pdf.add_page()
    pdf.set_fill_color(*BG)
    pdf.rect(0, 0, 210, 297, style="F")

    # Date header — spaced caps like reference PDF
    center_text(pdf, content["month"], 38, 13, "B")
    pdf.ln(2)
    pdf.set_font("Times", "", 11)
    pdf.set_text_color(*INK)
    pdf.cell(0, 5, content["year"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.set_font("Times", "B", 11)
    pdf.cell(0, 5, f'{content["weekday"]}   {content["day"]}', align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)
    center_text(pdf, content["blessing"], pdf.get_y(), 11)

    pdf.ln(8)
    center_text(pdf, content["names"], pdf.get_y(), 26, "I", GOLD)

    pdf.ln(6)
    center_text(pdf, content["invite_line1"], pdf.get_y(), 12)
    center_text(pdf, content["invite_line2"], pdf.get_y() + 2, 12)
    center_text(pdf, content["date_full"], pdf.get_y() + 2, 12, "B")

    pdf.ln(6)
    center_text(pdf, content["ceremony"], pdf.get_y(), 10, color=INK_SOFT)
    center_text(pdf, content["venue"], pdf.get_y() + 1, 10, color=INK_SOFT)

    pdf.ln(12)
    center_text(pdf, content["valid_for"], pdf.get_y(), 11)

    pdf.ln(10)
    center_text(pdf, content["cta1"], pdf.get_y(), 10)
    center_text(pdf, content["cta2"], pdf.get_y() + 1, 10)

    # Button with link
    pdf.ln(12)
    btn_w, btn_h = 118, 14
    btn_x = (210 - btn_w) / 2
    btn_y = pdf.get_y()
    pdf.set_draw_color(*INK)
    pdf.set_line_width(0.35)
    pdf.rect(btn_x, btn_y, btn_w, btn_h, style="D")
    pdf.link(btn_x, btn_y, btn_w, btn_h, SITE_URL)
    pdf.set_xy(btn_x, btn_y + 3.5)
    pdf.set_font("Times", "", 11)
    pdf.set_text_color(*INK)
    pdf.cell(btn_w, 6, content["button"], align="C")

    pdf.ln(16)
    center_text(pdf, content["rsvp_note1"], pdf.get_y() + 8, 9, color=INK_SOFT)
    center_text(pdf, content["rsvp_note2"], pdf.get_y() + 1, 9, "B", INK_SOFT)

    # URL at bottom
    pdf.ln(10)
    center_text(pdf, SITE_URL, pdf.get_y(), 8, color=GOLD)
    pdf.link(22, pdf.get_y() - 4, 166, 6, SITE_URL)

    return pdf


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for lang, content in INVITES.items():
        path = OUT_DIR / content["filename"]
        build_pdf(content).output(str(path))
        print(f"Created: {path}")


if __name__ == "__main__":
    main()
