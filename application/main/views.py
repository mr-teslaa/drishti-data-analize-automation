################################################
#### TABLE OF CONTENT   #######################
#### 1. Weather Data
#### 2. Laser Data
#### 3. Temperature Meter Data
#### 1. Tilt Meter
#### 1. LDVT Data
#### 1. Weather Data
#### 1. Weather Data
#### 1. Weather Data
 
################################################

from flask import Blueprint
from flask import render_template
import pandas as pd
import numpy as np
import re

# import pdfkit
from flask import send_file
main = Blueprint('main', __name__)

# DEFINING THE CSV FILES
weather_csv = "AutomaticWeatherStation_Data_List.csv"
laser_csv = "TallahROBLaser_Data_List.csv"
dl = [
    "Tallah_ROB_A1_P7_DL1-DataList.csv",
    "Tallah_ROB_P6_P8_DL2-DataList.csv",
    "Tallah_ROB_P7_CP2_DL3-DataList.csv",
    "Tallah_ROB_P9_A2_DL4-DataList.csv",
    "Tallah_ROB_P16_A3_DL5-DataList.csv"
]

@main.route("/")
def home():
    ########## START Weather Data ##########

    # --------------------------------------- #
    # -- ANALYZE Automatic Weather Station -- #
    # --------------------------------------- #

    # Read the CSV file into a DataFrame
    weather_csv_file = weather_csv
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
    laser_csv_file = laser_csv
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

    # DEFINE THRESHOLD VALUE
    threshold_values = {
        'A1_Concrete_LS1_1': 35.2,
        'A1-P1_Steel_LS2_2': 35.2,
        'P1-P2_LS3_3': 35.2,
        'P2-P3_LS4_4': 35.2,
        'P3-P4_LS5_5': 35.2,
        'P4-P5_LS6_6': 35.2,
        'CP1-P5 RHS_LS7_7': 27.4,
        'CP1-P5_LHS_LS8_1': 27.4,
        'CP1-P6_RHS_LS9_2': 37.5,
        'CP1-P6_LHS_LS10_3': 37.5,
        'P6-P7_RHS_LS11_4': 62.5,
        'P6-P7_LHS_LS12_5': 62.5,
        'P7-P8_RHS_LS13_6': 62.5,
        'P7-P8_LHS_LS14_7': 65.2,
        'P8-P9_RHS_LS15_7': 31.5,
        'P8-P9_LHS_LS16_6': 31.5,
        'P9-CP2_RHS_LS17_5': 35.2,
        'P9-CP2_LHS_LS18_4': 35.2,
        'CP2-P10_RHS_LS19_3': 35.2,
        'CP2-P10_LHS_LS20_2': 35.2,
        'P10-P11_LS21_1': 35.2,
        'P11-P12_LS22_5': 35.2,
        'P12-P13_LS23_4': 35.2,
        'P13-P14_LS24_3': 35.2,
        'P14-A2_Steel_LS25_2': 35.2,
        'P14-A2_Concrete_LS26_1': 21.4,
        'A3-P21_Concrete_LS27_1': 22.9,
        'A3-P21_Steel_LS28_2': 22.9,
        'P21-P20_LS29_3': 22.9,
        'P20-P19_LS30_4': 35.2,
        'P19-P18_LS31_5': 35.2,
        'P-17-P16_LS33_7': 10.5
    }

    # Initialize an empty list to store the calculated results
    laser_datas = []

    # Loop over the rows in the table
    for index, row in laser_df.iterrows():
        # Initialize a dictionary to store the results for this row
        row_results = {}

        # Loop over the columns and calculate min, max, avg, and std
        for laser_column in laser_columns:
            # Find the correct deflection column based on the LS number
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

            # Add the threshold value for the column
            threshold_value = threshold_values.get(laser_column)

            # Add the results to the dictionary
            row_results[laser_column] = {
                "Min": column_min,
                "Max": column_max,
                "Avg": column_avg,
                "Std": column_std,
                "Threshold": threshold_value
            }

            row_results[deflection_column] = {
                "Min": deflection_min,
                "Max": deflection_max,
                "Avg": deflection_avg,
                "Std": deflection_std,
                "Threshold": threshold_value
            }


        # Append the row results to the overall results list
        laser_datas.append(row_results)
    ########## END Laser Data ##########


    ########## START Temperature Meter Data ##########

    # --------------------------------------- #
    # -- ANALYZE Temperature Meter ---------- #
    # --------------------------------------- #

    temprature_meter_csv_files = [
        dl[1],
        dl[3]
        # "Tallah_ROB_P6_P8_DL2-DataList23Jun23.csv",
        # "Tallah_ROB_P9_A2_DL4-DataList23Jun23.csv"
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
        dl[0],
        dl[3]
        # "Tallah_ROB_A1_P7_DL1-DataList23Jun23.csv",
        # "Tallah_ROB_P9_A2_DL4-DataList23Jun23.csv"
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
        dl[0],
        dl[1],
        dl[2],
        dl[3],
        dl[4],
        # "Tallah_ROB_A1_P7_DL1-DataList23Jun23.csv",
        # "Tallah_ROB_P6_P8_DL2-DataList23Jun23.csv",
        # "Tallah_ROB_P7_CP2_DL3-DataList23Jun23.csv",
        # "Tallah_ROB_P9_A2_DL4-DataList23Jun23.csv",
        # "Tallah_ROB_P16_A3_DL5-DataList23Jun23.csv"
    ]

    # Define the columns for analysis
    # ldvt_columns = [
    #     "P6_BS1_FF_D_Displacement",
    #     "P6_BS1_LGS_D_Displacement",
    #     "P6_BS2_LGS_D_Displacement",
    #     "P6_BS2_FF_D_Displacement",
    #     "P3_D1_Displacement",
    #     "P3_D2_Displacement",
    #     "P3_D3_Displacement",
    #     "P3_D4_Displacement",
    #     "P3_D5_Displacement",
    #     "P3_D6_Displacement",
    #     "P3_D7_Displacement",
    #     "P3_D8_Displacement",
    #     "P4_D1_Displacement",
    #     "P4_D2_Displacement",
    #     "P4_D3_Displacement",
    #     "P4_D4_Displacement",
    #     "P4_D5_Displacement",
    #     "P4_D6_Displacement",
    #     "P4_D7_Displacement",
    #     "P4_D8_Displacement",
    #     "P7_BS1_TGS_Displacement",
    #     "P7_BS1_FX_Displacement",
    #     "P7_BS2_FX_Displacement",
    #     "P7_P8_BS3_FF_Displacement",
    #     "P7_P8_BS3_LGS_Displacement",
    #     "P7_P8_BS4_LGS_Displacement",
    #     "P7_BS4_FX_Displacement",
    #     "P7_BS2_TGS_Displacement",
    #     "P8_D1_Displacement",
    #     "P8_D2_Displacement",
    #     "P8_D3_Displacement",
    #     "P8_D4_Displacement",
    #     "P9_D1_Displacement",
    #     "P9_D2_Displacement",
    #     "P9_D3_Displacement",
    #     "P9_D4_Displacement",
    #     "CP2_BS5_TGS_D_Displacement",
    #     "CP2_BS5_FX_D_Displacement",
    #     "CP_BS6_FX_D_Displacement",
    #     "CP2_BS6_TGS_D_Displacement",
    #     "P12_D1_Displacement",
    #     "P12_D2_Displacement",
    #     "P12_D3_Displacement",
    #     "P12_D4_Displacement",
    #     "P12_D5_Displacement",
    #     "P12_D6_Displacement",
    #     "P12_D7_Displacement",
    #     "P12_D8_Displacement",
    #     "P11_D1_Displacement",
    #     "P11_D2_Displacement",
    #     "P11_D3_Displacement",
    #     "P11_D4_Displacement",
    #     "P11_D5_Displacement",
    #     "P11_D6_Displacement",
    #     "P11_D7_Displacement",
    #     "P11_D8_Displacement",
    #     "P18_D1_Displacement",
    #     "P18_D2_Displacement",
    #     "P18_D3_Displacement",
    #     "P18_D4_Displacement",
    #     "P17_D1_Displacement",
    #     "P17_D2_Displacement",
    #     "P17_D3_Displacement",
    #     "P17_D4_Displacement"
    # ]

    # Define Threshold value for LVDT
    ldvt_columns = {
        "P6_BS1_FF_D_Displacement": 92.5,
        "P6_BS1_LGS_D_Displacement": 92.5,
        "P6_BS2_LGS_D_Displacement": 92.5,
        "P6_BS2_FF_D_Displacement": 92.5,
        "P3_D1_Displacement": 30,
        "P3_D2_Displacement": 30,
        "P3_D3_Displacement": 30,
        "P3_D4_Displacement": 30,
        "P3_D5_Displacement": 30,
        "P3_D6_Displacement": 30,
        "P3_D7_Displacement": 30,
        "P3_D8_Displacement": 30,
        "P4_D1_Displacement": 10,
        "P4_D2_Displacement": 10,
        "P4_D3_Displacement": 10,
        "P4_D4_Displacement": 10,
        "P4_D5_Displacement": 10,
        "P4_D6_Displacement": 10,
        "P4_D7_Displacement": 10,
        "P4_D8_Displacement": 10,
        "P7_BS1_TGS_Displacement": 35,
        "P7_BS1_FX_Displacement": 1,
        "P7_BS2_FX_Displacement": 1,
        "P7_P8_BS3_FF_Displacement": 92.5,
        "P7_P8_BS3_LGS_Displacement": 92.5,
        "P7_P8_BS4_LGS_Displacement": 92.5,
        "P7_BS4_FX_Displacement": 1,
        "P7_BS2_TGS_Displacement": 35,
        "P8_D1_Displacement": 35,
        "P8_D2_Displacement": 1,
        "P8_D3_Displacement": 1,
        "P8_D4_Displacement": 35,
        "P9_D1_Displacement": 92.5,
        "P9_D2_Displacement": 92.5,
        "P9_D3_Displacement": 92.5,
        "P9_D4_Displacement": 92.5,
        "CP2_BS5_TGS_D_Displacement": 35,
        "CP2_BS5_FX_D_Displacement": 1,
        "CP_BS6_FX_D_Displacement": 1,
        "CP2_BS6_TGS_D_Displacement": 35,
        "P12_D1_Displacement": 10,
        "P12_D2_Displacement": 10,
        "P12_D3_Displacement": 10,
        "P12_D4_Displacement": 1,
        "P12_D5_Displacement": 1,
        "P12_D6_Displacement": 10,
        "P12_D7_Displacement": 10,
        "P12_D8_Displacement": 10,
        "P11_D1_Displacement": 10,
        "P11_D2_Displacement": 10,
        "P11_D3_Displacement": 10,
        "P11_D4_Displacement": 1,
        "P11_D5_Displacement": 1,
        "P11_D6_Displacement": 10,
        "P11_D7_Displacement": 10,
        "P11_D8_Displacement": 10,
        "P18_D1_Displacement": 10,
        "P18_D2_Displacement": 30,
        "P18_D3_Displacement": 30,
        "P18_D4_Displacement": 30,
        "P17_D1_Displacement": 30,
        "P17_D2_Displacement": 1,
        "P17_D3_Displacement": 1,
        "P17_D4_Displacement": 10
    }

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


    ########## START Strain Gauges Data ##########

    # --------------------------------------- #
    # ------------ PART 1 ------------------- #
    # -- ANALYZE Strain Gauges -------------- #
    # -- Shayam bazar Viaduct RHS & LHS ----- #
    # --------------------------------------- #
    shayam_bazar_viaduct_csv_files = [
        dl[0]
        # "Tallah_ROB_A1_P7_DL1-DataList23Jun23.csv"
    ]

    # Define the columns for analysis
    shayam_bazar_viaduct_RHS_columns = [
        "A1_RBLG_SG_1_Strain",
        "SA1P1_RBLG_SG_1_Strain",
        "SP1P2_RBLG_SG_1_Strain",
        "SP2P3_RBLG_SG_1_Strain",
        "SP3P4_RBLG_SG_1_Strain",
        "SP4P5_RBLG_SG_1_Strain",
        "SP5CP1_RBLG_SG_1_Strain"
    ]

    shayam_bazar_viaduct_LHS_columns = [
        "A1_LBLG_SG_2_Strain",
        "SA1P1_LBLG_SG_2_Strain",
        "SP1P2_LBLG_SG_2_Strain",
        "SP2P3_LBLG_SG_2_Strain",
        "SP3P4_LBLG_SG_2_Strain",
        "SP4P5_LBLG_SG_2_Strain",
        "SP5CP1_LBLG_SG_2_Strain"
    ]

    # Calculate the statistics
    shayam_bazar_viaduct_RHS_statistics = {
        "Instrument Tag No.": [],
        "MAX.": [],
        "MIN.": [],
        "AVG.": [],
        "SD.": []
    }

    shayam_bazar_viaduct_LHS_statistics = {
        "Instrument Tag No.": [],
        "MAX.": [],
        "MIN.": [],
        "AVG.": [],
        "SD.": []
    }

    # Iterate over each CSV file
    for csv_file in shayam_bazar_viaduct_csv_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, skiprows=3)

        # Calculate the statistics for each column
        for column in shayam_bazar_viaduct_RHS_columns:
            if column in df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = df[column].max()
                minimum = df[column].min()
                average = df[column].mean()
                std_dev = df[column].std()

                # Store the statistics in the dictionary
                shayam_bazar_viaduct_RHS_statistics["Instrument Tag No."].append(column)
                shayam_bazar_viaduct_RHS_statistics["MAX."].append(maximum)
                shayam_bazar_viaduct_RHS_statistics["MIN."].append(minimum)
                shayam_bazar_viaduct_RHS_statistics["AVG."].append(average)
                shayam_bazar_viaduct_RHS_statistics["SD."].append(std_dev)

        # Calculate the statistics for each column
        for column in shayam_bazar_viaduct_LHS_columns:
            if column in df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = df[column].max()
                minimum = df[column].min()
                average = df[column].mean()
                std_dev = df[column].std()

                # Store the statistics in the dictionary
                shayam_bazar_viaduct_LHS_statistics["Instrument Tag No."].append(column)
                shayam_bazar_viaduct_LHS_statistics["MAX."].append(maximum)
                shayam_bazar_viaduct_LHS_statistics["MIN."].append(minimum)
                shayam_bazar_viaduct_LHS_statistics["AVG."].append(average)
                shayam_bazar_viaduct_LHS_statistics["SD."].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    shayam_bazar_viaduct_RHS_statistics_datas = pd.DataFrame(shayam_bazar_viaduct_RHS_statistics)
    shayam_bazar_viaduct_LHS_statistics_datas = pd.DataFrame(shayam_bazar_viaduct_LHS_statistics)



    # --------------------------------------- #
    # ------------ PART 2 ------------------- #
    # -- ANALYZE Strain Gauges -------------- #
    # -- P6-P7 LHS - BS1 -------------------- #
    # --------------------------------------- #

    P6_P7_BS1_csv_files  = [
        dl[0],
        dl[1]
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_A1_P7_DL1-DataList.csv",
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P6_P8_DL2-DataList.csv"
    ]

    # Define the columns for analysis
    P6_P7_BS1_LHS_columns = [
        "SP6P7_BS1R_HAJ_SG_1_Strain",
        "SP6P7_BS1R_HAJ_SG_2_Strain",
        "SP6P7_BS1R_HAJ_SG_3_Strain",
        "SP6P7_BS1R_AAJ_SG_1_Strain",
        "SP6P7_BS1R_AAJ_SG_2_Strain",
        "SP6P7_BS1R_AAJ_SG_3_Strain",
        "SP6P7_BS1R_HBLBJ_SG1_Strain",
        "SP6P7_BS1R_HBLBJ_SG2_Strain",
        "SP6P7_BS1R_HBLBJ_SG3_Strain",
        "SP6P7_BS1R_BLBJ_SG_1_Strain",
        "SP6P7_BS1R_BLBJ_SG_2_Strain",
        "SP6P7_BS1R_BLBJ_SG_3_Strain",
        "SP6P7_BS1L_HAJ_SG_1_Strain",
        "SP6P7_BS1L_HAJ_SG_2_Strain",
        "SP6P7_BS1L_HAJ_SG_3_Strain",
        "SP6P7_BS1L_AAJ_SG_1_Strain",
        "SP6P7_BS1L_AAJ_SG_2_Strain",
        "SP6P7_BS1L_AAJ_SG_3_Strain",
        "SP6P7_BS1L_HBLBJ_SG1_Strain",
        "SP6P7_BS1L_HBLBJ_SG2_Strain",
        "SP6P7_BS1L_HBLBJ_SG3_Strain",
        "SP6P7_BS1L_BLBJ_SG_1_Strain",
        "SP6P7_BS1L_BLBJ_SG_2_Strain",
        "SP6P7_BS1L_BLBJ_SG3_Strain",
        "P6_BS1L_NJ_SG_1_Strain",
        "P6_BS1R_NJ_SG_2_Strain",
        "P7_BS1L_NJ_SG_3_Strain",
        "P7_BS1R_NJ_SG_4_Strain"
    ]

    P6_P7_BS1_LHS_statistics = {
        "Instrument Tag No.": [],
        "MAX.": [],
        "MIN.": [],
        "AVG.": [],
        "SD.": []
    }

    # Iterate over each CSV file
    for csv_file in P6_P7_BS1_csv_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, skiprows=3)

        # Calculate the statistics for each column
        for column in P6_P7_BS1_LHS_columns:
            if column in df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = df[column].max()
                minimum = df[column].min()
                average = df[column].mean()
                std_dev = df[column].std()

                # Store the statistics in the dictionary
                P6_P7_BS1_LHS_statistics["Instrument Tag No."].append(column)
                P6_P7_BS1_LHS_statistics["MAX."].append(maximum)
                P6_P7_BS1_LHS_statistics["MIN."].append(minimum)
                P6_P7_BS1_LHS_statistics["AVG."].append(average)
                P6_P7_BS1_LHS_statistics["SD."].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    P6_P7_BS1_LHS_statistics_datas = pd.DataFrame(P6_P7_BS1_LHS_statistics)


    # --------------------------------------- #
    # ------------ PART 3 ------------------- #
    # -- ANALYZE Strain Gauges -------------- #
    # -- P6-P7 LHS - BS3 -------------------- #
    # --------------------------------------- #

    P6_P7_BS3_csv_files = [
        dl[1],
        dl[2]
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P6_P8_DL2-DataList.csv",
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P7_CP2_DL3-DataList.csv"
    ]

    # Define the columns for analysis
    P6_P7_BS3_LHS_columns = [
        "SP7P8_BS3R_HAJ_SG_1_Strain",
        "SP7P8_BS3R_HAJ_SG_2_Strain",
        "SP7P8_BS3R_HAJ_SG_3_Strain",
        "SP7P8_BS3R_AAJ_SG_1_Strain",
        "SP7P8_BS3R_AAJ_SG_2_Strain",
        "SP7P8_BS3R_AAJ_SG_3_Strain",
        "SP7P8_BS3R_HBLBJ_SG1_Strain",
        "SP7P8_BS3R_HBLBJ_SG2_Strain",
        "SP7P8_BS3R_HBLBJ_SG3_Strain",
        "SP7P8_BS3R_BLBJ_SG_1_Strain",
        "SP7P8_BS3R_BLBJ_SG_2_Strain",
        "SP7P8_BS3R_BLBJ_SG_3_Strain",
        "SP7P8_BS3L_HAJ_SG_1_Strain",
        "SP7P8_BS3L_HAJ_SG_2_Strain",
        "SP7P8_BS3L_HAJ_SG_3_Strain",
        "SP7P8_BS3L_AAJ_SG_1_Strain",
        "SP7P8_BS3L_AAJ_SG_2_Strain",
        "SP7P8_BS3L_AAJ_SG_3_Strain",
        "SP7P8_BS3L_HBLBJ_SG1_Strain",
        "SP7P8_BS3L_HBLBJ_SG2_Strain",
        "SP7P8_BS3L_HBLBJ_SG3_Strain",
        "SP7P8_BS3L_BLBJ_SG_1_Strain",
        "SP7P8_BS3L_BLBJ_SG_2_Strain",
        "SP7P8_BS3L_BLBJ_SG_3_Strain",
        "P7_BS3L_NJ_SG_1_Strain",
        "P7_BS3R_NJ_SG_2_Strain",
        "P8_BS3L_NJ_SG_3_Strain"
    ]

    # Calculate the statistics
    P6_P7_BS3_LHS_statistics = {
        "Instrument Tag No.": [],
        "MAX.": [],
        "MIN.": [],
        "AVG.": [],
        "SD.": []
    }

    # Iterate over each CSV file
    for csv_file in P6_P7_BS3_csv_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, skiprows=3)

        # Calculate the statistics for each column
        for column in P6_P7_BS3_LHS_columns:
            if column in df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = df[column].max()
                minimum = df[column].min()
                average = df[column].mean()
                std_dev = df[column].std()

                # Store the statistics in the dictionary
                P6_P7_BS3_LHS_statistics["Instrument Tag No."].append(column)
                P6_P7_BS3_LHS_statistics["MAX."].append(maximum)
                P6_P7_BS3_LHS_statistics["MIN."].append(minimum)
                P6_P7_BS3_LHS_statistics["AVG."].append(average)
                P6_P7_BS3_LHS_statistics["SD."].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    P6_P7_BS3_LHS_statistics_datas = pd.DataFrame(P6_P7_BS3_LHS_statistics)



    # --------------------------------------- #
    # ------------ PART 4 ------------------- #
    # -- ANALYZE Strain Gauges -------------- #
    # -- P9-CP2 LHS - BS5 ------------------- #
    # --------------------------------------- #

    P6_P7_BS5_csv_files = [
        dl[2],
        dl[3]
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P7_CP2_DL3-DataList.csv",
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P9_A2_DL4-DataList.csv"
    ]

    # Define the columns for analysis
    P6_P7_BS5_LHS_columns = [
        "SP9CP2_BS5R_HAJ_SG_1_Strain",
        "SP9CP2_BS5R_HAJ_SG_2_Strain",
        "SP9CP2_BS5R_HAJ_SG_3_Strain",
        "SP9CP2_BS5R_AAJ_SG_1_Strain",
        "SP9CP2_BS5R_AAJ_SG_2_Strain",
        "SP9CP2_BS5R_AAJ_SG_3_Strain",
        "SP9CP2_BS5R_HBLBJSG1_Strain",
        "SP9CP2_BS5R_HBLBJSG2_Strain",
        "SP9CP2_BS5R_HBLBJSG3_Strain",
        "SP9CP2_BS5R_BLBJ_SG1_Strain",
        "SP9CP2_BS5R_BLBJ_SG2_Strain",
        "SP9CP2_BS5R_BLBJ_SG3_Strain",
        "SP9CP2_BS5L_HAJ_SG1_Strain",
        "SP9CP2_BS5L_HAJ_SG2_Strain",
        "SP9CP2_BS5L_HAJ_SG3_Strain",
        "SP9CP2_BS5L_AAJ_SG1_Strain",
        "SP9CP2_BS5L_AAJ_SG2_Strain",
        "SP9CP2_BS5L_AAJ_SG3_Strain",
        "SP9CP2_BS5L_HBLBJSG1_Strain",
        "SP9CP2_BS5L_HBLBJSG2_Strain",
        "SP9CP2_BS5L_HBLBJSG3_Strain",
        "SP9CP2_BS5L_BLBJSG1_Strain",
        "SP9CP2_BS5L_BLBJSG2_Strain",
        "SP9CP2_BS5L_BLBJSG3_Strain",
        "P9_BS5L_NJ_SG_1_Strain",
        "P9_BS5R_NJ_SG_2_Strain",
        "CP2_BS5L_NJ_SG_3_Strain",
        "CP2_BS5R_NJ_SG_4_Strain"
    ]

    # Calculate the statistics
    P6_P7_BS5_LHS_statistics = {
        "Instrument Tag No.": [],
        "MAX.": [],
        "MIN.": [],
        "AVG.": [],
        "SD.": []
    }

    # Iterate over each CSV file
    for csv_file in P6_P7_BS5_csv_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, skiprows=3)

        # Calculate the statistics for each column
        for column in P6_P7_BS5_LHS_columns:
            if column in df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = df[column].max()
                minimum = df[column].min()
                average = df[column].mean()
                std_dev = df[column].std()

                # Store the statistics in the dictionary
                P6_P7_BS5_LHS_statistics["Instrument Tag No."].append(column)
                P6_P7_BS5_LHS_statistics["MAX."].append(maximum)
                P6_P7_BS5_LHS_statistics["MIN."].append(minimum)
                P6_P7_BS5_LHS_statistics["AVG."].append(average)
                P6_P7_BS5_LHS_statistics["SD."].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    P6_P7_BS5_LHS_statistics_datas = pd.DataFrame(P6_P7_BS5_LHS_statistics)



    # --------------------------------------- #
    # ------------ PART 5 ------------------- #
    # -- ANALYZE Strain Gauges -------------- #
    # -- P6-P7 RHS - BS2 -------------------- #
    # --------------------------------------- #

    P6_P7_BS2_csv_files = [
        dl[0],
        dl[1]
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_A1_P7_DL1-DataList.csv",
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P6_P8_DL2-DataList.csv"
    ]

    # Define the columns for analysis
    P6_P7_BS2_RHS_columns = [
        "SP6P7_BS2L_HAJ_SG_1_Strain",
        "SP6P7_BS2L_HAJ_SG_2_Strain",
        "SP6P7_BS2L_HAJ_SG_3_Strain",
        "SP6P7_BS2L_AAJ_SG_1_Strain",
        "SP6P7_BS2L_AAJ_SG_2_Strain",
        "SP6P7_BS2L_AAJ_SG_3_Strain",
        "SP6P7_BS2L_HBLBJ_SG1_Strain",
        "SP6P7_BS2L_HBLBJ_SG2_Strain",
        "SP6P7_BS2L_HBLBJ_SG3_Strain",
        "SP6P7_BS2L_BLBJ_SG_1_Strain",
        "SP6P7_BS2L_BLBJ_SG_2_Strain",
        "SP6P7_BS2L_BLBJ_SG_3_Strain",
        "SP6P7_BS2R_HAJ_SG_1_Strain",
        "SP6P7_BS2R_HAJ_SG_2_Strain",
        "SP6P7_BS2R_HAJ_SG_3_Strain",
        "SP6P7_BS2R_AAJ_SG_1_Strain",
        "SP6P7_BS2R_AAJ_SG_2_Strain",
        "SP6P7_BS2R_AAJ_SG_3_Strain",
        "SP6P7_BS2R_HBLBJ_SG1_Strain",
        "SP6P7_BS2R_HBLBJ_SG2_Strain",
        "SP6P7_BS2R_HBLBJ_SG3_Strain",
        "SP6P7_BS2R_BLBJ_SG_1_Strain",
        "SP6P7_BS2R_BLBJ_SG_2_Strain",
        "SP6P7_BS2R_BLBJ_SG_3_Strain",
        "P6_BS2L_NJ_SG_1_Strain",
        "P6_BS2R_NJ_SG_2_Strain",
        "P7_BS2L_NJ_SG_3_Strain",
        "P7_BS2R_NJ_SG_4_Strain"
    ]

    # Calculate the statistics
    P6_P7_BS2_RHS_statistics = {
        "Instrument Tag No.": [],
        "MAX.": [],
        "MIN.": [],
        "AVG.": [],
        "SD.": []
    }

    # Iterate over each CSV file
    for csv_file in P6_P7_BS2_csv_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, skiprows=3)

        # Calculate the statistics for each column
        for column in P6_P7_BS2_RHS_columns:
            if column in df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = df[column].max()
                minimum = df[column].min()
                average = df[column].mean()
                std_dev = df[column].std()

                # Store the statistics in the dictionary
                P6_P7_BS2_RHS_statistics["Instrument Tag No."].append(column)
                P6_P7_BS2_RHS_statistics["MAX."].append(maximum)
                P6_P7_BS2_RHS_statistics["MIN."].append(minimum)
                P6_P7_BS2_RHS_statistics["AVG."].append(average)
                P6_P7_BS2_RHS_statistics["SD."].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    P6_P7_BS2_RHS_statistics_datas = pd.DataFrame(P6_P7_BS2_RHS_statistics)




    # --------------------------------------- #
    # ------------ PART 7 ------------------- #
    # -- ANALYZE Strain Gauges -------------- #
    # -- P6-P7 RHS - BS4 -------------------- #
    # --------------------------------------- #

    P6_P7_BS4_csv_files = [
        dl[1],
        dl[2]
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P6_P8_DL2-DataList.csv",
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P7_CP2_DL3-DataList.csv"
    ]

    # Define the columns for analysis
    P6_P7_BS4_RHS_columns = [
        "SP7P8_BS4L_HAJ_SG_1_Strain",
        "SP7P8_BS4L_HAJ_SG_2_Strain",
        "SP7P8_BS4L_HAJ_SG_3_Strain",
        "SP7P8_BS4L_AAJ_SG_1_Strain",
        "SP7P8_BS4L_AAJ_SG_2_Strain",
        "SP7P8_BS4L_AAJ_SG_3_Strain",
        "SP7P8_BS4L_HBLBJ_SG1_Strain",
        "SP7P8_BS4L_HBLBJ_SG2_Strain",
        "SP7P8_BS4L_HBLBJ_SG3_Strain",
        "SP7P8_BS4L_BLBJ_SG_1_Strain",
        "SP7P8_BS4L_BLBJ_SG_2_Strain",
        "SP7P8_BS4L_BLBJ_SG_3_Strain",
        "SP7P8_BS4R_HAJ_SG_1_Strain",
        "SP7P8_BS4R_HAJ_SG_2_Strain",
        "SP7P8_BS4R_HAJ_SG_3_Strain",
        "SP7P8_BS4R_AAJ_SG_1_Strain",
        "SP7P8_BS4R_AAJ_SG_2_Strain",
        "SP7P8_BS4R_AAJ_SG_3_Strain",
        "SP7P8_BS4R_HBLBJ_SG1_Strain",
        "SP7P8_BS4R_HBLBJ_SG2_Strain",
        "SP7P8_BS4R_HBLBJ_SG3_Strain",
        "SP7P8_BS4R_BLBJ_SG_1_Strain",
        "SP7P8_BS4R_BLBJ_SG_2_Strain",
        "SP7P8_BS4R_BLBJ_SG_3_Strain",
        "P7_BS4L_NJ_SG_1_Strain",
        "P7_BS4R_NJ_SG_2_Strain",
        "P8_BS4L_NJ_SG_3_Strain",
        "P8_BS4R_NJ_SG_4_Strain"
    ]

    # Calculate the statistics
    P6_P7_BS4_RHS_statistics = {
        "Instrument Tag No.": [],
        "MAX.": [],
        "MIN.": [],
        "AVG.": [],
        "SD.": []
    }

    # Iterate over each CSV file
    for csv_file in P6_P7_BS4_csv_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, skiprows=3)

        # Calculate the statistics for each column
        for column in P6_P7_BS4_RHS_columns:
            if column in df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = df[column].max()
                minimum = df[column].min()
                average = df[column].mean()
                std_dev = df[column].std()

                # Store the statistics in the dictionary
                P6_P7_BS4_RHS_statistics["Instrument Tag No."].append(column)
                P6_P7_BS4_RHS_statistics["MAX."].append(maximum)
                P6_P7_BS4_RHS_statistics["MIN."].append(minimum)
                P6_P7_BS4_RHS_statistics["AVG."].append(average)
                P6_P7_BS4_RHS_statistics["SD."].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    P6_P7_BS4_RHS_statistics_datas = pd.DataFrame(P6_P7_BS4_RHS_statistics)




    # --------------------------------------- #
    # ------------ PART 8 ------------------- #
    # -- ANALYZE Strain Gauges -------------- #
    # -- P9-CP2 BS-6 RHS -------------------- #
    # --------------------------------------- #

    P6_P7_BS6_csv_files = [
        dl[2],
        dl[3]
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P7_CP2_DL3-DataList.csv",
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P9_A2_DL4-DataList.csv"
    ]

    # Define the columns for analysis
    P6_P7_BS6_RHS_columns = [
        "SP9CP2_BS6L_HAJ_SG_1_Strain",
        "SP9CP2_BS6L_HAJ_SG_2_Strain",
        "SP9CP2_BS6L_HAJ_SG_3_Strain",
        "SP9CP2_BS6L_AAJ_SG_1_Strain",
        "SP9CP2_BS6L_AAJ_SG_2_Strain",
        "SP9CP2_BS6L_AAJ_SG_3_Strain",
        "SP9CP2_BS6L_HBLBJSG1_Strain",
        "SP9CP2_BS6L_HBLBJSG2_Strain",
        "SP9CP2_BS6L_HBLBJSG3_Strain",
        "SP9CP2_BS6L_BLBJ_SG1_Strain",
        "SP9CP2_BS6L_BLBJ_SG2_Strain",
        "SP9CP2_BS6L_BLBJ_SG3_Strain",
        "SP9CP2_BS6R_HAJ_SG_1_Strain",
        "SP9CP2_BS6R_HAJ_SG_2_Strain",
        "SP9CP2_BS6R_HAJ_SG_3_Strain",
        "SP9CP2_BS6R_AAJ_SG1_Strain",
        "SP9CP2_BS6R_AAJ_SG_2_Strain",
        "SP9CP2_BS6R_AAJ_SG_3_Strain",
        "SP9CP2_BS6R_HBLBJSG1_Strain",
        "SP9CP2_BS6R_HBLBJSG2_Strain",
        "SP9CP2_BS6R_HBLBJSG3_Strain",
        "SP9CP2_BS6R_BLBJSG1_Strain",
        "SP9CP2_BS6R_BLBJSG2_Strain",
        "SP9CP2_BS6R_BLBJSG3_Strain",
        "P9_BS6L_NJ_SG_1_Strain",
        "P9_BS6R_NJ_SG_2_Strain",
        "CP2_BS6L_NJ_SG_3_Strain",
        "CP2_BS6R_NJ_SG_4_Strain"
    ]

    # Calculate the statistics
    P6_P7_BS6_RHS_statistics = {
        "Instrument Tag No.": [],
        "MAX.": [],
        "MIN.": [],
        "AVG.": [],
        "SD.": []
    }

    # Iterate over each CSV file
    for csv_file in P6_P7_BS6_csv_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, skiprows=3)

        # Calculate the statistics for each column
        for column in P6_P7_BS6_RHS_columns:
            if column in df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = df[column].max()
                minimum = df[column].min()
                average = df[column].mean()
                std_dev = df[column].std()

                # Store the statistics in the dictionary
                P6_P7_BS6_RHS_statistics["Instrument Tag No."].append(column)
                P6_P7_BS6_RHS_statistics["MAX."].append(maximum)
                P6_P7_BS6_RHS_statistics["MIN."].append(minimum)
                P6_P7_BS6_RHS_statistics["AVG."].append(average)
                P6_P7_BS6_RHS_statistics["SD."].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    P6_P7_BS6_RHS_statistics_datas = pd.DataFrame(P6_P7_BS6_RHS_statistics)



    # --------------------------------------- #
    # -- ANALYZE Strain Gauges -------------- #
    # -- Dunlop Viaduct LHS & RHS ----------- #
    # --------------------------------------- #

    dunlop_Viaduct_csv_files = [
        dl[3]
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P9_A2_DL4-DataList.csv"
    ]

    # Define the columns for analysis
    dunlop_Viaduct_RHS_columns = [
        "SCP2P10_RBLG_SG_1_Strain",
        "SP10P11_RBLG_SG_1_Strain",
        "SP11P12_RBLG_SG_1_Strain",
        "SP12P13_RBLG_SG_1_Strain",
        "SP13P14_RBLG_SG_1_Strain",
        "SP14A2_RBLG_SG_1_Strain",
        "A2_RBLG_SG_1_Strain"
    ]

    dunlop_Viaduct_LHS_columns = [
        "SCP2P10_LBLG_SG_2_Strain",
        "SP10P11_LBLG_SG_2_Strain",
        "SP11P12_LBLG_SG_2_Strain",
        "SP12P13_LBLG_SG_2_Strain",
        "SP13P14_LBLG_SG_2_Strain",
        "SP14A2_LBLG_SG_2_Strain",
        "A2_LBLG_SG_2_Strain"
    ]

    # Calculate the statistics
    dunlop_Viaduct_RHS_statistics = {
        "Instrument Tag No.": [],
        "MAX.": [],
        "MIN.": [],
        "AVG.": [],
        "SD.": []
    }

    dunlop_Viaduct_LHS_statistics = {
        "Instrument Tag No.": [],
        "MAX.": [],
        "MIN.": [],
        "AVG.": [],
        "SD.": []
    }

    # Iterate over each CSV file
    for csv_file in dunlop_Viaduct_csv_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, skiprows=3)

        # Calculate the statistics for each column
        for column in dunlop_Viaduct_RHS_columns:
            if column in df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = df[column].max()
                minimum = df[column].min()
                average = df[column].mean()
                std_dev = df[column].std()

                # Store the statistics in the dictionary
                dunlop_Viaduct_RHS_statistics["Instrument Tag No."].append(column)
                dunlop_Viaduct_RHS_statistics["MAX."].append(maximum)
                dunlop_Viaduct_RHS_statistics["MIN."].append(minimum)
                dunlop_Viaduct_RHS_statistics["AVG."].append(average)
                dunlop_Viaduct_RHS_statistics["SD."].append(std_dev)

        # Calculate the statistics for each column
        for column in dunlop_Viaduct_LHS_columns:
            if column in df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = df[column].max()
                minimum = df[column].min()
                average = df[column].mean()
                std_dev = df[column].std()

                # Store the statistics in the dictionary
                dunlop_Viaduct_LHS_statistics["Instrument Tag No."].append(column)
                dunlop_Viaduct_LHS_statistics["MAX."].append(maximum)
                dunlop_Viaduct_LHS_statistics["MIN."].append(minimum)
                dunlop_Viaduct_LHS_statistics["AVG."].append(average)
                dunlop_Viaduct_LHS_statistics["SD."].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    dunlop_Viaduct_RHS_statistics_datas = pd.DataFrame(dunlop_Viaduct_RHS_statistics)
    dunlop_Viaduct_LHS_statistics_datas = pd.DataFrame(dunlop_Viaduct_LHS_statistics)




    # ----------------------------------------------------------------------- #
    # -- ANALYZE Strain Gauges ---------------------------------------------- #
    # -- P7-P8 BS-4	RHS (additional as suggested by IIT) -------------------- #
    # ----------------------------------------------------------------------- #

    P7_P8_BS4_additional_csv_files = [
        dl[1],
        dl[2]
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P6_P8_DL2-DataList.csv",
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P7_CP2_DL3-DataList.csv"
    ]

    # Define the columns for analysis
    P7_P8_BS4_additional_RHS_columns = [
        "SP7P8_BS4L_HBLBJ_SG4_Strain",
        "Additional_SG13_Strain",
        "Additional_SG14_Strain"
    ]

    # Calculate the statistics
    P7_P8_BS4_additional_RHS_statistics = {
        "Instrument Tag No.": [],
        "MAX.": [],
        "MIN.": [],
        "AVG.": [],
        "SD.": []
    }

    # Iterate over each CSV file
    for csv_file in P7_P8_BS4_additional_csv_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, skiprows=3)

        # Calculate the statistics for each column
        for column in P7_P8_BS4_additional_RHS_columns:
            if column in df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = df[column].max()
                minimum = df[column].min()
                average = df[column].mean()
                std_dev = df[column].std()

                # Store the statistics in the dictionary
                P7_P8_BS4_additional_RHS_statistics["Instrument Tag No."].append(column)
                P7_P8_BS4_additional_RHS_statistics["MAX."].append(maximum)
                P7_P8_BS4_additional_RHS_statistics["MIN."].append(minimum)
                P7_P8_BS4_additional_RHS_statistics["AVG."].append(average)
                P7_P8_BS4_additional_RHS_statistics["SD."].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    P7_P8_BS4_additional_RHS_statistics_datas = pd.DataFrame(P7_P8_BS4_additional_RHS_statistics)





    # --------------------------------------- #
    # -- ANALYZE Strain Gauges -------------- #
    # -- Chitpur Viaduct RHS & LHS ---------- #
    # --------------------------------------- #

    chitpur_viaduct_csv_files = [
        dl[4]
        # "/content/drive/MyDrive/Colab Notebooks/dristy-automation-csvs/Tallah_ROB_P16_A3_DL5-DataList.csv",
    ]

    # Define the columns for analysis
    chitpur_viaduct_RHS_columns = [
        "SP16P17_RBLG_SG_1_Strain",
        "SP17P18_RBLG_SG_1_Strain",
        "SP18P19_RBLG_SG_1_Strain",
        "SP19P20_RBLG_SG_1_Strain",
        "SP20P21_RBLG_SG_1_Strain",
        "SP21A3_RBLG_SG_1_Strain",
        "A3_RBLG_SG_1_Strain"
    ]

    chitpur_viaduct_LHS_columns = [
        "SP16P17_LBLG_SG_2_Strain",
        "SP17P18_LBLG_SG_2_Strain",
        "SP18P19_LBLG_SG_2_Strain",
        "SP19P20_LBLG_SG_2_Strain",
        "SP20P21_LBLG_SG_2_Strain",
        "SP21A3_LBLG_SG_2_Strain",
        "A3_LBLG_SG_2_Strain"
    ]

    # Calculate the statistics
    chitpur_viaduct_RHS_statistics = {
        "Instrument Tag No.": [],
        "MAX.": [],
        "MIN.": [],
        "AVG.": [],
        "SD.": []
    }

    chitpur_viaduct_LHS_statistics = {
        "Instrument Tag No.": [],
        "MAX.": [],
        "MIN.": [],
        "AVG.": [],
        "SD.": []
    }

    # Iterate over each CSV file
    for csv_file in chitpur_viaduct_csv_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, skiprows=3)

        # Calculate the statistics for each column
        for column in chitpur_viaduct_RHS_columns:
            if column in df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = df[column].max()
                minimum = df[column].min()
                average = df[column].mean()
                std_dev = df[column].std()

                # Store the statistics in the dictionary
                chitpur_viaduct_RHS_statistics["Instrument Tag No."].append(column)
                chitpur_viaduct_RHS_statistics["MAX."].append(maximum)
                chitpur_viaduct_RHS_statistics["MIN."].append(minimum)
                chitpur_viaduct_RHS_statistics["AVG."].append(average)
                chitpur_viaduct_RHS_statistics["SD."].append(std_dev)

        # Calculate the statistics for each column
        for column in chitpur_viaduct_LHS_columns:
            if column in df.columns:
                # Calculate the maximum, minimum, average, and standard deviation for each column
                maximum = df[column].max()
                minimum = df[column].min()
                average = df[column].mean()
                std_dev = df[column].std()

                # Store the statistics in the dictionary
                chitpur_viaduct_LHS_statistics["Instrument Tag No."].append(column)
                chitpur_viaduct_LHS_statistics["MAX."].append(maximum)
                chitpur_viaduct_LHS_statistics["MIN."].append(minimum)
                chitpur_viaduct_LHS_statistics["AVG."].append(average)
                chitpur_viaduct_LHS_statistics["SD."].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    chitpur_viaduct_RHS_statistics_datas = pd.DataFrame(chitpur_viaduct_RHS_statistics)
    chitpur_viaduct_LHS_statistics_datas = pd.DataFrame(chitpur_viaduct_LHS_statistics)

    ########## END Strain Gauges Data ##########

                
    return render_template(
        "home.html",
        weather_datas=weather_datas, laser_datas=laser_datas,
        temprature_meter_datas=temprature_meter_datas, 
        tilt_meter_datas=tilt_meter_datas, ldvt_datas=ldvt_datas,
        shayam_bazar_viaduct_RHS_statistics_datas=shayam_bazar_viaduct_RHS_statistics_datas,
        shayam_bazar_viaduct_LHS_statistics_datas=shayam_bazar_viaduct_LHS_statistics_datas,
        P6_P7_BS1_LHS_statistics_datas=P6_P7_BS1_LHS_statistics_datas,
        P6_P7_BS3_LHS_statistics_datas=P6_P7_BS3_LHS_statistics_datas,
        P6_P7_BS5_LHS_statistics_datas=P6_P7_BS5_LHS_statistics_datas,
        P6_P7_BS2_RHS_statistics_datas=P6_P7_BS2_RHS_statistics_datas,
        P6_P7_BS4_RHS_statistics_datas=P6_P7_BS4_RHS_statistics_datas,
        P6_P7_BS6_RHS_statistics_datas=P6_P7_BS6_RHS_statistics_datas,
        dunlop_Viaduct_RHS_statistics_datas=dunlop_Viaduct_RHS_statistics_datas,
        dunlop_Viaduct_LHS_statistics_datas=dunlop_Viaduct_LHS_statistics_datas,
        P7_P8_BS4_additional_RHS_statistics_datas=P7_P8_BS4_additional_RHS_statistics_datas,
        chitpur_viaduct_RHS_statistics_datas=chitpur_viaduct_RHS_statistics_datas,
        chitpur_viaduct_LHS_statistics_datas=chitpur_viaduct_LHS_statistics_datas
    )