import streamlit as st
from datetime import date
from app.database.db import SessionLocal
from app.database.init_db import init_db
from app.models.application import JobApplication

st.set_page_config(page_title="JobFlow AI", page_icon="📌", layout="wide")

init_db()

def get_all_applications():
    db = SessionLocal()
    try:
        return db.query(JobApplication).all()
    finally:
        db.close()

def add_application(company, role, status, applied_date, notes):
    db = SessionLocal()
    try:
        new_application = JobApplication(
            company=company,
            role=role,
            status=status,
            date_applied=str(applied_date),
            notes=notes,
        )
        db.add(new_application)
        db.commit()
    finally:
        db.close()

applications = get_all_applications()

st.title("JobFlow AI")
st.subheader("Track job applications and follow-ups in one place")

st.markdown("### Dashboard Overview")

total_apps = len(applications)
interviews = sum(1 for app in applications if app.status == "Interview")
offers = sum(1 for app in applications if app.status == "Offer")
follow_ups_due = sum(1 for app in applications if app.status == "Applied")

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
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Save Application")

    if submitted:
        if company.strip() and role.strip():
            add_application(
                company.strip(),
                role.strip(),
                status,
                applied_date,
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
        "Notes": app.notes,
    }
    for app in applications
]

st.dataframe(table_data, use_container_width=True)

st.markdown("---")
st.info("Applications are now stored in SQLite for persistent tracking.")