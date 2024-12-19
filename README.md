# Air_Quality DS
# Project Overview
  This project, submitted for the "Learn Data Analysis with Python" course from Dicoding, focuses on analysis Air_Quality chinese station data which is objective to analysis about Yearly Trends Changes Between 2013 to 2017, Percentage Growth Pollutant in Yearly, highest and lowest station analysis, and correlations pollutant with weather variables

# Variable Description
  - PM2.5 = Particulate matter (PM) with a diameter of 2.5 micrometers or less
  - PM10  = Particulate matter (PM) with a diameter of 10 micrometers or less
  - SO2 = Sulfur dioxide concentration
  - NO2 = Nitrogen dioxide concentration
  - CO  = Carbon monoxide concentration
  - O3  = Ozone concentration
  - Temp  = Temperature in degrees Celsius
  - Pres  = Atmospheric pressure
  - DEWP  = Dew point
  - Rain  = Rainfall amount
  - Wd    = Direction of wind
  - WSPM  = Speed of wind

# How To Run Dashboard
 1. Setup Requirement
    ```
    pip install pandas numpy scipy matplotlib seaborn pymannkendall scipy streamlit
    pipenv install
    pipenv shell
    pip install -r requirements.txt
    ```
2. Run dashboard
   ```
   cd dashboard
   streamlit run dashboard.py
   ```
# Url Dashboard
  https://dicoding-ds-airquality-dnat8vtydwmn8xttc6zlcw.streamlit.app/

  Note: Since my dashboard does work in local and not work in deploy streamlit. i got error when i put csv data and dashboard.py in same folder dasboard, so i change the code in this part :
  data = pd.read_csv('all_data.csv') > in local test before deploy
  data = pd.read_csv('dashboard/all_data.csv') to deploy dashboard on streamlit
  
