### hey this is my moon phase tracker i wanted to do for fun :) hope you enjoy itxx -r

import streamlit as st
from datetime import datetime
import ephem
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
import calendar


def get_moon_phase(date=None):
    if not date:
        date = datetime.now()
    moon = ephem.Moon(date)
    phase = moon.phase

    if phase < 1:
        return "New Moon"
    elif phase < 50:
        return "Waxing Crescent"
    elif phase == 50:
        return "First Quarter"
    elif phase < 100:
        return "Waxing Gibbous"
    elif phase == 100:
        return "Full Moon"
    elif phase > 50:
        return "Waning Gibbous"
    elif phase == 50:
        return "Last Quarter"
    else:
        return "Waning Crescent"


def create_moon_visual(phase):
    img = Image.new("RGB", (200, 200), "black")
    draw = ImageDraw.Draw(img)
    draw.ellipse([25, 25, 175, 175], fill="white")
    return img


def astrophotography_tips(phase):
    if phase in ["New Moon", "Waxing Crescent", "Waning Crescent"]:
        return "Great night for stargazing! The dark skies allow for excellent astrophotography."
    elif phase in ["First Quarter", "Last Quarter"]:
        return "Good for stargazing, but bright moonlight may reduce visibility for faint stars."
    elif phase in ["Full Moon", "Waxing Gibbous", "Waning Gibbous"]:
        return "Not ideal for stargazing. The moonlight will overpower most stars."
    else:
        return "Phase unknown. Please check again!"


def get_monthly_phases(year, month):
    cal = calendar.Calendar()
    days = cal.itermonthdays(year, month)
    phases = {}

    for day in days:
        if day > 0:
            date = datetime(year, month, day)
            phase_name = get_moon_phase(date)
            phases[day] = phase_name

    return phases


def generate_pdf(date, phase, tips):
    filename = f"Moon_Phase_{date}.pdf"
    c = canvas.Canvas(filename)
    c.drawString(100, 800, f"Moon Phase Report for {date}")
    c.drawString(100, 780, f"Phase: {phase}")
    c.drawString(100, 760, f"Astrophotography Tip: {tips}")
    c.save()
    return filename


st.title("Enhanced Moon Phase Tracker 🌙")

date = st.date_input("Select a date:", datetime.now())
phase = get_moon_phase(date)
tips = astrophotography_tips(phase)

st.write(f"Moon Phase on {date}: {phase}")
st.write(f"Astrophotography Tip: {tips}")

moon_image = create_moon_visual(phase)
st.image(moon_image, caption=f"Moon Phase: {phase}")

if st.button("Download Report"):
    pdf_path = generate_pdf(date, phase, tips)
    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF Report", f, file_name="moon_phase_report.pdf")

year = st.number_input("Year:", min_value=2000, max_value=2100, value=datetime.now().year)
month = st.number_input("Month:", min_value=1, max_value=12, value=datetime.now().month)

if st.button("Generate Calendar"):
    phases = get_monthly_phases(year, month)
    st.write(f"Moon Phases for {calendar.month_name[month]} {year}:")
    for day, phase in phases.items():
        st.write(f"{day}: {phase}")
