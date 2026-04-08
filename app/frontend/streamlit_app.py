import os
import sys
from datetime import date
import pandas as pd
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database.db import SessionLocal
from app.database.init_db import init_db
from app.models.application import JobApplication

st.set_page_config(page_title="JobFlow AI", page_icon="📌", layout="wide")

init_db()


def get_all_applications():
    db = SessionLocal()
    try:
        return db.query(JobApplication).order_by(JobApplication.id.desc()).all()
    finally:
        db.close()


def add_application(company, role, status, applied_date, recruiter_name, recruiter_email, notes):
    db = SessionLocal()
    try:
        new_application = JobApplication(
            company=company,
            role=role,
            status=status,
            date_applied=str(applied_date),
            recruiter_name=recruiter_name,
            recruiter_email=recruiter_email,
            notes=notes,
        )
        db.add(new_application)
        db.commit()
    finally:
        db.close()


applications = get_all_applications()

st.title("JobFlow AI")
st.subheader("Track job applications and follow-ups in one place")

st.markdown("### Search and Filter")

search_term = st.text_input("Search by company or role")
status_filter = st.selectbox(
    "Filter by status",
    ["All", "Applied", "Interview", "Rejected", "Offer"]
)

filtered_applications = applications

if search_term.strip():
    query = search_term.strip().lower()
    filtered_applications = [
        app for app in filtered_applications
        if query in app.company.lower() or query in app.role.lower()
    ]

if status_filter != "All":
    filtered_applications = [
        app for app in filtered_applications
        if app.status == status_filter
    ]

st.markdown("---")
st.markdown("### Dashboard Overview")

total_apps = len(filtered_applications)
interviews = sum(1 for app in filtered_applications if app.status == "Interview")
offers = sum(1 for app in filtered_applications if app.status == "Offer")
follow_ups_due = sum(1 for app in filtered_applications if app.status == "Applied")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Applications", total_apps)

with col2:
    st.metric("Interviews", interviews)

with col3:
    st.metric("Offers", offers)

with col4:
    st.metric("Follow-ups Due", follow_ups_due)

st.markdown("---")
st.markdown("### Add New Job Application")

with st.form("job_application_form"):
    company = st.text_input("Company")
    role = st.text_input("Role")
    status = st.selectbox("Status", ["Applied", "Interview", "Rejected", "Offer"])
    applied_date = st.date_input("Date Applied", value=date.today())
    recruiter_name = st.text_input("Recruiter Name")
    recruiter_email = st.text_input("Recruiter Email")
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Save Application")

    if submitted:
        if company.strip() and role.strip():
            add_application(
                company.strip(),
                role.strip(),
                status,
                applied_date,
                recruiter_name.strip(),
                recruiter_email.strip(),
                notes.strip()
            )
            st.success(f"Application for {role} at {company} added successfully.")
            st.rerun()
        else:
            st.error("Please enter both company and role.")

st.markdown("---")
st.markdown("### Tracked Applications")

table_data = [
    {
        "ID": app.id,
        "Company": app.company,
        "Role": app.role,
        "Status": app.status,
        "Date Applied": app.date_applied,
        "Recruiter Name": app.recruiter_name,
        "Recruiter Email": app.recruiter_email,
        "Notes": app.notes,
    }
    for app in filtered_applications
]

if table_data:
    st.dataframe(table_data, use_container_width=True)

    df = pd.DataFrame(table_data)
    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Export to CSV",
        data=csv_data,
        file_name="jobflow_applications.csv",
        mime="text/csv",
    )
else:
    st.warning("No applications match your current search/filter.")

st.markdown("---")
st.info("You can now track recruiter details for each application.")