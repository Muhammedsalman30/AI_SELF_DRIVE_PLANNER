import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


def generate_itinerary_pdf(itinerary):

    # Create output folder in project root
    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    output_folder = os.path.join(project_dir, "generated_reports")
    os.makedirs(output_folder, exist_ok=True)

    customer_name = itinerary["customer"]["name"]

    safe_name = "".join(
        character for character in customer_name
        if character.isalnum() or character in ("_", "-")
    )

    filename = f"{safe_name}_Travel_Itinerary.pdf"

    pdf_path = os.path.join(output_folder, filename)

    # Create PDF document
    document = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        alignment=1,
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=12,
        spaceAfter=8
    )

    normal_style = styles["BodyText"]

    story = []

    # Title
    story.append(
        Paragraph("EUROPE SELF-DRIVE TRAVEL ITINERARY", title_style)
    )

    story.append(Spacer(1, 10))

    # Customer details
    story.append(
        Paragraph("1. CUSTOMER DETAILS", heading_style)
    )

    customer = itinerary["customer"]

    customer_data = [
        ["Customer Name", customer["name"]],
        ["Number of Travellers", str(customer["travellers"])],
        ["Travel Days", str(itinerary["travel_days"])],
        ["Travel Budget", str(customer["budget"])]
    ]

    customer_table = Table(customer_data, colWidths=[6 * cm, 10 * cm])

    customer_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 7)
    ]))

    story.append(customer_table)

    # Starting location
    story.append(
        Paragraph("2. STARTING LOCATION", heading_style)
    )

    story.append(
        Paragraph(
            itinerary["starting_location"],
            normal_style
        )
    )

    # Circular route
    story.append(
        Paragraph("3. CIRCULAR DRIVING ROUTE", heading_style)
    )

    route_text = " → ".join(itinerary["circular_route"])

    story.append(
        Paragraph(route_text, normal_style)
    )

    # Driving summary
    story.append(
        Paragraph("4. DRIVING SUMMARY", heading_style)
    )

    driving = itinerary["driving_summary"]

    driving_data = [
        ["Total Distance", f'{driving["total_distance_km"]} KM'],
        ["Estimated Driving Time", f'{driving["total_driving_hours"]} Hours']
    ]

    driving_table = Table(driving_data, colWidths=[6 * cm, 10 * cm])

    driving_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 7)
    ]))

    story.append(driving_table)

    # Attractions
    story.append(
        Paragraph("5. SELECTED TOURIST ATTRACTIONS", heading_style)
    )

    for destination_id, attraction_list in (
        itinerary["selected_attractions"].items()
    ):

        story.append(
            Paragraph(f"<b>{destination_id}</b>", normal_style)
        )

        for attraction in attraction_list:
            story.append(
                Paragraph(f"• {attraction}", normal_style)
            )

        story.append(Spacer(1, 5))

    # Hotels
    story.append(
        Paragraph("6. HOTEL COMPARISON", heading_style)
    )

    hotel_data = [
        [
            "Hotel Name",
            "Platform",
            "Stars",
            "Total Price",
            "Price/Night"
        ]
    ]

    for hotel in itinerary["hotel_options"]:

        hotel_data.append([
            hotel["hotel_name"],
            hotel["platform"],
            str(hotel["hotel_stars"]),
            f'{hotel["currency"]} {hotel["total_price"]}',
            f'{hotel["currency"]} {hotel["price_per_night"]}'
        ])

    hotel_table = Table(
        hotel_data,
        colWidths=[5 * cm, 3 * cm, 1.3 * cm, 3.2 * cm, 3.5 * cm],
        repeatRows=1
    )

    hotel_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 8)
    ]))

    story.append(hotel_table)

    # Hotel data disclaimer
    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>Hotel Data Status:</b> " +
            itinerary["hotel_data_status"],
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "Thank you for using our Europe Self-Drive Travel Planner!",
            styles["Italic"]
        )
    )

    # Generate PDF
    document.build(story)

    print("\nPDF GENERATED SUCCESSFULLY!")
    print("File location:", pdf_path)

    return pdf_path