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

import os
import re
import random
import string
import datetime
import numpy as np
import pandas as pd
from flask import Blueprint
from flask import render_template
from flask import jsonify



# import pdfkit
from flask import send_file
main = Blueprint('main', __name__)

# DEFINING THE CSV FILES
weather_csv = "AutomaticWeatherStation_Data_List.csv"

laser_csv = "TallahROBLaser_Data_List.csv"

accelerometers_csv = [
    "Tallah_ROB Accelerometer_3DACC1_A1_Approach -Data List13Jul23.csv",
    "Tallah_ROB Accelerometer_3DACC2_P6_P7_RHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_3DACC3_P6_P7_LHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_3DACC4_P7_P8_RHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_3DACC5_P7_P8_LHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_3DACC6_P9_CP2_RHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_3DACC7_P9_CP_LHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_3DACC8_A2_Approach -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_3DACC9_A3_Approach -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC01_A1_P1_RHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC02_A1_P1_LHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC03_P1_P2 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC04_P2_P3 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC05_P3_P4 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC06_P4_P5 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC07_P5_CP1 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC08_CP1_P6_RHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC09_CP1_P6_LHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC10_P8_P9_RHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC11_P8_P9_LHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC12_CP2_P10 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC13_P10_P11 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC14_P11_P12 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC15_P12_P13 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC16_P13_P14 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC17_P14_A2_RHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC18_P14_A2_LHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC19_A3_P21_RHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC20_A3_P21_LHS -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC21_P21_P20 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC22_P20_P19 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC23_P19_P18 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC24_P18_P17 -Data List13Jul23.csv",
    # "Tallah_ROB Accelerometer_ACC25_P17_P16 -Data List13Jul23.csv"
]

dl = [
    "Tallah_ROB_A1_P7_DL1-DataList.csv",
    "Tallah_ROB_P6_P8_DL2-DataList.csv",
    "Tallah_ROB_P7_CP2_DL3-DataList.csv",
    "Tallah_ROB_P9_A2_DL4-DataList.csv",
    "Tallah_ROB_P16_A3_DL5-DataList.csv"
]

corrosion_csv = "Tallah_Corrosion_Current-DataList.csv"

################ START - GLOBAL COLUMN NAME DEFINED ################
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

# Define the columns for analysis
P7_P8_BS4_additional_RHS_columns = [
    "SP7P8_BS4L_HBLBJ_SG4_Strain",
    "Additional_SG13_Strain",
    "Additional_SG14_Strain"
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
################ END - GLOBAL COLUMN NAME DEFINED ################

################ START - SAVE THE LINE CHART ################
# Define the desired lower and upper limits of the y-axis
lower_limit = -50
upper_limit = 50

# Define the desired tick spacing for the y-axis
tick_spacing = 5

# Calculate the tick positions based on the desired tick spacing
tick_positions = np.arange(lower_limit, upper_limit+1, tick_spacing)
################ END - SAVE THE LINE CHART ################


# Function to generate a random ID
def generate_random_id():
    length = 8
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


@main.route("/")
def home():
    ########## START Weather Data ##########

    # --------------------------------------- #
    # -- ANALYZE Automatic Weather Station -- #
    # --------------------------------------- #

    # Read the CSV file into a DataFrame
    weather_csv_file = weather_csv
    weather_df = pd.read_csv(weather_csv_file, skiprows=3)

    # TAKING THE DATE AND TIME RANGE
    # Extract the first and last datetime values from the "Datetime" column
    first_datetime = pd.to_datetime(weather_df["Datetime"].iloc[0])
    last_datetime = pd.to_datetime(weather_df["Datetime"].iloc[-1])

    # Extract the start date, end date, start time, and end time
    start_date = first_datetime.strftime("%d/%m/%Y")
    end_date = last_datetime.strftime("%d/%m/%Y")
    start_time = first_datetime.strftime("%I:%M %p")
    end_time = last_datetime.strftime("%I:%M %p")

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
    laser_df.columns = laser_df.columns.str.strip()

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


    ########## START Temperature Meter Data ##########

    # --------------------------------------- #
    # -- ANALYZE Temperature Meter ---------- #
    # --------------------------------------- #

    temprature_meter_csv_files = [
        dl[1],
        dl[3]
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
        dl[4]
    ]

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


    ########## START Strain Gauges Data ##########

    # --------------------------------------- #
    # ------------ PART 1 ------------------- #
    # -- ANALYZE Strain Gauges -------------- #
    # -- Shayam bazar Viaduct RHS & LHS ----- #
    # --------------------------------------- #
    shayam_bazar_viaduct_csv_files = [
        dl[0]
    ]

    # I made this array globally accessable so that we don't need
    # to copy and past the same code again and again. 
    # Check line 81

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
    ]

    # I made this array globally accessable so that we don't need
    # to copy and past the same code again and again. 
    # Check line 81

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
    ]

    # I made this array globally accessable so that we don't need
    # to copy and past the same code again and again. 
    # Check line 81

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
    ]

    # I made this array globally accessable so that we don't need
    # to copy and past the same code again and again. 
    # Check line 81

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
    ]

    # I made this array globally accessable so that we don't need
    # to copy and past the same code again and again. 
    # Check line 81

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
    ]

    # I made this array globally accessable so that we don't need
    # to copy and past the same code again and again. 
    # Check line 81

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
    ]

    # I made this array globally accessable so that we don't need
    # to copy and past the same code again and again. 
    # Check line 81

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
    ]

    # I made this array globally accessable so that we don't need
    # to copy and past the same code again and again. 
    # Check line 81

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
    ]

    # I made this array globally accessable so that we don't need
    # to copy and past the same code again and again. 
    # Check line 81

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
    ]

    # I made this array globally accessable so that we don't need
    # to copy and past the same code again and again. 
    # Check line 81

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


    ################## START CORROSION DATA ######################
    corrosion_csv_files = corrosion_csv

    # Define the columns for analysis
    corrosion_columns = [
        "N01_Corrosion_Current_1",
        "N01_Corrosion_Current_2",
        "N01_Corrosion_Current_3",
        "N01_Corrosion_Current_4",
        "N02_Corrosion_Current_1",
        "N02_Corrosion_Current_2",
        "N02_Corrosion_Current_3",
        "N02_Corrosion_Current_4"
    ]

    df = pd.read_csv(corrosion_csv_files, skiprows=3)

    # Select the specified columns from the DataFrame
    corrosion_selected_columns = df[corrosion_columns]

    # Convert the DataFrame to a list of dictionaries
    corrosion_data = corrosion_selected_columns.to_dict(orient='records')
    ################## END CORROSION DATA ######################


    return render_template(
        "home.html",
        start_date=start_date, end_date=end_date,
        start_time=start_time, end_time=end_time,
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
        chitpur_viaduct_LHS_statistics_datas=chitpur_viaduct_LHS_statistics_datas,
        corrosion_data=corrosion_data
    )


#   STRAIN GUGES CHARTS VIEW
@main.route('/strain/')
def strain():
    shayam_bazar_viaduct_csv_files = [
        dl[0]
    ] 
    
    P6_P7_BS1_csv_files  = [
        dl[0],
        dl[1]
    ]

    P6_P7_BS3_csv_files = [
        dl[1],
        dl[2]
    ]

    P6_P7_BS5_csv_files = [
        dl[2],
        dl[3]
    ]

    P6_P7_BS2_csv_files = [
        dl[0],
        dl[1]
    ]

    P6_P7_BS4_csv_files = [
        dl[1],
        dl[2]
    ]

    P6_P7_BS6_csv_files = [
        dl[2],
        dl[3]
    ]

    dunlop_Viaduct_csv_files = [
        dl[3]
    ]

    P7_P8_BS4_additional_csv_files = [
        dl[1],
        dl[2]
    ]

    chitpur_viaduct_csv_files = [
        dl[4]
    ]

    # Create a list to store all the CSV files and their corresponding columns
    csv_data_list = [
        (shayam_bazar_viaduct_csv_files, shayam_bazar_viaduct_RHS_columns),
        (shayam_bazar_viaduct_csv_files, shayam_bazar_viaduct_LHS_columns),
        (P6_P7_BS1_csv_files, P6_P7_BS1_LHS_columns),
        (P6_P7_BS3_csv_files, P6_P7_BS3_LHS_columns),
        (P6_P7_BS5_csv_files, P6_P7_BS5_LHS_columns),
        (P6_P7_BS2_csv_files, P6_P7_BS2_RHS_columns),
        (P6_P7_BS4_csv_files, P6_P7_BS4_RHS_columns),
        (P6_P7_BS6_csv_files, P6_P7_BS6_RHS_columns),
        (dunlop_Viaduct_csv_files, dunlop_Viaduct_RHS_columns),
        (dunlop_Viaduct_csv_files, dunlop_Viaduct_LHS_columns),
        (P7_P8_BS4_additional_csv_files, P7_P8_BS4_additional_RHS_columns),
        (chitpur_viaduct_csv_files, chitpur_viaduct_RHS_columns),
        (chitpur_viaduct_csv_files, chitpur_viaduct_LHS_columns)
    ]

    strain_charts_data = []

    # Iterate over each group of CSV files and their columns
    for csv_files, columns in csv_data_list:
        # Create an empty dictionary to store data for this group
        group_data = {
            "csv_files": csv_files, 
            "columns": columns,
            "data": []
        }

        ###############################################
        #### THIS CODE RETURNING AN ERROR 
        #### KeyError: "['SP6P7_BS1L_HAJ_SG_1_Strain', 'SP6P7_BS1L_HAJ_SG_2_Strain', 'SP6P7_BS1L_HAJ_SG_3_Strain', 'SP6P7_BS1L_AAJ_SG_1_Strain', 'SP6P7_BS1L_AAJ_SG_2_Strain', 'SP6P7_BS1L_AAJ_SG_3_Strain', 'SP6P7_BS1L_HBLBJ_SG1_Strain', 'SP6P7_BS1L_HBLBJ_SG2_Strain', 'SP6P7_BS1L_HBLBJ_SG3_Strain', 'SP6P7_BS1L_BLBJ_SG_1_Strain', 'SP6P7_BS1L_BLBJ_SG_2_Strain', 'SP6P7_BS1L_BLBJ_SG3_Strain', 'P7_BS1L_NJ_SG_3_Strain', 'P7_BS1R_NJ_SG_4_Strain'] not in index"
        ###############################################
        
        # # Iterate over each CSV file in the group
        # for csv_file in csv_files:
        #     # Read the CSV file into a DataFrame
        #     df = pd.read_csv(csv_file, skiprows=3)

        #     # Extract data for the defined columns and store it in the dictionary
        #     group_data["data"].extend(df[columns].values.tolist())
        ############################################
        ############################################

        # Iterate over each CSV file in the group
        for csv_file in csv_files:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file, skiprows=3)
            df.columns = df.columns.str.strip()

            # Find the common columns between DataFrame and specified columns
            common_columns = list(set(columns).intersection(df.columns))
            group_data["labels"] = list(df['DateTime'])
            
            # Extract data for the common columns and store it in the dictionary
            for column in common_columns:
                column_data = {
                    "column_name": column,
                    "csv_name": csv_file,
                    "values": df[column].tolist()
                }
                
                group_data["data"].append(column_data)

        # Append the data for this group to the list for all CSV files
        strain_charts_data.append(group_data)

    return render_template(
        'strain.html', 
        strain_charts_data=strain_charts_data
    ) 

#   ACCELEROMETERS VIEW 
@main.route("/accelerometers/")
def accelerometers():
    # ########## START Accelero Meter Data ##########
    # Initialize a list to store data from all CSV files
    accelerometers_charts_data = []

    # Iterate over each CSV file
    for csv_file in accelerometers_csv:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, skiprows=3)
        df.columns = df.columns.str.strip()

        # Create a dictionary to store data for this CSV file
        csv_data = {
            "csv_name": csv_file,  # Track the name of this CSV in the data
            "data": df.to_dict(orient="list")
        }

        # Append the data for this CSV file to the list for all CSV files
        accelerometers_charts_data.append(csv_data)
    # ########## END Temperature Meter Data ##########
    return render_template('accelerometers.html', accelerometers_charts_data=accelerometers_charts_data) 


#   ACCELEROMETERS CHART VIEW 
@main.route("/ldvt/")
def ldvt():
    # --------------------------------------- #
    # -- SHOWING LINE CHART OF LDVT Data --- #
    # --------------------------------------- #
    chart_columns = [
        ['P6_BS1_LGS_D_Displacement', 'P6_BS1_BS2_Alert_Positive', 'P6_BS1_BS2_Alert_Negative', 'P6_BS1_BS2_Action_Positive', 'P6_BS1_BS2_Action_Negative', 'P6_BS1_BS2_Alarm_Positive', 'P6_BS1_BS2_Alarm_Negative'],
        ['P6_BS2_LGS_D_Displacement', 'P6_BS1_BS2_Alert_Positive', 'P6_BS1_BS2_Alert_Negative', 'P6_BS1_BS2_Action_Positive', 'P6_BS1_BS2_Action_Negative', 'P6_BS1_BS2_Alarm_Positive', 'P6_BS1_BS2_Alarm_Negative'],
        ['P6_BS1_FF_D_Displacement', 'P6_BS1_BS2_Alert_Positive', 'P6_BS1_BS2_Alert_Negative', 'P6_BS1_BS2_Action_Positive', 'P6_BS1_BS2_Action_Negative', 'P6_BS1_BS2_Alarm_Positive', 'P6_BS1_BS2_Alarm_Negative'],
        ['P6_BS2_FF_D_Displacement', 'P6_BS1_BS2_Alert_Positive', 'P6_BS1_BS2_Alert_Negative', 'P6_BS1_BS2_Action_Positive', 'P6_BS1_BS2_Action_Negative', 'P6_BS1_BS2_Alarm_Positive', 'P6_BS1_BS2_Alarm_Negative'],
        ['P7_BS1_TGS_Displacement', 'P7_TGS_Alert_Positive', 'P7_TGS_Alert_Negative', 'P7_TGS_Action_Positive', 'P7_TGS_Action_Negative', 'P6_BS1_BS2_Alarm_Positive', 'P6_BS1_BS2_Alarm_Negative'],
        ['P7_BS1_FX_Displacement', 'P7_FX_Alert_Positive', 'P7_FX_Alert_Negative', 'P7_FX_Action_Positive', 'P7_FX_Action_Negative', 'P7_FX_Alarm_Positive', 'P7_FX_Alarm_Negative'],
        ['P7_BS2_FX_Displacement', 'P7_FX_Alert_Positive', 'P7_FX_Alert_Negative', 'P7_FX_Action_Positive', 'P7_FX_Action_Negative', 'P7_FX_Alarm_Positive', 'P7_FX_Alarm_Negative'],
        ['P7_P8_BS3_FF_Displacement', 'P7_P8_BS3_BS4_Alert_Positive', 'P7_P8_BS4_Alert_Negative', 'P7_P8_BS4_Action_Positive', 'P7_P8_BS4_Action_Negative', 'P7_P8_BS4_Alarm_Positive', 'P7_P8_BS4_Alarm_Negative'],
        ['P7_P8_BS3_LGS_Displacement', 'P7_P8_BS3_BS4_Alert_Positive', 'P7_P8_BS4_Alert_Negative', 'P7_P8_BS4_Action_Positive', 'P7_P8_BS4_Action_Negative', 'P7_P8_BS4_Alarm_Positive', 'P7_P8_BS4_Alarm_Negative'],
        ['P7_P8_BS4_LGS_Displacement', 'P7_P8_BS3_BS4_Alert_Positive', 'P7_P8_BS4_Alert_Negative', 'P7_P8_BS4_Action_Positive', 'P7_P8_BS4_Action_Negative', 'P7_P8_BS4_Alarm_Positive', 'P7_P8_BS4_Alarm_Negative'],
        ['P7_BS2_TGS_Displacement', 'P7_TGS_Alert_Positive', 'P7_TGS_Alert_Negative', 'P7_TGS_Action_Positive', 'P7_TGS_Action_Negative', 'P7_TGS_Alarm_Positive', 'P7_TGS_Alarm_Negative'],
        ['P8_D1_Displacement', 'TGS_Alert_Positive', 'TGS_Alert_Negative', 'TGS_Action_Positive', 'TGS_Action_Negative', 'TGS_Alarm_Positive', 'TGS_Alarm_Negative'],
        ['P8_D2_Displacement', 'P8_D2_D3_Alert_Positive', 'P8_D2_D3_Alert_Negative', 'P8_D2_D3_Action_Positive', 'P8_D2_D3_Action_Negative', 'P8_D2_D3_Alarm_Positive', 'P8_D2_D3_Alarm_Negative'],
        ['P8_D3_Displacement', 'P8_D2_D3_Alert_Positive', 'P8_D2_D3_Alert_Negative', 'P8_D2_D3_Action_Positive', 'P8_D2_D3_Action_Negative', 'P8_D2_D3_Alarm_Positive', 'P8_D2_D3_Alarm_Negative'],
        ['P8_D4_Displacement', 'TGS_Alert_Positive', 'TGS_Alert_Negative', 'TGS_Action_Positive', 'TGS_Action_Negative', 'TGS_Alarm_Positive', 'TGS_Alarm_Negative'],
        ['P9_D1_Displacement', 'FF_Alert_Positive', 'FF_Alert_Negative', 'FF_Action_Positive', 'FF_Action_Negative', 'FF_Alarm_Positive', 'FF_Alarm_Negative'],
        ['P9_D2_Displacement', 'LGS_Alert_Positive', 'LGS_Alert_Negative', 'LGS_Action_Positive', 'LGS_Action_Negative', 'LGS_Alarm_Positive', 'LGS_Alarm_Negative'],
        ['P9_D3_Displacement', 'LGS_Alert_Positive', 'LGS_Alert_Negative', 'LGS_Action_Positive', 'LGS_Action_Negative', 'LGS_Alarm_Positive', 'LGS_Alarm_Negative'],
        ['P9_D4_Displacement', 'FF_Alert_Positive', 'FF_Alert_Negative', 'FF_Action_Positive', 'FF_Action_Negative', 'FF_Alarm_Positive', 'FF_Alarm_Negative'],
        ['P12_D1_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['P12_D2_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['P12_D3_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['P12_D4_Displacement', 'P11_P12_D4_D5_Alert_Positive', 'P11_P12_D4_D5_Alert_Negative', 'P11_P12_D4_D5_Action_Positive', 'P11_P12_D4_D5_Action_Negative', 'P11_P12_D4_D5_Alarm_Positive', 'P11_P12_D4_D5_Alarm_Negative'],
        ['P12_D5_Displacement', 'P11_P12_D4_D5_Alert_Positive', 'P11_P12_D4_D5_Alert_Negative', 'P11_P12_D4_D5_Action_Positive', 'P11_P12_D4_D5_Action_Negative', 'P11_P12_D4_D5_Alarm_Positive', 'P11_P12_D4_D5_Alarm_Negative'],
        ['P12_D6_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['P12_D7_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['P12_D8_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['P11_D1_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['P11_D2_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['P11_D3_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['P11_D4_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['P11_D5_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['P11_D6_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['P11_D7_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['P11_D8_Displacement', 'P11_P12_D1_D8_Alert_Positive', 'P11_P12_D1_D8_Alert_Negative', 'P11_P12_D1_D8_Action_Positive', 'P11_P12_D1_D8_Action_Negative', 'P11_P12_D1_D8_Alarm_Positive', 'P11_P12_D1_D8_Alarm_Negative'],
        ['CP2_BS5_TGS_D_Displacement', 'TGS_Alert_Negative', 'TGS_Alert_Positive', 'TGS_Action_Positive', 'TGS_Action_Negative', 'TGS_Alarm_Positive', 'TGS_Alarm_Negative'],
        ['CP2_BS5_FX_D_Displacement', 'FX_Alert_Negative', 'FX_Alert_Positive', 'FX_Action_Positive', 'FX_Action_Negative', 'FX_Alarm_Positive', 'FX_Alarm_Negative'],
        ['CP_BS6_FX_D_Displacement', 'FX_Alert_Negative', 'FX_Alert_Positive', 'FX_Action_Positive', 'FX_Action_Negative', 'FX_Alarm_Positive', 'FX_Alarm_Negative'],
        ['CP2_BS6_TGS_D_Displacement', 'TGS_Alert_Negative', 'TGS_Alert_Positive', 'TGS_Action_Positive', 'TGS_Action_Negative', 'TGS_Alarm_Positive', 'TGS_Alarm_Negative'],
        ['P18_D1_Displacement', 'FF_Alert_Negative', 'FF_Alert_Positive', 'FF_Action_Positive', 'FF_Action_Negative', 'FF_Alarm_Positive', 'FF_Alarm_Negative'],
        ['P18_D2_Displacement', 'LGS_Alert_Negative', 'LGS_Alert_Positive', 'LGS_Action_Positive', 'LGS_Action_Negative', 'LGS_Alarm_Positive', 'LGS_Alarm_Negative'],
        ['P18_D3_Displacement', 'LGS_Alert_Negative', 'LGS_Alert_Positive', 'LGS_Action_Positive', 'LGS_Action_Negative', 'LGS_Alarm_Positive', 'LGS_Alarm_Negative'],
        ['P18_D4_Displacement', 'FF_Alert_Negative', 'FF_Alert_Positive', 'FF_Action_Positive', 'FF_Action_Negative', 'FF_Alarm_Positive', 'FF_Alarm_Negative'],
        ['P17_D1_Displacement', 'TGS_Alert_Negative', 'TGS_Alert_Positive', 'TGS_Action_Positive', 'TGS_Action_Negative', 'TGS_Alarm_Positive', 'TGS_Alarm_Negative'],
        ['P17_D2_Displacement', 'P17_D3_D2_Alert_Negative', 'P17_D3_D2_Alert_Positive', 'P17_D3_D2_Action_Positive', 'P17_D3_D2_Action_Negative', 'P17_D3_D2_Alarm_Positive', 'P17_D3_D2_Alarm_Negative'],
        ['P17_D3_Displacement', 'P17_D3_D2_Alert_Negative', 'P17_D3_D2_Alert_Positive', 'P17_D3_D2_Action_Positive', 'P17_D3_D2_Action_Negative', 'P17_D3_D2_Alarm_Positive', 'P17_D3_D2_Alarm_Negative'],
        ['P17_D4_Displacement', 'TGS_Alert_Negative', 'TGS_Alert_Positive', 'P17_D3_D2_Action_Positive', 'P17_D3_D2_Action_Negative', 'P17_D3_D2_Alarm_Positive', 'P17_D3_D2_Alarm_Negative']
    ]

    # Initialize a list to store chart data for all charts
    ldvt_charts_data = []

    # Iterate over each CSV file
    for dl_csv_file in dl:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(dl_csv_file, skiprows=3)
        df.columns = df.columns.str.strip()

        # Initialize a list to store chart data for this CSV file
        csv_charts_data = []

        for i, columns in enumerate(chart_columns):
            # Check if all required columns exist in the DataFrame
            if all(column in df.columns for column in columns):
                # Create a dictionary to store chart data
                chart_data = {
                    "dl_name": dl_csv_file,
                    "chart_title": f"Chart {i + 1}",
                    "labels": list(df['DateTime']),
                    "datasets": []
                }

                for column in columns:
                    # Create a dataset dictionary for this column
                    dataset = {
                        "label": column,
                        "data": list(df[column])
                    }

                    # Generate a random ID for the chart
                    chart_data["canvas_id"] = generate_random_id()

                    # Append the chart data to the list for this CSV file
                    csv_charts_data.append(chart_data)

                    # Add the dataset to the chart data
                    chart_data["datasets"].append(dataset)

                # Append the chart data to the list for this CSV file
                csv_charts_data.append(chart_data)
            else:
                print(f"Required columns not found in {dl_csv_file}. Skipping chart {i + 1}.")

        # Append the chart data for this CSV file to the list for all CSV files
        ldvt_charts_data.append(csv_charts_data)
    return render_template('ldvt.html', ldvt_charts_data=ldvt_charts_data)



#   LASER CHART VIEW 
@main.route("/laser/")
def laser():
    # --------------------------------------- #
    # -- SHOWING LINE CHART OF Laser Data --- #
    # --------------------------------------- #

    # Read the CSV file into a DataFrame
    laser_csv_file = laser_csv
    laser_df = pd.read_csv(laser_csv_file, skiprows=3)
    laser_df.columns = laser_df.columns.str.strip()

    # Initialize an array to store data for each chart
    laser_charts_data = []

    # Iterate over the Deflection columns
    for i in range(1, 6):
        deflection_column = f"Deflection_{i}"
        threshold_column = f"Threshold_LS{i}_Alert"

        # Create data dictionary for this chart
        chart_data = {
            f"ls{i}": [{
                "labels": list(laser_df['DateTime']),  # Assuming 'DateTime' is a column in 'laser_df'
                "deflection_data": list(laser_df[deflection_column]),
                "threshold_data": list(laser_df[threshold_column]),
            }],
            "chart_id": f"laser_chart_{i}",
            "chart_title": f"Laser Chart {i}",
        }

        # Append data dictionary to the array
        laser_charts_data.append(chart_data)
    return render_template('laser.html', laser_charts_data=laser_charts_data)