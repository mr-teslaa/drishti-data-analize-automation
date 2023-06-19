from flask import Blueprint, render_template
import pandas as pd
import numpy as np
import re


main = Blueprint('main', __name__)


@main.route("/")
def home():
    ######################### START weather data #########################################

    # --------------------------------------- #
    # -- ANALYZE Automatic Weather Station -- #
    # --------------------------------------- #
    # Read the CSV file into a DataFrame
    csv_file = "AutomaticWeatherStation_Data_List12Jun23.csv"
    df = pd.read_csv(csv_file, skiprows=3)

    # Define the columns for analysis
    columns = [
        "Solar_Radiation (W/m2)",
        "Wind_Direction_max",
        "Relative_Humidity (%RH)",
        "Atmospheric_Temp (DegC)",
        "Air_Pressure (hPa)",
        "Wind_Speed_max (km/h)"
    ]

    # Calculate the statistics
    statistics = {
        "Weather Parameter": [],
        "Maximum": [],
        "Minimum": [],
        "Average": [],
        "Standard Deviation": []
    }

    for column in columns:
        # Calculate the maximum, minimum, average, and standard deviation for each column
        maximum = df[column].max()
        minimum = df[column].min()
        average = df[column].mean()
        std_dev = df[column].std()

        # Store the statistics in the dictionary
        statistics["Weather Parameter"].append(column)
        statistics["Maximum"].append(maximum)
        statistics["Minimum"].append(minimum)
        statistics["Average"].append(average)
        statistics["Standard Deviation"].append(std_dev)

    # Create a DataFrame from the statistics dictionary
    statistics_df = pd.DataFrame(statistics)

    # Display the table of statistics
    print(statistics_df)

    ######################### END weather data #########################################

    # Read the CSV file into a DataFrame
    data = pd.read_csv("TallahROBLaser_Data_List16Jun23.csv", skiprows=3)

    # Define the columns we need to calculate
    columns = [
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

    # Define the threshold value
    threshold = 0.5

    # Initialize an empty list to store the calculated results
    results = []

    # Loop over the rows in the table
    for index, row in data.iterrows():
        # Initialize a dictionary to store the results for this row
        row_results = {}

        # Loop over the columns and calculate min, max, avg, and std
        for column in columns:
            # Find the correct deflection column based on the LS number
            # ls_number = int(''.join(filter(str.isdigit, column.split("_LS")[-1])))
            ls_number = re.search(r'LS(\d+)', column).group(1)
            deflection_column = f"Deflection_{ls_number}"

            # Grab the data for the current column and deflection column
            column_values = row[column]
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
            row_results[column] = {
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
        results.append(row_results)

    # Print the results
    for result in results:
        # print("Location\tParameter\tMax.\tMin.\tAvg.\tStandard Deviation")
        for column, values in result.items():
            # print('----- start ---')
            # print(column)
            # print(values)
            # print('------')
            parameter = column.split("_")[-1]
            max_value = values["Max"]
            min_value = values["Min"]
            avg_value = values["Avg"]
            std_value = values["Std"]

        # print(f"{column}\t{parameter}\t{max_value}\t{min_value}\t{avg_value}\t{std_value}")

    return render_template("home.html", statistics=statistics_df, results=results)
