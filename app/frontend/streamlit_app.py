import streamlit as st

st.set_page_config(page_title="JobFlow AI", page_icon="📌", layout="wide")

st.title("JobFlow AI")
st.subheader("Track job applications and follow-ups in one place")

st.markdown("### Dashboard Preview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Applications", 12)

with col2:
    st.metric("Interviews", 3)

with col3:
    st.metric("Offers", 1)

with col4:
    st.metric("Follow-ups Due", 4)

st.markdown("---")

st.markdown("### Recent Applications")

sample_data = [
    {"Company": "Google", "Role": "Product Analyst", "Status": "Applied"},
    {"Company": "Amazon", "Role": "Business Analyst", "Status": "Interview"},
    {"Company": "Meta", "Role": "Product Manager", "Status": "Rejected"},
]

st.table(sample_data)

st.markdown("---")
st.info("This is the first visible UI for JobFlow AI.")