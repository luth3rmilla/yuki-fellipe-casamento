#!/usr/bin/env python3
"""Generate onboarding PDF invites — 2 per language (1 guest + 2 guests)."""

from pathlib import Path

from fpdf import FPDF

SITE_URL = "https://luth3rmilla.github.io/yuki-fellipe-casamento/"
OUT_DIR = Path(__file__).resolve().parent.parent / "Convites"
FONTS_DIR = Path(__file__).resolve().parent / "fonts"

BG = (243, 238, 233)
INK = (42, 36, 32)
GOLD = (154, 123, 79)
INK_SOFT = (92, 83, 76)

# Fallback paths for Chinese / Unicode on macOS
UNICODE_FONT_CANDIDATES = [
    FONTS_DIR / "NotoSansSC-Regular.ttf",
    Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
    Path("/Library/Fonts/Arial Unicode.ttf"),
]


def spaced(text: str) -> str:
    return " ".join(text.upper())


LANGS = {
    "pt": {
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
        "valid_one": "Convite válido para 1 pessoa",
        "valid_two": "Convite válido para 2 pessoas",
        "cta1": "Clique no botão abaixo para confirmar a sua presença",
        "cta2": "e obter mais informações!",
        "button": spaced("Abrir Convite"),
        "rsvp_note1": "Por favor, confirmar presença até o dia",
        "rsvp_note2": "03 de Outubro de 2026",
        "file_one": "OnBoard_CONVITE_YUKI-FELLIPE_PT_1pessoa.pdf",
        "file_two": "OnBoard_CONVITE_YUKI-FELLIPE_PT_2pessoas.pdf",
        "unicode": False,
    },
    "en": {
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
        "valid_one": "Invitation valid for 1 guest",
        "valid_two": "Invitation valid for 2 guests",
        "cta1": "Tap the button below to confirm your attendance",
        "cta2": "and see all the details!",
        "button": spaced("Open Invitation"),
        "rsvp_note1": "Please confirm your attendance by",
        "rsvp_note2": "October 3, 2026",
        "file_one": "OnBoard_CONVITE_YUKI-FELLIPE_EN_1guest.pdf",
        "file_two": "OnBoard_CONVITE_YUKI-FELLIPE_EN_2guests.pdf",
        "unicode": False,
    },
    "zh": {
        "month": "十月",
        "year": "2 0 2 6",
        "weekday": "星 期 五",
        "day": "0 3",
        "blessing": "承蒙上帝与双方家人祝福",
        "names": "Yuki & Fellipe",
        "invite_line1": "Yuki 与 Fellipe 诚挚邀请您",
        "invite_line2": "出席婚礼 ·",
        "date_full": "2026年10月3日",
        "ceremony": "宗教仪式与喜宴 · 下午2时",
        "venue": "Catembe Gallery Hotel · 马普托",
        "valid_one": "本请柬限 1 位宾客",
        "valid_two": "本请柬限 2 位宾客",
        "cta1": "请点击下方按钮确认出席",
        "cta2": "并查看婚礼详情！",
        "button": "打 开 请 柬",
        "rsvp_note1": "请于以下日期前确认出席",
        "rsvp_note2": "2026年10月3日",
        "file_one": "OnBoard_CONVITE_YUKI-FELLIPE_ZH_1guest.pdf",
        "file_two": "OnBoard_CONVITE_YUKI-FELLIPE_ZH_2guests.pdf",
        "unicode": True,
    },
}


class InvitePDF(FPDF):
    def __init__(self, use_unicode: bool = False):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=False)
        self.set_margins(22, 22, 22)
        self.use_unicode = use_unicode
        self.body_font = "Times"
        if use_unicode:
            font_path = next((p for p in UNICODE_FONT_CANDIDATES if p.exists()), None)
            if not font_path:
                raise FileNotFoundError(
                    "Chinese font not found. Place NotoSansSC-Regular.ttf in scripts/fonts/"
                )
            self.add_font("WeddingUnicode", fname=str(font_path))
            self.body_font = "WeddingUnicode"


def center_text(
    pdf: InvitePDF,
    text: str,
    y: float,
    size: float = 11,
    style: str = "",
    color=INK,
):
    pdf.set_y(y)
    pdf.set_text_color(*color)
    if pdf.use_unicode:
        pdf.set_font(pdf.body_font, size=size)
    else:
        pdf.set_font("Times", style, size)
    pdf.cell(0, size * 0.45, text, align="C", new_x="LMARGIN", new_y="NEXT")


def build_pdf(content: dict, use_unicode: bool) -> InvitePDF:
    pdf = InvitePDF(use_unicode=use_unicode)
    pdf.add_page()
    pdf.set_fill_color(*BG)
    pdf.rect(0, 0, 210, 297, style="F")

    center_text(pdf, content["month"], 38, 13 if not use_unicode else 12, "B" if not use_unicode else "")
    pdf.ln(2)
    if pdf.use_unicode:
        pdf.set_font(pdf.body_font, size=11)
    else:
        pdf.set_font("Times", "", 11)
    pdf.set_text_color(*INK)
    pdf.cell(0, 5, content["year"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    if pdf.use_unicode:
        pdf.set_font(pdf.body_font, size=11)
    else:
        pdf.set_font("Times", "B", 11)
    pdf.cell(0, 5, f'{content["weekday"]}   {content["day"]}', align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)
    center_text(pdf, content["blessing"], pdf.get_y(), 11)

    pdf.ln(8)
    center_text(pdf, content["names"], pdf.get_y(), 26 if not use_unicode else 22, "I" if not use_unicode else "", GOLD)

    pdf.ln(6)
    center_text(pdf, content["invite_line1"], pdf.get_y(), 12)
    center_text(pdf, content["invite_line2"], pdf.get_y() + 2, 12)
    center_text(pdf, content["date_full"], pdf.get_y() + 2, 12, "B" if not use_unicode else "")

    pdf.ln(6)
    center_text(pdf, content["ceremony"], pdf.get_y(), 10, color=INK_SOFT)
    center_text(pdf, content["venue"], pdf.get_y() + 1, 10, color=INK_SOFT)

    pdf.ln(12)
    center_text(pdf, content["valid_for"], pdf.get_y(), 11, "B" if not use_unicode else "")

    pdf.ln(10)
    center_text(pdf, content["cta1"], pdf.get_y(), 10)
    center_text(pdf, content["cta2"], pdf.get_y() + 1, 10)

    pdf.ln(12)
    btn_w, btn_h = 118, 14
    btn_x = (210 - btn_w) / 2
    btn_y = pdf.get_y()
    pdf.set_draw_color(*INK)
    pdf.set_line_width(0.35)
    pdf.rect(btn_x, btn_y, btn_w, btn_h, style="D")
    pdf.link(btn_x, btn_y, btn_w, btn_h, SITE_URL)
    pdf.set_xy(btn_x, btn_y + 3.5)
    if pdf.use_unicode:
        pdf.set_font(pdf.body_font, size=11)
    else:
        pdf.set_font("Times", "", 11)
    pdf.set_text_color(*INK)
    pdf.cell(btn_w, 6, content["button"], align="C")

    pdf.ln(16)
    center_text(pdf, content["rsvp_note1"], pdf.get_y() + 8, 9, color=INK_SOFT)
    center_text(pdf, content["rsvp_note2"], pdf.get_y() + 1, 9, "B" if not use_unicode else "", INK_SOFT)

    pdf.ln(10)
    center_text(pdf, SITE_URL, pdf.get_y(), 8, color=GOLD)
    pdf.link(22, pdf.get_y() - 4, 166, 6, SITE_URL)

    return pdf


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Remove old single-version PDFs
    for old in (
        "OnBoard_CONVITE_YUKI-FELLIPE_PT.pdf",
        "OnBoard_CONVITE_YUKI-FELLIPE_EN.pdf",
    ):
        old_path = OUT_DIR / old
        if old_path.exists():
            old_path.unlink()
            print(f"Removed old: {old_path}")

    for lang_key, lang in LANGS.items():
        for guests, file_key, valid_key in (
            (1, "file_one", "valid_one"),
            (2, "file_two", "valid_two"),
        ):
            content = {**lang, "valid_for": lang[valid_key]}
            path = OUT_DIR / lang[file_key]
            build_pdf(content, use_unicode=lang["unicode"]).output(str(path))
            print(f"Created ({lang_key}, {guests} guest(s)): {path}")


if __name__ == "__main__":
    main()
