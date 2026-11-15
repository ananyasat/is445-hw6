
import streamlit as st
import pandas as pd
import altair as alt

st.title("Illinois Building Inventory Explorer")

st.write("IS 445 - Homework 6")

url = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv"

df = pd.read_csv(url)

df["Square Footage"] = pd.to_numeric(
    df["Square Footage"], errors="coerce"
)

df["Year Constructed"] = pd.to_numeric(
    df["Year Constructed"], errors="coerce"
)

# Interactive dropdown
agencies = ["All agencies"] + sorted(
    df["Agency Name"].dropna().unique().tolist()
)

selected_agency = st.selectbox("Select an agency", agencies)

if selected_agency != "All agencies":
    df = df[df["Agency Name"] == selected_agency]

# Visualization 1
st.header("Total Square Footage by Building Usage")

chart1 = alt.Chart(df).mark_bar(color="steelblue").encode(
    x=alt.X(
        "sum(Square Footage):Q",
        title="Total Square Footage"
    ),
    y=alt.Y(
        "Usage Description:N",
        sort="-x",
        title="Building Usage"
    ),
    tooltip=[
        "Usage Description:N",
        "sum(Square Footage):Q"
    ]
).properties(height=400)

st.altair_chart(chart1, use_container_width=True)

st.write("""
The first visualization highlights how total building square
footage varies across different building usage categories.
I chose a horizontal bar chart because it makes comparing
categories easier and provides sufficient space for the
category labels. I used a quantitative scale for square
footage and a nominal scale for building usage. The bars are
sorted in descending order to make comparisons easier.
I selected a consistent blue color to avoid unnecessary
visual distractions. If I had more time, I would include
additional geographic filters and allow users to compare
multiple agencies at once.
""")

# Visualization 2
st.header("Building Construction by Decade")

building_years = df[
    (df["Year Constructed"] >= 1800) &
    (df["Year Constructed"] <= 2026)
].copy()

building_years["Decade"] = (
    building_years["Year Constructed"] // 10 * 10
).astype(int)

chart2 = alt.Chart(building_years).mark_bar(
    color="seagreen"
).encode(
    x=alt.X("Decade:O", title="Construction Decade"),
    y=alt.Y("count():Q", title="Number of Buildings"),
    tooltip=["Decade:O", "count():Q"]
).properties(height=350)

st.altair_chart(chart2, use_container_width=True)

st.write("""
The second visualization shows how the number of buildings
in the inventory varies by construction decade. I grouped
construction years into decades to reduce visual clutter
and make historical patterns easier to identify. I used
vertical bars with an ordinal scale for decades and a
quantitative scale for building counts. I chose green to
distinguish this visualization from the first chart.
The agency dropdown allows users to explore construction
patterns for individual agencies. If I had more time,
I would add an interactive year range and compare
construction patterns across different counties.
""")
