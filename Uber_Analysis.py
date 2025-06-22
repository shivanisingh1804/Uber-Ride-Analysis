import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit setup
st.set_page_config(page_title="Uber Data Analysis", layout="wide")
st.title("🚖 Uber Ride Data Analysis")
st.markdown("This app provides insights into Uber rides based on the uploaded dataset.")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your Uber CSV file", type=["csv"])
if uploaded_file:
    dataset = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(dataset.head())

    # Convert START_DATE to datetime and extract useful features
    dataset['START_DATE'] = pd.to_datetime(dataset['START_DATE'], errors='coerce')
    dataset = dataset.dropna(subset=['START_DATE'])

    dataset['Date'] = dataset['START_DATE'].dt.date
    dataset['Time'] = dataset['START_DATE'].dt.hour
    dataset['Month_Num'] = dataset['START_DATE'].dt.month
    dataset['Day'] = dataset['START_DATE'].dt.day_name()

    # Map months to labels
    month_label = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    dataset['Month'] = dataset['Month_Num'].map(month_label)

    # Time of day binning
    dataset['DayPeriod'] = pd.cut(
        x=dataset['Time'],
        bins=[-1, 10, 15, 19, 24],
        labels=["Morning", "Afternoon", "Evening", "Night"]
    )

    # Layout for charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ride Count by Category")
        fig1, ax1 = plt.subplots()
        sns.countplot(x='CATEGORY', data=dataset, ax=ax1)
        ax1.set_title("Ride Category Count")
        ax1.set_xlabel("Category")
        ax1.set_ylabel("Count")
        st.pyplot(fig1)

    with col2:
        st.subheader("Ride Count by Purpose")
        if 'PURPOSE' in dataset.columns:
            fig2, ax2 = plt.subplots()
            sns.countplot(x='PURPOSE', data=dataset, order=dataset['PURPOSE'].value_counts().index, ax=ax2)
            ax2.set_title("Purpose of Ride")
            ax2.set_xlabel("Purpose")
            ax2.set_ylabel("Count")
            plt.xticks(rotation=45)
            st.pyplot(fig2)
        else:
            st.warning("No 'PURPOSE' column found in the dataset.")

    # Monthly analysis
    st.subheader("📅 Monthly Ride Analysis")
    monthly_counts = dataset['Month'].value_counts().sort_index()
    df_month = pd.DataFrame({
        "Month": monthly_counts.index,
        "Ride Count": monthly_counts.values
    })

    fig3, ax3 = plt.subplots()
    sns.lineplot(x="Month", y="Ride Count", data=df_month, ax=ax3, marker='o')
    ax3.set_title("Rides per Month")
    st.pyplot(fig3)

    # Daily ride distribution
    st.subheader("📆 Ride Distribution by Day")
    day_counts = dataset['Day'].value_counts()
    fig4, ax4 = plt.subplots()
    sns.barplot(x=day_counts.index, y=day_counts.values, ax=ax4)
    ax4.set_title("Rides per Day of the Week")
    ax4.set_xlabel("Day")
    ax4.set_ylabel("Count")
    st.pyplot(fig4)

    # Day period ride distribution
    st.subheader("🕒 Ride Distribution by Time of Day")
    fig5, ax5 = plt.subplots()
    sns.countplot(x='DayPeriod', data=dataset, order=["Morning", "Afternoon", "Evening", "Night"], ax=ax5)
    ax5.set_title("Rides by Time of Day")
    ax5.set_xlabel("Day Period")
    ax5.set_ylabel("Count")
    st.pyplot(fig5)

    st.success("✅ Analysis completed. You can explore more charts or upload a new dataset.")
else:
    st.info("📁 Please upload a CSV file to begin analysis.")
