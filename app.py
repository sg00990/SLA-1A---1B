import streamlit as st
import datetime
import json

st.set_page_config(
    page_title="SLA 1A & 1B Questionnaire",
    page_icon="💻",
    layout="wide"
)

conn = st.connection("snowflake")

st.markdown('<p style="font-family:sans-serif; color:#324a62; font-size: 28px; font-weight: bold">Tier 2 SLA Questionnaire</p>', unsafe_allow_html=True)
st.write("###")

st.markdown('<p style="font-family:sans-serif; color:#87c440; font-size: 20px; font-weight: bold">SLA 1A/1B</p>', unsafe_allow_html=True)


st.write("**Did your team experience a Planned or Unplanned Outage this past week?**")
experienced_outage = st.radio("experienced_outage", options=["No", "Yes"], label_visibility="collapsed")
st.write("**Workstream**")
workstream = st.selectbox("Workstream", options=["BP", "Impact", "LDAP", "Doc Center", "CDMS", "IC Importers", "Content Manager"], label_visibility="collapsed")

outage_start_datetime = None
outage_end_datetime = None
outage_desc = None
outage_planned = None

if experienced_outage == "Yes":
    st.write("**If yes, please answer the following**")
    outage_planned = st.radio("Planned?", options=["No", "Yes"])

    col3, col4 = st.columns(2)

    with col3:
        outage_start = st.date_input(
            "Outage Start Date",
            format="MM/DD/YYYY"
        )
    with col4:
        outage_start_time = st.time_input("Outage Start Time", step=60, value=None, help="Please type or select a time from the list. To restart, please select the 'x' to the right.")

    col5, col6 = st.columns(2)

    with col5:
        outage_end = st.date_input(
            "Outage End Date",
            format="MM/DD/YYYY",
        )
    with col6:
        outage_end_time = st.time_input("Outage End Time", step=60, value=None, help="Please type or select a time from the list. To restart, please select the 'x' to the right.")

    outage_desc = st.text_area("Brief Description", key="outage_desc")
    outage_desc = outage_desc.replace("\n", "  ").replace("'", "''").replace('"', r'\"')

    if outage_start_time is not None:
        outage_start_datetime = datetime.datetime.combine(outage_start, outage_start_time)
    if outage_end_time is not None:
        outage_end_datetime = datetime.datetime.combine(outage_end, outage_end_time)

#st.write("**Additional Comments**")
#survey_text = st.text_area("survey_text", label_visibility="collapsed")
#survey_text = survey_text.replace("\n", "  ").replace("'", "''").replace('"', r'\"')


col1, col2, col3 = st.columns(3)

with col3:
    if st.button("Submit", use_container_width=True):
        data = {
            "sla_1ab_experienced_outage": experienced_outage,
            "sla_1ab_workstream": workstream,
            "sla_1ab_outage_planned": outage_planned,
            "sla_1ab_outage_start": outage_start_datetime,
            "sla_1ab_outage_end": outage_end_datetime,
            "sla_1ab_outage_reason": outage_desc,
            #"sla_1ab_comments": survey_text
        }

        json_data = json.dumps(data, indent=4, sort_keys=True, default=str)

        date_submitted = datetime.datetime.now()

        try:
            conn.query(f""" INSERT INTO sla_tier_2_questionnaire (type, date_submitted, json_data) SELECT 'SLA 1A & 1B', '{date_submitted}', (parse_json('{json_data}'))""")
        except:
            st.success("Thank you for your responses!")


col4, col5, col6 = st.columns([1, .5, 1])

with col4:
    st.write("##")
    st.image("img/blue_bar.png")
    
with col5:
    col17, col18, col19 = st.columns(3)
    with col18:
        st.write("######")
        st.image("img/moser_logo.png")
with col6:
    st.write("##")
    st.image("img/blue_bar.png")


