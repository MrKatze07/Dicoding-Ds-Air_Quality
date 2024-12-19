import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load the dataset
data = pd.read_csv('all_data.csv')

# Preprocess data: Aggregate yearly pollutant means
yearly_data = data.groupby(by=['year']).agg({
    'PM2.5': 'mean',
    'PM10': 'mean',
    'SO2': 'mean',
    'NO2': 'mean',
    'CO': 'mean',
    'O3': 'mean'
}).sort_values(by=['year'], ascending=True)

# Calculate percentage change from 2013 to 2017
pollutant_change = ((yearly_data.loc[2017] - yearly_data.loc[2013]) / yearly_data.loc[2013]) * 100
pollutant_change = pd.Series(pollutant_change.squeeze(), index=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']).round(2)

# Calculate percentage change in yearly
pollutant_change_yearly = yearly_data.pct_change() * 100
pollutant_change_yearly.fillna(0, inplace=True)
pollutant_change_yearly = pollutant_change_yearly.round(2)

# Station-level average pollutants
avg_pollutants = data.groupby('station')[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()

# Correlation matrix for pollutants and weather
corr_matrix = data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'RAIN', 'WSPM']].corr()

# Streamlit dashboard
st.set_page_config(page_title="Air Quality Pollution", layout="wide")
st.title("Air Quality Pollution")

# Sidebar navigation
st.sidebar.title("Navigation")
options = ["Overview", "Yearly Trends Between 2013 to 2017", "Percentage Growth in Yearly", "Highest and Lowest Station Analysis", "Correlation Analysis", "Insights"]
active_option = "Overview"  # Default option

# Sidebar button logic
for option in options:
    if st.sidebar.button(option):
        active_option = option


# Overview
if active_option == "Overview":
    st.header("Dashboard Overview")
    st.markdown(
        """This dashboard provides insights into air pollution data, including yearly trends, percentage growth pollutant in yearly, 
       highest and lowest station analysis, and correlations pollutant with weather variables. Use the navigation panel to explore each view."""
    )

if active_option == "Yearly Trends Between 2013 to 2017":
    st.header("Trend Perkembangan Polutan dari 2013 hingga 2017")
    with st.expander("**Yearly Trend Change Between 2013 to 2017**"):
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            for column in ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']:
                ax.plot(yearly_data.index, yearly_data[column], label=column, marker='o')
            ax.set_title("**Yearly Trends in Pollutants**", fontsize=16)
            ax.set_xlabel("Year", fontsize=14)
            ax.set_ylabel("Concentration", fontsize=14)
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

        with col2:
            st.write("**Trends Summary:**")
            st.write("- PM2.5 and PM10 show consistent trends.")
            st.write("- O3 levels fluctuate more than others.")

        with col3:
            st.write("**Trends Table:**")
            st.table(yearly_data)

    with st.expander("**Percentage Yearly Trend Between 2013 to 2017**"):
        st.write("**Persentase Perkembangan Trend Polutan dari 2013 hingga 2017**")
        colors = ["#DC143C" if v > 0 else "#1E90FF" for v in pollutant_change.values]
        col4, col5 = st.columns([2, 1])

        with col4:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(pollutant_change.index, pollutant_change.values, color=colors)
            ax.set_title("Percentage Change in Pollutants (2013-2017)", fontsize=12)
            ax.set_xlabel("Pollutant", fontsize=14)
            ax.set_ylabel("Percentage Change (%)", fontsize=10)
            ax.grid(axis='y')
            for i, v in enumerate(pollutant_change.values):
                ax.text(i, v, f"{v}%", ha='center', va='bottom' if v > 0 else 'top', fontsize=10)
            st.pyplot(fig)

        with col5:
            st.write("**Key Changes:**")
            for pollutant, change in pollutant_change.items():
                trend = "Increase" if change > 0 else "Decrease"
                st.write(f"- {pollutant}: {trend} of {change}%")
            
            st.table(pollutant_change)

if active_option == "Percentage Growth in Yearly":
    st.header("Persentase Perkembangan Polutan Setiap Tahunnya") 
    with st.expander("**Percentage Growth in Yearly**"):
        col1, col2 = st.columns([2, 1])
        

        with col1:
            # Create a line plot for yearly percentage changes
            fig, ax = plt.subplots(figsize=(10, 6))
            for column in pollutant_change_yearly.columns:
                ax.plot(pollutant_change_yearly.index, pollutant_change_yearly[column], label=column, marker='o')

            # Set plot title and labels
            ax.set_title('Percentage Growth per Year', fontsize=16)
            ax.set_xlabel('Year', fontsize=14)
            ax.set_ylabel('Percentage Growth (%)', fontsize=14)

            # Display legend and grid
            ax.legend(title="Pollutants")
            ax.grid(True)

            # Adjust layout to prevent clipping
            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            st.write("**Percentage Growth Table:**")
            st.table(pollutant_change_yearly)

# Highest and Lowest Station Analysis
if active_option == "Highest and Lowest Station Analysis":
    st.header("Stasiun dengan Polutan Tertinggi dan Terendah")
    with st.expander("**Highest and Lowest Station Analysis**"):
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            pollutants = avg_pollutants.columns
            highest_values = avg_pollutants.max()
            lowest_values = avg_pollutants.min()
            stations_highest = avg_pollutants.idxmax()
            stations_lowest = avg_pollutants.idxmin()

            # Bar chart for highest and lowest pollutant values
            ax.barh(pollutants, highest_values, color='crimson', alpha=0.7, label="Highest Levels")
            ax.barh(pollutants, lowest_values, color='cyan', alpha=0.7, label="Lowest Levels")

            # Add labels for stations
            for i, pollutant in enumerate(pollutants):
                ax.text(highest_values[i], i, f"{stations_highest[pollutant]} ({highest_values[i]:.2f})",
                        va='center', ha='left', fontsize=9, color='crimson')
                ax.text(lowest_values[i], i, f"{stations_lowest[pollutant]} ({lowest_values[i]:.2f})",
                        va='center', ha='right', fontsize=9, color='cyan')

            ax.set_title("Highest & Lowest Pollutant Levels by Station", fontsize=14)
            ax.set_xlabel("Pollutant Levels")
            ax.set_yticks(range(len(pollutants)))
            ax.set_yticklabels(pollutants)
            ax.legend()
            ax.grid(axis='x')
            st.pyplot(fig)
        
        with col2:
            st.write("**Highest Station-Level Table:**")
            st.table(stations_highest)
            st.write("**Lowest Station-Level Table:**")
            st.table(stations_lowest)


        with col3:
            st.write("**Station-Level Averages Table:**")
            st.table(avg_pollutants)

if active_option == "Correlation Analysis":
    st.header("Korelasi Hubungan Polutan dengan Cuaca")
    with st.expander("**Correlation Between Pollutants and Weather Variables**"):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            ax.set_title("Correlation Heatmap")
            st.pyplot(fig)

        with col2:
            st.write("**Correlation Insights:**")
            st.write("- Temperature negatively correlates with most pollutants.")
            st.write("- Wind speed generally reduces pollutant levels.")

        with col3:
            st.write("**Correlation Table:**")
            st.table(corr_matrix)

if active_option == "Insights":
    st.header("Conclusion")
    st.markdown("""
                ## Trend Kualitas Polusi dari 2013 ke 2017
                 Berdasarkan analisis data, perkembangan trend kualitas polusi untuk **PM2.5**, **PM10**, **NO2**, dan **CO** dari tahun 2013 ke 2017 mengalami **kenaikan**, sedangkan **SO2** dan **O3** mengalami **penurunan**. Berikut adalah perubahan persentase secara berurutan:
                - **CO** mengalami kenaikan sebanyak **31.73%**.
                - **PM2.5** mengalami kenaikan sebanyak **15.54%**.
                - **NO2** mengalami kenaikan sebanyak **9.03%**.
                - **PM10** mengalami kenaikan sebanyak **7.97%**.
                - **SO2** mengalami penurunan sebanyak **-9.35%**.
                - **O3** mengalami penurunan sebanyak **-29.89%**.

                ## Perkembangan Trend Kualitas Polusi Tiap Tahunnya
                  Berdasarkan analisis data, perkembangan tiap tahun menunjukkan hal-hal berikut:
                - **2014** merupakan titik awal kenaikan persentase pada setiap polutan. Pada tahun ini, semuanya mengalami kenaikan, dengan peningkatan terbesar terjadi pada **PM10 (12.67%)** dan **PM2.5 (6.72%)**.
                - **2015** mengalami penurunan signifikan pada sebagian besar polutan, terkecuali pada **CO** yang mengalami peningkatan sedikit sebanyak **CO (0.11%)** dan **O3 (1.60%)**.
                - **2016** melanjutkan penurunan sebagian besar polutan, namun tidak separah tahun 2015.
                - **2017** merupakan tahun dengan peningkatan polutan yang sangat signifikan.

                ## Stasiun dengan Tingkat Pollutan Tertinggi dan Terendah
                  Berdasarkan analisis data, **stasiun dengan polutan tertinggi** adalah **Dongsi** dan **stasiun dengan polutan terendah** adalah **Dingling**.

                ## Korelasi Tingkat Polusi dengan Cuaca
                  Berdasarkan analisis data, berikut adalah korelasi antara tingkat polusi dan cuaca:
                - **Suhu** memiliki korelasi negatif dengan sebagian besar polutan lainnya dan korelasi positif yang kuat pada **O3**.
                - **Tekanan** memiliki korelasi positif yang lemah dengan sebagian besar polutan dan korelasi negatif kuat pada **O3**.
                - **Hujan** memiliki korelasi negatif yang lemah dengan sebagian besar polutan.
                - **Kecepatan angin** memiliki korelasi negatif pada sebagian besar polutan dan korelasi positif yang cukup kuat pada **O3**.
                
                Secara keseluruhan, **suhu** dan **angin** memiliki pengaruh yang lebih besar terhadap **kenaikan konsentrasi polutan**, sedangkan **tekanan** dan **hujan** memiliki pengaruh yang lebih lemah."""
                )


