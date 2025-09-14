import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- App Config ---
st.set_page_config(page_title="Women Techsters Vision Board", layout="wide")
theme_css = """
<style>
/* Main App Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #6A1B9A, #EC407A);
    font-family: 'Segoe UI', sans-serif;
    color: #ffffff;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: linear-gradient(#6A1B9A; #ffffff);
    color: #ffffff;
    
}
[data-testid="stSidebar"] .css-1v3fvcr { /* Sidebar titles */
    color: #6A1B9A !important;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar titles */
[data-testid="stSidebar"] h1, h2, h3, h4, label {
    color: #6A1B9A !important;
    font-family: 'Segoe UI', sans-serif;
 }

/* Header */
[data-testid="stHeader"] h1, h3 {
    
    color: #6A1B9A;
    border-bottom: 3px solid #EC407A;
}

/* Title and Subheader */
h1, h2 {
    color: #ffffff !important;
    font-weight: bold;
}
h3 {
    background: #ffffff;
    color: ##6A1B9A !important;
    font-family: 'Segoe UI', sans-serif;
}

/* Buttons */
div.stButton > button {
    background-color: #26A69A;
    color: #ffffff;
    border-radius: 8px;
    border: none;
}
div.stButton > button:hover {
    background-color: #EC407A;
    color: #ffffff;
}


div.stform {
    background-color: #EC407A
    color: #EC407A;
    font-weight: bold

/* Dataframes (tables) */
.css-1xarl3l, .css-1q8dd3e { 
    background-color: #ffffff !important;
    color: #000814 !important;
    border-radius: 10px;
}



/* Success/Info messages */
.stAlert {
    color: #ffffff;
    border-radius: 8px;
}

# div.stSuccess {
#     color: #ffffff;
#     border-radius: 8px;
# }
</style>
"""
st.markdown(theme_css, unsafe_allow_html=True)

# --- THEME STYLING ---
# custom_theme = """
# <style>
# /* App background */
# [data-testid="stAppViewContainer"] {
#     background: linear-gradient(135deg, #4B0082, #000814); /* purple → bluish black */
#     color: white;
# }

# /* Sidebar */
# [data-testid="stSidebar"] {
#     background-color: #2C003E; /* dark purple */
#     color: white;
# }

# /* Header titles */
# h1, h2, h3, h4 {
#     color: #ffffff !important;
#     font-family: 'Segoe UI', sans-serif;
# }

# /* Sidebar titles */
# [data-testid="stSidebar"] h1, h2, h3, h4, label {
#     color: #ffffff !important;
# }
# </style>
# """
# st.markdown(custom_theme, unsafe_allow_html=True)

# --- ADD LOGO ---
logo_path = "WTF_LOGO.PNG"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width='content')
else:
    st.sidebar.warning("⚠️ Logo not found. Place 'logo.png' in app folder.")

st.title("📊 My Women Techsters Fellowship Vision Board")
st.subheader("✨ Data Science & Engineering Track")

# --- File Paths ---
FILES = {
    "goals": "goals.csv",
    "activities": "activities.csv",
    "weekly": "weekly.csv",
    "metrics": "metrics.csv"
}

# --- Load & Save ---
def load_csv(file):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame()

def save_csv(df, file):
    df.to_csv(file, index=False)

goals = load_csv(FILES["goals"])
activities = load_csv(FILES["activities"])
weekly = load_csv(FILES["weekly"])
metrics = load_csv(FILES["metrics"])

# --- Sidebar Navigation ---
st.sidebar.title("📌 Navigation")
section = st.sidebar.radio(
    "Go to Section",
    ["🎯 Goals", "📝 Activities", "📔 Weekly Journal", "📈 Metrics & KPIs"]
)

# --- EDIT & DELETE UTILITIES ---
def edit_entry(df, file, index):
    st.write("✏️ Edit entry:")
    cols = st.columns(len(df.columns))
    new_data = {}
    for i, col in enumerate(df.columns):
        value = df.at[index, col]
        if isinstance(value, (int, float)):
            new_data[col] = cols[i].number_input(col, value=value)
        else:
            new_data[col] = cols[i].text_input(col, value=str(value))
    if st.button("Save Changes", key=f"save_{file}_{index}"):
        for k, v in new_data.items():
            df.at[index, k] = v
        save_csv(df, file)
        st.success("✅ Entry updated successfully!")
        #st.experimental_rerun()

def delete_entry(df, file, index):
    if st.button("🗑️ Delete", key=f"del_{file}_{index}"):
        df = df.drop(index).reset_index(drop=True)
        save_csv(df, file)
        st.success("🚮 Entry deleted successfully!")
        #st.experimental_rerun()
    return df


# --- GOALS SECTION ---
if section == "🎯 Goals":
    st.header("🎯 Goals & Phases")
    st.dataframe(goals)

    # Add New Goal
    with st.form("Add Goal"):
        st.write("New Goal Form")
        new_goal = st.text_input("Goal")
        new_phase = st.text_input("Phase")
        new_progress = st.number_input("Current Progress %", 0, 100, step=1)
        submitted = st.form_submit_button("Add Goal")
        if submitted and new_goal:
            new_row = {"Goal": new_goal, "Phase": new_phase, "Current Progress %": new_progress}
            goals = pd.concat([goals, pd.DataFrame([new_row])], ignore_index=True)
            save_csv(goals, FILES["goals"])
            st.success("New goal added!")

    if not goals.empty:
        selected = st.selectbox("Select entry to edit/delete", goals.index)
        edit_entry(goals, FILES["goals"], selected)
        goals = delete_entry(goals, FILES["goals"], selected)


    # Visualization
    if not goals.empty:
        fig1, ax1 = plt.subplots()
        ax1.bar(goals["Goal"], goals["Current Progress %"])
        ax1.set_ylabel("Progress %")
        ax1.set_ylim(0, 100)
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig1)


# --- ACTIVITIES SECTION ---
elif section == "📝 Activities":
    st.header("📝 Activities Tracker")
    st.dataframe(activities)

    # Add New Activity
    with st.form("Add Activity"):
        st.write("New Activity Form")
        new_activity = st.text_input("Activity")
        new_goal = st.selectbox("Related Goal", ["Tutorial", "Project", "Posts"])
        new_output = st.text_input("Expected Output")
        new_outcome = st.text_input("Expected Outcome")
        new_startdate = st.date_input("Start Date")
        new_enddate = st.date_input("End Date")
        new_duration = st.number_input("Duration (hrs)", 1, 14)
        new_status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])
        new_progress = st.text_input("Progress %")
        new_output_link = st.text_input("Actual Output Link")
        new_metric = st.text_input("Impact Metric Percent")
        submitted = st.form_submit_button("Add New Activity")
        if submitted and new_activity:
            new_row = {
                "Activity": new_activity, 
                "Related Goal": new_goal, 
                "Expected Outcome": new_outcome, 
                "Start Date":new_startdate, 
                "End Date": new_enddate, 
                "Status": new_status, 
                "Progress %": new_progress, 
                "Actual Output Link": new_output_link, 
                "Impact Metric Percent": new_metric
                }
            activities = pd.concat([activities, pd.DataFrame([new_row])], ignore_index=True)
            save_csv(activities, FILES["activities"])
            st.success("New activity added!")


    if not activities.empty:
        selected = st.selectbox("Select entry to edit/delete", activities.index)
        edit_entry(activities, FILES["activities"], selected)
        activities = delete_entry(activities, FILES["activities"], selected)

    # Visualization
    if not activities.empty:
        status_counts = activities["Status"].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=90)
        ax2.axis("equal")
        st.pyplot(fig2)


# --- WEEKLY JOURNAL SECTION ---
elif section == "📔 Weekly Journal":
    st.header("📔 Weekly Journal")
    st.dataframe(weekly)

    # Add Weekly Journal
    with st.form("Add Weekly Entry"):
        st.write("New weekly Entry form")
        week = st.text_input("Week")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        duration = st.number_input("Duration (days)", 1, 14)
        lessons = st.text_area("Key Lessons")
        summary = st.text_area("Keynote Summary")
        challenges = st.text_area("Challenges")
        wins = st.text_area("Wins")
        yt_link = st.text_input("YouTube Tutorial Link")
        blog_link = st.text_input("Medium Blog Link")
        confidence = st.slider("Confidence End Week (1-10)", 1, 10)
        remark = st.text_area("Remark")
        next_steps = st.text_area("Next Steps")
        submitted = st.form_submit_button("Add Journal Entry")
        if submitted and week:
            new_row = {
                "Week": week, "Start Date": start_date, "End Date": end_date,
                "Duration": duration, "Key Lessons": lessons, "Keynote Summary": summary,
                "Challenges": challenges, "Wins": wins,
                "Output Link 1": yt_link, "Output Link 2": blog_link,
                "Confidence End Week (1-10)": confidence, "Remark": remark, "Next Steps": next_steps
            }
            weekly = pd.concat([weekly, pd.DataFrame([new_row])], ignore_index=True)
            save_csv(weekly, FILES["weekly"])
            st.success("New Weekly entry added!")

    # Display Expander Format
    for _, row in weekly.iterrows():
        with st.expander(f"{row['Week']} {row['Start Date']} - {row['End Date']}"):
            st.write(f"**Duration(Days):** {row['Duration']}")
            st.write(f"**Key Lessons:** {row['Key Lessons']}")
            st.write(f"**Keynote Summary:** {row['Keynote Summary']}")
            st.write(f"**Challenges:** {row['Challenges']}")
            st.write(f"**Wins:** {row['Wins']}")
            st.markdown(f"📺 [YouTube Tutorial Video]({row['Output Link 1']}) | ✍️ [Medium Blog]({row['Output Link 2']})")
            st.write(f"Confidence Level: {row['Confidence End Week (1-10)']}/10")
            st.write(f"**Remark:** {row['Remark']}")
            st.write(f"**Next Steps:** {row['Next Steps']}")

    if not weekly.empty:
        selected = st.selectbox("Select entry to edit/delete", weekly.index)
        edit_entry(weekly, FILES["weekly"], selected)
        weekly = delete_entry(weekly, FILES["weekly"], selected)

    # Visualization
    if not weekly.empty:
        fig3, ax3 = plt.subplots()
        ax3.plot(weekly["Week"], weekly["Confidence End Week (1-10)"], marker="o", color="teal")
        ax3.set_ylabel("Confidence Level")
        ax3.set_ylim(0, 10)
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig3)


# --- METRICS SECTION ---
elif section == "📈 Metrics & KPIs":
    st.header("📈 Metrics & KPIs")
    st.dataframe(metrics)

    with st.form("Add Metric"):
        st.write("New Metric form")
        metric_name = st.text_input("Impact Metric")
        percent = st.number_input("Percent Achieved", 0, 100, step=1)
        submitted = st.form_submit_button("Add Metric")
        if submitted and metric_name:
            new_row = {"Impact Metric": metric_name, "Percent Achieved": percent}
            metrics = pd.concat([metrics, pd.DataFrame([new_row])], ignore_index=True)
            save_csv(metrics, FILES["metrics"])
            st.success("New Metric added!")    

    if not metrics.empty:
        selected = st.selectbox("Select entry to edit/delete", metrics.index)
        edit_entry(metrics, FILES["metrics"], selected)
        metrics = delete_entry(metrics, FILES["metrics"], selected)

    # Visualization
    if not metrics.empty:
        fig4, ax4 = plt.subplots()
        ax4.bar(metrics["Impact Metric"], metrics["Percent Achieved"])
        ax4.set_ylabel("% Achieved")
        ax4.set_ylim(0, 100)
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig4)

st.sidebar.info("Produced by: **SHAMMAH AGYARE** (WTFC 2026 Fellow)")
st.success("Vision Board Dashboard loaded successfully! 🚀")



# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import os

# # --- App Config ---
# st.set_page_config(page_title="Women Techsters Vision Board", layout="wide")
# st.title("📊 My Women Techsters Fellowship Vision Board")
# st.subheader("Data Science & Engineering Track")

# # --- File Paths ---
# FILES = {
#     "goals": "goals.csv",
#     "activities": "activities.csv",
#     "weekly": "weekly.csv",
#     "metrics": "metrics.csv"
# }

# # --- Load Data ---
# def load_csv(file):
#     if os.path.exists(file):
#         return pd.read_csv(file)
#     else:
#         return pd.DataFrame()

# def save_csv(df, file):
#     df.to_csv(file, index=False)

# goals = load_csv(FILES["goals"])
# activities = load_csv(FILES["activities"])
# weekly = load_csv(FILES["weekly"])
# metrics = load_csv(FILES["metrics"])

# # --- Sidebar Navigation ---
# st.sidebar.title("📌 Navigation")
# section = st.sidebar.radio(
#     "Go to Section",
#     ["🎯 Goals", "📝 Activities", "📔 Weekly Journal", "📈 Metrics & KPIs"]
# )

# # --- GOALS SECTION ---
# if section == "🎯 Goals":
#     st.header("🎯 Goals & Phases")
#     st.dataframe(goals)

    # # Add New Goal
    # with st.form("Add Goal"):
    #     new_goal = st.text_input("Goal")
    #     new_phase = st.text_input("Phase")
    #     new_progress = st.number_input("Current Progress %", 0, 100, step=1)
    #     submitted = st.form_submit_button("Add Goal")
    #     if submitted and new_goal:
    #         new_row = {"Goal": new_goal, "Phase": new_phase, "Current Progress %": new_progress}
    #         goals = pd.concat([goals, pd.DataFrame([new_row])], ignore_index=True)
    #         save_csv(goals, FILES["goals"])
    #         st.success("New goal added!")

#     # Visualization
#     if not goals.empty:
#         fig1, ax1 = plt.subplots()
#         ax1.bar(goals["Goal"], goals["Current Progress %"])
#         ax1.set_ylabel("Progress %")
#         ax1.set_ylim(0, 100)
#         plt.xticks(rotation=30, ha="right")
#         st.pyplot(fig1)


# # --- ACTIVITIES SECTION ---
# elif section == "📝 Activities":
#     st.header("📝 Activities Tracker")
#     st.dataframe(activities)

    # # Add New Activity
    # with st.form("Add Activity"):
    #     new_activity = st.text_input("Activity")
    #     new_goal = st.selectbox("Related Goal", ["Tutorial", "Project", "Posts"])
    #     new_output = st.text_input("Expected Output")
    #     new_outcome = st.text_input("Expected Outcome")
    #     new_startdate = st.date_input("Start Date")
    #     new_enddate = st.date_input("End Date")
    #     new_duration = st.number_input("Duration (hrs)", 1, 14)
    #     new_status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])
    #     new_progress = st.text_input("Progress %")
    #     new_output_link = st.text_input("Actual Output Link")
    #     new_metric = st.text_input("Impact Metric Percent")
    #     submitted = st.form_submit_button("Add New Activity")
    #     if submitted and new_activity:
    #         new_row = {
    #             "Activity": new_activity, 
    #             "Related Goal": new_goal, 
    #             "Expected Outcome": new_outcome, 
    #             "Start Date":new_startdate, 
    #             "End Date": new_enddate, 
    #             "Status": new_status, 
    #             "Progress %": new_progress, 
    #             "Actual Output Link": new_output_link, 
    #             "Impact Metric Percent": new_metric
    #             }
    #         activities = pd.concat([activities, pd.DataFrame([new_row])], ignore_index=True)
    #         save_csv(activities, FILES["activities"])
    #         st.success("New activity added!")

#     # Visualization
#     if not activities.empty:
#         status_counts = activities["Status"].value_counts()
#         fig2, ax2 = plt.subplots()
#         ax2.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=90)
#         ax2.axis("equal")
#         st.pyplot(fig2)


# # --- WEEKLY JOURNAL SECTION ---
# elif section == "📔 Weekly Journal":
#     st.header("📔 Weekly Journal")
#     st.dataframe(weekly)

    # # Add Weekly Journal
    # with st.form("Add Weekly Entry"):
    #     week = st.text_input("Week")
    #     start_date = st.date_input("Start Date")
    #     end_date = st.date_input("End Date")
    #     duration = st.number_input("Duration (days)", 1, 14)
    #     lessons = st.text_area("Key Lessons")
    #     summary = st.text_area("Keynote Summary")
    #     challenges = st.text_area("Challenges")
    #     wins = st.text_area("Wins")
    #     yt_link = st.text_input("YouTube Tutorial Link")
    #     blog_link = st.text_input("Medium Blog Link")
    #     confidence = st.slider("Confidence End Week (1-10)", 1, 10)
    #     remark = st.text_area("Remark")
    #     next_steps = st.text_area("Next Steps")
    #     submitted = st.form_submit_button("Add Journal Entry")
    #     if submitted and week:
    #         new_row = {
    #             "Week": week, "Start Date": start_date, "End Date": end_date,
    #             "Duration": duration, "Key Lessons": lessons, "Keynote Summary": summary,
    #             "Challenges": challenges, "Wins": wins,
    #             "Output Link 1": yt_link, "Output Link 2": blog_link,
    #             "Confidence End Week (1-10)": confidence, "Remark": remark, "Next Steps": next_steps
    #         }
    #         weekly = pd.concat([weekly, pd.DataFrame([new_row])], ignore_index=True)
    #         save_csv(weekly, FILES["weekly"])
    #         st.success("New Weekly entry added!")

    # # Display Expander Format
    # for _, row in weekly.iterrows():
    #     with st.expander(f"{row['Week']} {row['Start Date']} - {row['End Date']}"):
    #         st.write(f"**Duration(Days):** {row['Duration']}")
    #         st.write(f"**Key Lessons:** {row['Key Lessons']}")
    #         st.write(f"**Keynote Summary:** {row['Keynote Summary']}")
    #         st.write(f"**Challenges:** {row['Challenges']}")
    #         st.write(f"**Wins:** {row['Wins']}")
    #         st.markdown(f"📺 [YouTube Tutorial Video]({row['Output Link 1']}) | ✍️ [Medium Blog]({row['Output Link 2']})")
    #         st.write(f"Confidence Level: {row['Confidence End Week (1-10)']}/10")
    #         st.write(f"**Remark:** {row['Remark']}")
    #         st.write(f"**Next Steps:** {row['Next Steps']}")

#     # Visualization
#     if not weekly.empty:
#         fig3, ax3 = plt.subplots()
#         ax3.plot(weekly["Week"], weekly["Confidence End Week (1-10)"], marker="o", color="teal")
#         ax3.set_ylabel("Confidence Level")
#         ax3.set_ylim(0, 10)
#         plt.xticks(rotation=30, ha="right")
#         st.pyplot(fig3)


# # --- METRICS SECTION ---
# elif section == "📈 Metrics & KPIs":
#     st.header("📈 Metrics & KPIs")
#     st.dataframe(metrics)

#     # Add Metric
    # with st.form("Add Metric"):
    #     metric_name = st.text_input("Impact Metric")
    #     percent = st.number_input("Percent Achieved", 0, 100, step=1)
    #     submitted = st.form_submit_button("Add Metric")
    #     if submitted and metric_name:
    #         new_row = {"Impact Metric": metric_name, "Percent Achieved": percent}
    #         metrics = pd.concat([metrics, pd.DataFrame([new_row])], ignore_index=True)
    #         save_csv(metrics, FILES["metrics"])
    #         st.success("New Metric added!")

#     # Visualization
#     if not metrics.empty:
#         fig4, ax4 = plt.subplots()
#         ax4.bar(metrics["Impact Metric"], metrics["Percent Achieved"])
#         ax4.set_ylabel("% Achieved")
#         ax4.set_ylim(0, 100)
#         plt.xticks(rotation=30, ha="right")
#         st.pyplot(fig4)

# st.sidebar.info("Produced by: **SHAMMAH AGYARE** (WTFC 2026 Fellow)")

# st.success("Vision Board Dashboard loaded successfully! 🚀")


# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# # Load CSVs
# try:
#     goals = pd.read_csv("goals.csv")
#     activities = pd.read_csv("activities.csv")
#     weekly = pd.read_csv("weekly.csv")
#     metrics = pd.read_csv("metrics.csv")
# except FileNotFoundError:
#     st.error("One or more required CSV files (goals.csv, activities.csv, weekly_journal.csv, metrics.csv) not found. Please ensure they are in the same directory as this script.")
#     st.stop()

# st.set_page_config(page_title="Women Techsters Vision Board", layout="wide")
# st.title("📊 My Women Techsters Fellowship Vision Board")
# st.subheader("Data Science & Engineering Track")

# # --- Goals Section ---
# st.header("🎯 Goals & Phases")
# st.dataframe(goals)

# fig1, ax1 = plt.subplots()
# ax1.bar(goals["Goal"], goals["Current Progress %"])
# ax1.set_ylabel("Progress %")
# ax1.set_ylim(0, 100)
# plt.xticks(rotation=30, ha="right")
# st.pyplot(fig1)

# # --- Activities Section ---
# st.header("📝 Activities Tracker")
# st.dataframe(activities)

# status_counts = activities["Status"].value_counts()
# fig2, ax2 = plt.subplots()
# ax2.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=90)
# ax2.axis("equal")
# st.pyplot(fig2)

# # --- Weekly Journal Section ---
# st.header("📔 Weekly Journal")
# st.dataframe(weekly)

# for _, row in weekly.iterrows():
#     with st.expander(f"{row['Week']} {row['Start Date']} - {row['End Date']}"):
#         st.write(f"**Duration(Days):** {row['Duration']}")
#         st.write(f"**Key Lessons:** {row['Key Lessons']}")
#         st.write(f"**Keynote Summary:** {row['Keynote Summary']}")
#         st.write(f"**Challenges:** {row['Challenges']}")
#         st.write(f"**Wins:** {row['Wins']}")
#         #st.write(f"**📺 [YouTube Tutorial Video]:** {row['Output Link 1']}")
#         st.markdown(f"📺 [YouTube Tutorial Video]({row['Output Link 1']}) | ✍️ [Medium Blog]({row['Output Link 2']})")
#         st.write(f"Confidence Level: {row['Confidence End Week (1-10)']}/10")
#         st.write(f"**Remark:** {row['Remark']}")
#         st.write(f"**Next Steps:** {row['Next Steps']}")

# confidence_level = weekly["Confidence End Week (1-10)"].value_counts()
# fig3, ax3 = plt.subplots()
# ax3.bar(weekly["Week"], confidence_level)
# ax3.set_ylabel("Confidence level Achieved")
# ax3.set_ylim(0, 10)
# plt.xticks(rotation=30, ha="right")
# st.pyplot(fig3)


# # --- Metrics Section ---
# st.header("📈 Metrics & KPIs")
# st.dataframe(metrics)


# fig3, ax3 = plt.subplots()
# ax3.bar(metrics["Impact Metric"], metrics["Percent Achieved"])
# ax3.set_ylabel("% Achieved")
# ax3.set_ylim(0, 100)
# plt.xticks(rotation=30, ha="right")
# st.pyplot(fig3)

# st.write("Produced by: **SHAMMAH AGYARE** (WTFC 2026 Fellow)")

# st.success("Vision Board Dashboard loaded successfully! 🚀")

