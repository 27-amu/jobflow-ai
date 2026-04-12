import os
import sys
from datetime import date, datetime
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


def add_application(company, role, status, applied_date, recruiter_name, recruiter_email, follow_up_date, notes):
    db = SessionLocal()
    try:
        new_application = JobApplication(
            company=company,
            role=role,
            status=status,
            date_applied=str(applied_date),
            recruiter_name=recruiter_name,
            recruiter_email=recruiter_email,
            follow_up_date=str(follow_up_date) if follow_up_date else "",
            notes=notes,
        )
        db.add(new_application)
        db.commit()
    finally:
        db.close()


def update_application(app_id, company, role, status, applied_date, recruiter_name, recruiter_email, follow_up_date, notes):
    db = SessionLocal()
    try:
        application = db.query(JobApplication).filter(JobApplication.id == app_id).first()
        if application:
            application.company = company
            application.role = role
            application.status = status
            application.date_applied = str(applied_date)
            application.recruiter_name = recruiter_name
            application.recruiter_email = recruiter_email
            application.follow_up_date = str(follow_up_date) if follow_up_date else ""
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


def is_overdue(follow_up_date_value):
    if not follow_up_date_value:
        return False
    try:
        return datetime.strptime(follow_up_date_value, "%Y-%m-%d").date() < date.today()
    except ValueError:
        return False


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
follow_ups_due = sum(
    1 for app in filtered_applications
    if app.follow_up_date and not is_overdue(app.follow_up_date)
)
overdue_followups = sum(
    1 for app in filtered_applications
    if is_overdue(app.follow_up_date)
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Applications", total_apps)
with col2:
    st.metric("Interviews", interviews)
with col3:
    st.metric("Offers", offers)
with col4:
    st.metric("Follow-ups Due", follow_ups_due)
with col5:
    st.metric("Overdue", overdue_followups)

st.markdown("---")
st.markdown("### Add New Job Application")

with st.form("job_application_form"):
    company = st.text_input("Company")
    role = st.text_input("Role")
    status = st.selectbox("Status", ["Applied", "Interview", "Rejected", "Offer"])
    applied_date = st.date_input("Date Applied", value=date.today())
    recruiter_name = st.text_input("Recruiter Name")
    recruiter_email = st.text_input("Recruiter Email")
    follow_up_date = st.date_input("Follow-up Date", value=None)
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
                follow_up_date,
                notes.strip()
            )
            st.success(f"Application for {role} at {company} added successfully.")
            st.rerun()
        else:
            st.error("Please enter both company and role.")

st.markdown("---")
st.markdown("### Tracked Applications")

table_data = []
for app in filtered_applications:
    table_data.append(
        {
            "ID": app.id,
            "Company": app.company,
            "Role": app.role,
            "Status": app.status,
            "Date Applied": app.date_applied,
            "Recruiter Name": app.recruiter_name,
            "Recruiter Email": app.recruiter_email,
            "Follow-up Date": app.follow_up_date,
            "Overdue": "Yes" if is_overdue(app.follow_up_date) else "No",
            "Notes": app.notes,
        }
    )

if table_data:
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)

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
st.markdown("### Edit Existing Application")

if applications:
    selected_application = st.selectbox(
        "Select application to edit",
        options=applications,
        format_func=lambda app: f"{app.id} - {app.company} | {app.role}"
    )

    default_applied_date = datetime.strptime(selected_application.date_applied, "%Y-%m-%d").date()

    if selected_application.follow_up_date:
        try:
            default_follow_up_date = datetime.strptime(selected_application.follow_up_date, "%Y-%m-%d").date()
        except ValueError:
            default_follow_up_date = None
    else:
        default_follow_up_date = None

    with st.form("edit_application_form"):
        edit_company = st.text_input("Edit Company", value=selected_application.company)
        edit_role = st.text_input("Edit Role", value=selected_application.role)
        edit_status = st.selectbox(
            "Edit Status",
            ["Applied", "Interview", "Rejected", "Offer"],
            index=["Applied", "Interview", "Rejected", "Offer"].index(selected_application.status),
        )
        edit_applied_date = st.date_input("Edit Date Applied", value=default_applied_date)
        edit_recruiter_name = st.text_input("Edit Recruiter Name", value=selected_application.recruiter_name or "")
        edit_recruiter_email = st.text_input("Edit Recruiter Email", value=selected_application.recruiter_email or "")
        edit_follow_up_date = st.date_input("Edit Follow-up Date", value=default_follow_up_date)
        edit_notes = st.text_area("Edit Notes", value=selected_application.notes or "")
        update_submitted = st.form_submit_button("Update Application")

        if update_submitted:
            if edit_company.strip() and edit_role.strip():
                update_application(
                    selected_application.id,
                    edit_company.strip(),
                    edit_role.strip(),
                    edit_status,
                    edit_applied_date,
                    edit_recruiter_name.strip(),
                    edit_recruiter_email.strip(),
                    edit_follow_up_date,
                    edit_notes.strip(),
                )
                st.success("Application updated successfully.")
                st.rerun()
            else:
                st.error("Company and role cannot be empty.")

st.markdown("---")
st.markdown("### Delete Application")

if applications:
    selected_delete_application = st.selectbox(
        "Select application to delete",
        options=applications,
        format_func=lambda app: f"{app.id} - {app.company} | {app.role}",
        key="delete_selectbox"
    )

    confirm_delete = st.checkbox(
        f"I understand this will permanently delete application #{selected_delete_application.id}",
        key="confirm_delete_checkbox"
    )

    if st.button("Delete Selected Application"):
        if confirm_delete:
            delete_application(selected_delete_application.id)
            st.success("Application deleted successfully.")
            st.rerun()
        else:
            st.error("Please confirm deletion before proceeding.")

st.markdown("---")
st.info("You can now add, edit, export, and safely delete applications.")