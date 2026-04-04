import streamlit as st
from datetime import date

st.set_page_config(page_title="JobFlow AI", page_icon="📌", layout="wide")

if "applications" not in st.session_state:
st.session_state.applications = [
{
"Company": "Google",
"Role": "Product Analyst",
"Status": "Applied",
"Date Applied": "2026-04-01",
"Notes": "Waiting for recruiter response",
},
{
"Company": "Amazon",
"Role": "Business Analyst",
"Status": "Interview",
"Date Applied": "2026-03-28",
"Notes": "Interview scheduled next week",
},
]

st.title("JobFlow AI")
st.subheader("Track job applications and follow-ups in one place")

st.markdown("### Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

applications = st.session_state.applications
total_apps = len(applications)
interviews = sum(1 for app in applications if app["Status"] == "Interview")
offers = sum(1 for app in applications if app["Status"] == "Offer")
follow_ups_due = sum(1 for app in applications if app["Status"] == "Applied")

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
            st.session_state.applications.append(
                {
                    "Company": company.strip(),
                    "Role": role.strip(),
                    "Status": status,
                    "Date Applied": str(applied_date),
                    "Notes": notes.strip(),
                }
            )
            st.success(f"Application for {role} at {company} added successfully.")
        else:
            st.error("Please enter both company and role.")

st.markdown("---")

st.markdown("### Tracked Applications")
st.dataframe(st.session_state.applications, use_container_width=True)

st.markdown("---")
st.info("Next step: store applications in SQLite instead of temporary session state.")
