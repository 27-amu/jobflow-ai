import os
import sys
from datetime import date, datetime

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


def update_application(app_id, company, role, status, applied_date, notes):
    db = SessionLocal()
    try:
        application = db.query(JobApplication).filter(JobApplication.id == app_id).first()
        if application:
            application.company = company
            application.role = role
            application.status = status
            application.date_applied = str(applied_date)
            application.notes = notes
            db.commit()
    finally:
        db.close()


def delete_application(app_id):
    db = SessionLocal()
    try:
        application = db.query(JobApplication).filter(JobApplication.id == app_id).first()
        if application:
            db.delete(application)
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
            add_application(company.strip(), role.strip(), status, applied_date, notes.strip())
            st.success(f"Application for {role} at {company} added successfully.")
            st.rerun()
        else:
            st.error("Please enter both company and role.")

st.markdown("---")
st.markdown("### Tracked Applications")

if applications:
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
else:
    st.warning("No applications tracked yet.")

st.markdown("---")
st.markdown("### Manage Existing Application")

if applications:
    selected_option = st.selectbox(
        "Select an application",
        options=applications,
        format_func=lambda app: f"{app.id} - {app.company} | {app.role} | {app.status}",
    )

    default_date = datetime.strptime(selected_option.date_applied, "%Y-%m-%d").date()

    with st.form("edit_application_form"):
        edit_company = st.text_input("Edit Company", value=selected_option.company)
        edit_role = st.text_input("Edit Role", value=selected_option.role)
        edit_status = st.selectbox(
            "Edit Status",
            ["Applied", "Interview", "Rejected", "Offer"],
            index=["Applied", "Interview", "Rejected", "Offer"].index(selected_option.status),
        )
        edit_date = st.date_input("Edit Date Applied", value=default_date)
        edit_notes = st.text_area("Edit Notes", value=selected_option.notes or "")
        col_save, col_delete = st.columns(2)

        with col_save:
            save_clicked = st.form_submit_button("Update Application")

        with col_delete:
            delete_clicked = st.form_submit_button("Delete Application")

        if save_clicked:
            if edit_company.strip() and edit_role.strip():
                update_application(
                    selected_option.id,
                    edit_company.strip(),
                    edit_role.strip(),
                    edit_status,
                    edit_date,
                    edit_notes.strip(),
                )
                st.success("Application updated successfully.")
                st.rerun()
            else:
                st.error("Company and role cannot be empty.")

        if delete_clicked:
            delete_application(selected_option.id)
            st.success("Application deleted successfully.")
            st.rerun()

st.markdown("---")
st.info("You can now add, update, and delete applications.")