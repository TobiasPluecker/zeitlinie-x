import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

def build_pdf(filename="episodes/ep01_dunkirk_1940/script_de.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=1.8*cm,
        leftMargin=1.8*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )

    styles = getSampleStyleSheet()
    
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        alignment=0
    )
    
    sub_style = ParagraphStyle(
        'SubStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#64748B'),
    )

    badge_style = ParagraphStyle(
        'BadgeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#B45309'),
    )

    scene_title_style = ParagraphStyle(
        'SceneTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1E293B'),
    )

    text_style = ParagraphStyle(
        'SpeakText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12.5,
        leading=18,
        textColor=colors.HexColor('#0F172A'),
    )

    cue_style = ParagraphStyle(
        'CueStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#64748B'),
    )

    story = []

    # Header
    story.append(Paragraph("ZEITLINIE X | @zeitlinie_x", badge_style))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("Sprecherskript: Folge 01 - Dünkirchen 1940", header_style))
    story.append(Paragraph("Thema: Was, wenn Dünkirchen gescheitert wäre? | Format: TikTok 9:16 (ca. 70s)", sub_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#CBD5E1'), spaceBefore=3, spaceAfter=10))

    # Recording Tips Box
    tip_text = (
        "<b>Aufnahme-Tipps:</b> Starte direkt mit maximaler Energie beim Hook! "
        "Sprich danach ruhig, tief und mit spürbarem Ernst. "
        "Lass Pausen (z. B. bei <b>[...]</b>) ganz bewusst ca. 0,8 Sekunden stehen. "
        "Wenn du dich verhaspelst: einfach Satz neu ansetzen, wir schneiden es später!"
    )
    tip_p = Paragraph(tip_text, ParagraphStyle('Tip', parent=styles['Normal'], fontSize=9.5, leading=14, textColor=colors.HexColor('#1E3A8A')))
    tip_table = Table([[tip_p]], colWidths=[17.4*cm])
    tip_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93C5FD')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(tip_table)
    story.append(Spacer(1, 0.4*cm))

    # Scenes with Hook A
    scenes = [
        (
            "[00:00 - 00:04] Szene 1: Der Provokations-Hook",
            "Text groß im Bild: „Der Tag, an dem Hitler fast gewann“ + brennende Küste",
            "„Es gab einen einzigen Tag, an dem Hitler fast den gesamten Zweiten Weltkrieg gewonnen hätte.“"
        ),
        (
            "[00:04 - 00:10] Szene 2: Die Falle von Dünkirchen",
            "Taktische Kesselkarte: 300.000 Soldaten am Strand, Panzer stoppen plötzlich",
            "„Dünkirchen, Mai 1940. Über 300.000 britische Soldaten sitzen in der Falle. Mit dem Rücken zum Meer. Hitlers Panzer stehen wenige Kilometer entfernt – und stoppen plötzlich für 48 Stunden. Ein Wunder: 330.000 Männer entkommen.“"
        ),
        (
            "[00:10 - 00:15] Szene 3: Der Zeitlinien-Bruch (Zeitlinie X)",
            "Zeitsprung-Effekt, Zeitlinie spaltet sich in Rot/Gold",
            "„Doch was passiert in Zeitlinie X? [...] Was, wenn dieser Haltebefehl niemals erteilt worden wäre?“"
        ),
        (
            "[00:15 - 00:26] Szene 4: Vernichtung des Expeditionskorps",
            "Panzer brechen durch, Stuka-Angriffe, Zerstörung am Strand",
            "„Innerhalb von nur 72 Stunden wäre das gesamte britische Expeditionskorps vernichtet oder gefangen genommen worden. Die gesamte kampffähige Berufsarmee Großbritanniens: ausgelöscht.“"
        ),
        (
            "[00:26 - 00:38] Szene 5: Panik & Krise in London",
            "Downing Street No. 10 im Regen, zerstrittenes Parlament, Churchill isoliert",
            "„In London bricht die Regierung zusammen. Winston Churchill verliert seinen Rückhalt – Friedensbefürworter übernehmen das Ruder. Ohne Armee steht England vor der Wahl: Kapitulation oder ein demütigender Frieden.“"
        ),
        (
            "[00:38 - 00:50] Szene 6: Waffenstillstand & Blick nach Osten",
            "Karte färbt sich rot, massive Truppenverlegungen per Zug nach Osten",
            "„Großbritannien scheidet 1940 aus dem Krieg aus. Keine Luftschlacht um England. Keine Landung in der Normandie 1944. Und als 1941 der Angriff auf die Sowjetunion beginnt, existiert keine zweite Front im Westen.“"
        ),
        (
            "[00:50 - 01:02] Szene 7: Das veränderte Schicksal der Welt",
            "Dunkle Weltkarte, Moskau unter Belagerung, isolierte USA",
            "„Die gesamte industrielle und militärische Macht der Achsenmächte konzentriert sich auf ein einziges Ziel: Moskau. Die USA bleiben isoliert. Die Geschichte unserer Welt wäre für immer eine andere.“"
        ),
        (
            "[01:02 - 01:12] Szene 8: Call to Action",
            "Zeitlinie X Logo & Frage-Sticker",
            "„Hätte England trotzdem weitergekämpft? Schreib deine Theorie in die Kommentare – und folge Zeitlinie X für mehr alternative Geschichte.“"
        ),
    ]

    for title, cue, text in scenes:
        cell_data = [
            [Paragraph(f"<b>{title}</b>", scene_title_style)],
            [Paragraph(f"<i>Visuell: {cue}</i>", cue_style)],
            [Spacer(1, 0.1*cm)],
            [Paragraph(f"<b>Sprechtext:</b><br/>{text}", text_style)]
        ]
        scene_table = Table(cell_data, colWidths=[17.4*cm])
        scene_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('PADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,-1), (-1,-1), 8),
        ]))
        story.append(scene_table)
        story.append(Spacer(1, 0.2*cm))

    doc.build(story)
    print(f"PDF successfully built: {filename}")

if __name__ == "__main__":
    build_pdf()
