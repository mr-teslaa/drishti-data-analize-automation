from flask import Blueprint
from flask import render_template
import pandas as pd
import numpy as np
import re

# import pdfkit
from flask import send_file
main = Blueprint('main', __name__)

@main.route("/")
def home():
    ########## START Weather Data ##########

    # --------------------------------------- #
    # -- ANALYZE Automatic Weather Station -- #
    # --------------------------------------- #

    # Read the CSV file into a DataFrame
    weather_csv_file = "AutomaticWeatherStation_Data_List12Jun23.csv"
    weather_df = pd.read_csv(weather_csv_file, skiprows=3)

    # Define the columns for analysis
    weather_columns = [
        "Solar_Radiation (W/m2)",
        "Wind_Direction_max",
        "Relative_Humidity (%RH)",
        "Atmospheric_Temp (DegC)",
        "Air_Pressure (hPa)",
        "Wind_Speed_max (km/h)"
    ]

    # Calculate the statistics
    weather_statistics = {
        "Weather Parameter": [],
        "Maximum": [],
        "Minimum": [],
        "Average": [],
        "Standard Deviation": []
    }

    for weather_column in weather_columns:
        # Calculate the maximum, minimum, average, and standard deviation for each column
        maximum = weather_df[weather_column].max()
        minimum = weather_df[weather_column].min()
        average = weather_df[weather_column].mean()
        std_dev = weather_df[weather_column].std()

        # Store the weather statistics in the dictionary
        weather_statistics["Weather Parameter"].append(weather_column)
        weather_statistics["Maximum"].append(maximum)
        weather_statistics["Minimum"].append(minimum)
        weather_statistics["Average"].append(average)
        weather_statistics["Standard Deviation"].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    weather_datas = pd.DataFrame(weather_statistics)

    ########## END Weather Data ##########


    ########## START Laser Data ##########
    
    # --------------------------------------- #
    # -- ANALYZE Laser Data ----------------- #
    # --------------------------------------- #

    # Read the CSV file into a DataFrame
    laser_csv_file = "TallahROBLaser_Data_List16Jun23.csv"
    laser_df = pd.read_csv(laser_csv_file, skiprows=3)

    # Define the columns we need to calculate
    laser_columns = [
        'A1_Concrete_LS1_1',
        'A1-P1_Steel_LS2_2',
        'P1-P2_LS3_3',
        'P2-P3_LS4_4',
        'P3-P4_LS5_5',
        'P4-P5_LS6_6',
        'CP1-P5 RHS_LS7_7',
        'CP1-P5_LHS_LS8_1',
        'CP1-P6_RHS_LS9_2',
        'CP1-P6_LHS_LS10_3',
        'P6-P7_RHS_LS11_4',
        'P6-P7_LHS_LS12_5',
        'P7-P8_RHS_LS13_6',
        'P7-P8_LHS_LS14_7',
        'P8-P9_RHS_LS15_7',
        'P8-P9_LHS_LS16_6',
        'P9-CP2_RHS_LS17_5',
        'P9-CP2_LHS_LS18_4',
        'CP2-P10_RHS_LS19_3',
        'CP2-P10_LHS_LS20_2',
        'P10-P11_LS21_1',
        'P11-P12_LS22_5',
        'P12-P13_LS23_4',
        'P13-P14_LS24_3',
        'P14-A2_Steel_LS25_2',
        'P14-A2_Concrete_LS26_1',
        'A3-P21_Concrete_LS27_1',
        'A3-P21_Steel_LS28_2',
        'P21-P20_LS29_3',
        'P20-P19_LS30_4',
        'P19-P18_LS31_5',
        'P-17-P16_LS33_7'
    ]

    # Initialize an empty list to store the calculated results
    laser_datas = []

    # Loop over the rows in the table
    for index, row in laser_df.iterrows():
        # Initialize a dictionary to store the results for this row
        row_results = {}

        # Loop over the columns and calculate min, max, avg, and std
        for laser_column in laser_columns:
            # Find the correct deflection column based on the LS number
            # ls_number = int(''.join(filter(str.isdigit, column.split("_LS")[-1])))
            ls_number = re.search(r'LS(\d+)', laser_column).group(1)
            deflection_column = f"Deflection_{ls_number}"

            # Grab the data for the current column and deflection column
            column_values = row[laser_column]
            deflection_values = row[deflection_column]

            # Calculate the min, max, avg, and std for the column and deflection
            column_min = np.min(column_values)
            column_max = np.max(column_values)
            column_avg = np.mean(column_values)
            column_std = np.std(column_values)

            deflection_min = np.min(deflection_values)
            deflection_max = np.max(deflection_values)
            deflection_avg = np.mean(deflection_values)
            deflection_std = np.std(deflection_values)

            # Add the results to the dictionary
            row_results[laser_column] = {
                "Min": column_min,
                "Max": column_max,
                "Avg": column_avg,
                "Std": column_std
            }

            row_results[deflection_column] = {
                "Min": deflection_min,
                "Max": deflection_max,
                "Avg": deflection_avg,
                "Std": deflection_std
            }

        # Append the row results to the overall results list
        laser_datas.append(row_results)
    ########## END Laser Data ##########


    ########## START Temperature Meter Data ##########

    # --------------------------------------- #
    # -- ANALYZE Temperature Meter ---------- #
    # --------------------------------------- #

    temprature_meter_csv_files = [
        "Tallah_ROB_P6_P8_DL2-DataList23Jun23.csv",
        "Tallah_ROB_P9_A2_DL4-DataList23Jun23.csv"
    ]

    # Define the columns for analysis
    temprature_columns = [
        "CP1_TM_Axis_A",
        "CP1_TM_Axis_B",
        "CP2_TM_Axis_A",
        "CP2_TM_Axis_B"
    ]

    # Calculate the statistics
    temprature_statistics = {
        "Sensor's Tag.": [],
        "Maximum": [],
        "Minimum": [],
        "Average": [],
        "Standard Deviation": []
    }
    # Iterate over each CSV file
    for csv_file in temprature_meter_csv_files:
        # Read the CSV file into a DataFrame
        temprature_meter_df = pd.read_csv(csv_file, skiprows=3)

        # Calculate the statistics for each column
        for temprature_column in temprature_columns:
            if temprature_column in temprature_meter_df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = temprature_meter_df[temprature_column].max()
                minimum = temprature_meter_df[temprature_column].min()
                average = temprature_meter_df[temprature_column].mean()
                std_dev = temprature_meter_df[temprature_column].std()

                # Store the statistics in the dictionary
                temprature_statistics["Sensor's Tag."].append(temprature_column)
                temprature_statistics["Maximum"].append(maximum)
                temprature_statistics["Minimum"].append(minimum)
                temprature_statistics["Average"].append(average)
                temprature_statistics["Standard Deviation"].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    temprature_meter_datas = pd.DataFrame(temprature_statistics)
    
    ########## END Temperature Meter Data ##########
    

    ########## START Tilt Meter Data ##########

    # --------------------------------------- #
    # -- ANALYZE Tilt Meter ---------------- #
    # --------------------------------------- #

    tilt_meter_csv_files = [
        "Tallah_ROB_A1_P7_DL1-DataList23Jun23.csv",
        "Tallah_ROB_P9_A2_DL4-DataList23Jun23.csv"
    ]

    # Define the columns for analysis
    tilt_meter_columns = [
        "CP1_TM_Axis_A",
        "CP1_TM_Axis_B",
        "CP2_TM_Axis_A",
        "CP2_TM_Axis_B"
    ]

    # Calculate the statistics
    tilt_meter_statistics = {
        "Sensor's Tag.": [],
        "Maximum": [],
        "Minimum": [],
        "Average": [],
        "Standard Deviation": []
    }
    # Iterate over each CSV file
    for tilt_meter_csv_file in tilt_meter_csv_files:
        # Read the CSV file into a DataFrame
        tilt_meter_df = pd.read_csv(tilt_meter_csv_file, skiprows=3)

        # Calculate the statistics for each column
        for tilt_meter_column in tilt_meter_columns:
            if tilt_meter_column in tilt_meter_df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = tilt_meter_df[tilt_meter_column].max()
                minimum = tilt_meter_df[tilt_meter_column].min()
                average = tilt_meter_df[tilt_meter_column].mean()
                std_dev = tilt_meter_df[tilt_meter_column].std()

                # Store the statistics in the dictionary
                tilt_meter_statistics["Sensor's Tag."].append(tilt_meter_column)
                tilt_meter_statistics["Maximum"].append(maximum)
                tilt_meter_statistics["Minimum"].append(minimum)
                tilt_meter_statistics["Average"].append(average)
                tilt_meter_statistics["Standard Deviation"].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    tilt_meter_datas = pd.DataFrame(tilt_meter_statistics)

    ########## END Tilt Meter Data ##########


    ########## START LDVT Data ##########

    # --------------------------------------- #
    # -- ANALYZE LDVT ----------------------- #
    # --------------------------------------- #

    ldvt_csv_files = [
        "Tallah_ROB_A1_P7_DL1-DataList23Jun23.csv",
        "Tallah_ROB_P6_P8_DL2-DataList23Jun23.csv",
        "Tallah_ROB_P7_CP2_DL3-DataList23Jun23.csv",
        "Tallah_ROB_P9_A2_DL4-DataList23Jun23.csv",
        "Tallah_ROB_P16_A3_DL5-DataList23Jun23.csv"
    ]

    # Define the columns for analysis
    ldvt_columns = [
        "P6_BS1_FF_D_Displacement",
        "P6_BS1_LGS_D_Displacement",
        "P6_BS2_LGS_D_Displacement",
        "P6_BS2_FF_D_Displacement",
        "P3_D1_Displacement",
        "P3_D2_Displacement",
        "P3_D3_Displacement",
        "P3_D4_Displacement",
        "P3_D5_Displacement",
        "P3_D6_Displacement",
        "P3_D7_Displacement",
        "P3_D8_Displacement",
        "P4_D1_Displacement",
        "P4_D2_Displacement",
        "P4_D3_Displacement",
        "P4_D4_Displacement",
        "P4_D5_Displacement",
        "P4_D6_Displacement",
        "P4_D7_Displacement",
        "P4_D8_Displacement",
        "P7_BS1_TGS_Displacement",
        "P7_BS1_FX_Displacement",
        "P7_BS2_FX_Displacement",
        "P7_P8_BS3_FF_Displacement",
        "P7_P8_BS3_LGS_Displacement",
        "P7_P8_BS4_LGS_Displacement",
        "P7_BS4_FX_Displacement",
        "P7_BS2_TGS_Displacement",
        "P8_D1_Displacement",
        "P8_D2_Displacement",
        "P8_D3_Displacement",
        "P8_D4_Displacement",
        "P9_D1_Displacement",
        "P9_D2_Displacement",
        "P9_D3_Displacement",
        "P9_D4_Displacement",
        "CP2_BS5_TGS_D_Displacement",
        "CP2_BS5_FX_D_Displacement",
        "CP_BS6_FX_D_Displacement",
        "CP2_BS6_TGS_D_Displacement",
        "P12_D1_Displacement",
        "P12_D2_Displacement",
        "P12_D3_Displacement",
        "P12_D4_Displacement",
        "P12_D5_Displacement",
        "P12_D6_Displacement",
        "P12_D7_Displacement",
        "P12_D8_Displacement",
        "P11_D1_Displacement",
        "P11_D2_Displacement",
        "P11_D3_Displacement",
        "P11_D4_Displacement",
        "P11_D5_Displacement",
        "P11_D6_Displacement",
        "P11_D7_Displacement",
        "P11_D8_Displacement",
        "P18_D1_Displacement",
        "P18_D2_Displacement",
        "P18_D3_Displacement",
        "P18_D4_Displacement",
        "P17_D1_Displacement",
        "P17_D2_Displacement",
        "P17_D3_Displacement",
        "P17_D4_Displacement"
    ]

    # Calculate the statistics
    ldvt_statistics = {
        "Sensor's Tag.": [],
        "MAX. (deg C)": [],
        "MIN. (deg C)": [],
        "AVG. (deg C)": [],
        "SD. (deg C)": []
    }

    # Iterate over each CSV file
    for ldvt_csv_file in ldvt_csv_files:
        # Read the CSV file into a DataFrame
        ldvt_df = pd.read_csv(ldvt_csv_file, skiprows=3)

        # Calculate the statistics for each column
        for ldvt_column in ldvt_columns:
            if ldvt_column in ldvt_df.columns:
                # print(column, " -- ", csv_file)
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = ldvt_df[ldvt_column].max()
                minimum = ldvt_df[ldvt_column].min()
                average = ldvt_df[ldvt_column].mean()
                std_dev = ldvt_df[ldvt_column].std()

                # Store the statistics in the dictionary
                ldvt_statistics["Sensor's Tag."].append(ldvt_column)
                ldvt_statistics["MAX. (deg C)"].append(maximum)
                ldvt_statistics["MIN. (deg C)"].append(minimum)
                ldvt_statistics["AVG. (deg C)"].append(average)
                ldvt_statistics["SD. (deg C)"].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    ldvt_datas = pd.DataFrame(ldvt_statistics)

    ########## END LDVT Data ##########

                
    return render_template(
        "home.html", 
        weather_datas=weather_datas, laser_datas=laser_datas,
        temprature_meter_datas=temprature_meter_datas, 
        tilt_meter_datas=tilt_meter_datas, ldvt_datas=ldvt_datas
    )