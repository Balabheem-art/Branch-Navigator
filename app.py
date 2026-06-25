
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    branch_scores = pd.read_csv(r"C:\Users\Balabheem\OneDrive\Desktop\Demo\data\branch_scores.csv")
    anomaly_data  = pd.read_csv(r"C:\Users\Balabheem\OneDrive\Desktop\Demo\data\anomaly_scores.csv")
    df            = pd.read_csv(r"C:\Users\Balabheem\OneDrive\Desktop\Demo\data\df_features.csv")
    return branch_scores, anomaly_data, df

branch_scores, anomaly_data, df = load_data()

st.title("Branch Navigator — AI Dashboard")
st.markdown("**Optimize Locations with Predictive Footfall Insights**")
st.divider()

page = st.sidebar.selectbox("Select Page", [
    "Branch Overview",
    "Transaction Mix",
    "Anomaly Alerts",
    "AI Recommendation"
])

if page == "Branch Overview":
    st.header("Branch Performance Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Branches",  f"{len(branch_scores)}")
    col2.metric("High Performers", f"{len(branch_scores[branch_scores['PerformanceLabel']=='High Performer'])}")
    col3.metric("Mid Performers",  f"{len(branch_scores[branch_scores['PerformanceLabel']=='Mid Performer'])}")
    col4.metric("Low Performers",  f"{len(branch_scores[branch_scores['PerformanceLabel']=='Low Performer'])}")
    st.divider()
    st.subheader("Top 10 Performing Branches")
    top10 = branch_scores.nlargest(10, "PerformanceScore")[["Store","AvgSales","AvgCustomers","PerformanceScore","PerformanceLabel"]]
    st.dataframe(top10, use_container_width=True)
    st.subheader("Bottom 10 Performing Branches")
    bot10 = branch_scores.nsmallest(10, "PerformanceScore")[["Store","AvgSales","AvgCustomers","PerformanceScore","PerformanceLabel"]]
    st.dataframe(bot10, use_container_width=True)
    st.subheader("Performance Score Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(branch_scores["PerformanceScore"], bins=30, color="steelblue", edgecolor="white")
    ax.set_xlabel("Performance Score")
    ax.set_ylabel("Number of Branches")
    st.pyplot(fig)

elif page == "Transaction Mix":
    st.header("Transaction Mix Analysis")
    store_id = st.selectbox("Select Store", sorted(df["Store"].unique()))
    store_data = df[df["Store"] == store_id]
    trans_dist = store_data["TransactionType"].value_counts()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Store {store_id} Transaction Mix")
        fig, ax = plt.subplots()
        ax.pie(trans_dist.values, labels=trans_dist.index, autopct="%1.1f%%",
               colors=["steelblue","orange","green","red"])
        st.pyplot(fig)
    with col2:
        st.subheader("Store Stats")
        score_info = branch_scores[branch_scores["Store"] == store_id].iloc[0]
        st.metric("Performance Score", f"{score_info['PerformanceScore']}/100")
        st.metric("Avg Daily Sales",   f"£{score_info['AvgSales']:,.0f}")
        st.metric("Avg Customers",     f"{score_info['AvgCustomers']:,.0f}")
        st.metric("Performance Label", score_info["PerformanceLabel"])

elif page == "Anomaly Alerts":
    st.header("Anomaly Alerts")
    anomalies = anomaly_data[anomaly_data["Status"] == "Anomaly"]
    normal    = anomaly_data[anomaly_data["Status"] == "Normal"]
    col1, col2 = st.columns(2)
    col1.metric("Normal Branches",  len(normal))
    col2.metric("Anomaly Branches", len(anomalies))
    st.divider()
    st.subheader("Anomalous Branches")
    st.dataframe(anomalies[["Store","AvgSales","AvgCustomers","Status"]], use_container_width=True)

elif page == "AI Recommendation":
    st.header("AI Branch Recommendation")
    store_id = st.number_input("Enter Store ID", min_value=1, max_value=1115, value=5)
    if st.button("Generate AI Report"):
        store_info   = branch_scores[branch_scores["Store"] == store_id].iloc[0]
        anomaly_info = anomaly_data[anomaly_data["Store"] == store_id].iloc[0]
        store_df     = df[df["Store"] == store_id]
        score  = store_info["PerformanceScore"]
        label  = store_info["PerformanceLabel"]
        status = anomaly_info["Status"]
        col1, col2, col3 = st.columns(3)
        col1.metric("Performance Score", f"{score}/100")
        col2.metric("Performance Label", label)
        col3.metric("Anomaly Status",    status)
        st.divider()
        st.subheader("Transaction Mix")
        trans = store_df["TransactionType"].value_counts(normalize=True) * 100
        st.bar_chart(trans)
        st.divider()
        st.subheader("Root Causes Found")
        causes = []
        if store_info["AvgSales"] < 5000:
            causes.append("Below average sales")
        if store_info["AvgCustomers"] < 500:
            causes.append("Low customer footfall")
        if store_df["Promo"].mean() < 0.3:
            causes.append("Low promo usage")
        if store_df["CompetitionDistance"].mean() < 1000:
            causes.append("High competition nearby")
        if status == "Anomaly":
            causes.append("Unusual behavior detected")
        if not causes:
            causes.append("No major issues found")
        for c in causes:
            st.write("❌", c)
        st.divider()
        st.subheader("AI Recommendation")
        if score >= 80:
            st.success("Branch is Excellent — Maintain current operations")
        elif score >= 50:
            st.warning("Branch needs improvement — Launch promotional campaign")
        else:
            st.error("Urgent Action Required")
            st.write("→ Launch targeted marketing campaign")
            st.write("→ Increase promotional days to 50%")
            st.write("→ Review and increase weekend staffing")
            st.write("→ Investigate competition nearby")
            st.write("→ Consider relocation if score stays below 30")
