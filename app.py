
import streamlit as st
import pandas as pd
import altair as alt

alt.data_transformers.disable_max_rows()

st.set_page_config(
    page_title="Illinois Building Inventory Explorer",
    layout="wide"
)

st.title("Illinois Building Inventory Explorer")
st.write("IS 445 - Homework 6")

url = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(url)

    df["Square Footage"] = pd.to_numeric(
        df["Square Footage"], errors="coerce"
    )

    df["Year Constructed"] = pd.to_numeric(
        df["Year Constructed"], errors="coerce"
    )

    return df

df = load_data()

st.write("""
Explore building usage and historical construction patterns
across Illinois. Select an agency to filter both visualizations.
""")

# Interactive dropdown
agencies = ["All agencies"] + sorted(
    df["Agency Name"].dropna().unique().tolist()
)

selected_agency = st.selectbox("Select an agency", agencies)

if selected_agency != "All agencies":
    df = df[df["Agency Name"] == selected_agency]

# Visualization 1
st.header("Total Square Footage by Building Usage")

usage_data = df.groupby(
    "Usage Description", as_index=False
)["Square Footage"].sum()

chart1 = alt.Chart(usage_data).mark_bar(
    color="steelblue"
).encode(
    x=alt.X(
        "Square Footage:Q",
        title="Total Square Footage",
        axis=alt.Axis(format="~s")
    ),
    y=alt.Y(
        "Usage Description:N",
        sort="-x",
        title="Building Usage"
    ),
    tooltip=[
        alt.Tooltip("Usage Description:N", title="Building Usage"),
        alt.Tooltip("Square Footage:Q", format=",.0f")
    ]
).properties(height=400)

st.altair_chart(chart1, use_container_width=True)

st.subheader("Visualization 1 Write-up")

st.write("""
The first visualization highlights how total building square
footage varies across different building usage categories in
Illinois. I chose a horizontal bar chart because it makes
comparing categories easier and provides sufficient space
for longer category labels. I used a quantitative scale for
square footage and a nominal scale for building usage.
The bars are sorted in descending order so users can easily
identify which categories occupy the most space. I selected
a consistent blue color because the purpose of the chart
is to compare bar lengths rather than distinguish additional
categories through color. The interactive agency dropdown
allows users to explore how building usage differs between
agencies. If I had more time, I would include geographic
filters and allow users to compare multiple agencies
simultaneously.
""")

st.write("""
**Homework 5 Overlap:** I did not complete Homework 5.
This visualization, data analysis, and write-up were
created specifically for Homework 6. No previous work
was reused.
""")

st.divider()

# Visualization 2
st.header("Building Construction by Decade")

building_years = df[
    (df["Year Constructed"] >= 1800) &
    (df["Year Constructed"] <= 2026)
].copy()

building_years["Decade"] = (
    building_years["Year Constructed"] // 10 * 10
).astype(int)

decade_data = building_years.groupby(
    "Decade"
).size().reset_index(name="Building Count")

chart2 = alt.Chart(decade_data).mark_bar(
    color="seagreen"
).encode(
    x=alt.X(
        "Decade:O",
        title="Construction Decade",
        sort="ascending",
        axis=alt.Axis(labelAngle=-45)
    ),
    y=alt.Y(
        "Building Count:Q",
        title="Number of Buildings"
    ),
    tooltip=[
        alt.Tooltip("Decade:O"),
        alt.Tooltip("Building Count:Q", format=",")
    ]
).properties(height=350)

st.altair_chart(chart2, use_container_width=True)

st.subheader("Visualization 2 Write-up")

st.write("""
The second visualization highlights historical construction
patterns by showing the number of buildings in the inventory
that were constructed during each decade. I grouped
construction years into decades to reduce visual clutter
and make broader historical patterns easier to identify.
Missing and unreasonable construction years were excluded
from the visualization. I chose vertical bar marks with
an ordinal scale for construction decades and a quantitative
scale for building counts. The decades are arranged
chronologically so users can identify changes over time.
I selected a consistent green color to distinguish this
visualization from the first chart without introducing
unnecessary visual complexity. The agency dropdown allows
users to explore construction patterns for individual
agencies. If I had more time, I would add an interactive
year range and allow users to compare historical construction
patterns across different counties.
""")

st.write("""
**Homework 5 Overlap:** I did not complete Homework 5.
This visualization, data analysis, and write-up were
created specifically for Homework 6. No previous work
was reused.
""")

st.divider()

st.caption("Data Source: UIUC iSchool Data Visualization - Illinois Building Inventory")

st.markdown(
    "[View Original Dataset](https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv)"
)
