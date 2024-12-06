#!/usr/bin/env python3
import argparse
import pandas as pd
import numpy as np

def check_country(country, df):
    if country in df["country"].values:
        return True
    else:
        return False

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Predict a country’s temperature change vs 1850")
    parser.add_argument("country", type=str, help="Input the country name")
    parser.add_argument("CO2_concentrations", type=str, 
                        help="Input the CO2 concentrations, like 187.3,908.3. Notice: The input should be a comma-separated list")
    parser.add_argument("-s", "--save", action="store_true",
                         help="Save the predictions to a CSV file")
    args = parser.parse_args()

    # Read parameters from CSV
    paras_df = pd.read_csv("./paras.csv")

    # Check for valid country
    if not (check_country(args.country, paras_df) or args.country == "global_mean"):
        exit('Invalid country name')

    paras_df.set_index(['country', 'degree'], inplace=True)

    # Parse CO2 concentrations
    if args.CO2_concentrations:
        datas = args.CO2_concentrations.split(",")
        CO2_concentrations = np.array(datas, dtype=np.float32)
    else:
        exit('Please input the CO2 concentrations')

    # Get model parameters for the selected country
    if args.country == "global_mean":
        weight = paras_df.loc["global_mean", 1].values
        bias = paras_df.loc["global_mean", 0].values
    else:
        weight = paras_df.loc[args.country, 1].values
        bias = paras_df.loc[args.country, 0].values

    # Calculate predictions
    predictions = weight * CO2_concentrations + bias

    # Optionally save predictions to CSV
    if args.save:
        df = pd.DataFrame({"CO2_concentrations": CO2_concentrations,
                            "predictions": predictions})
        df.to_csv("./predictions_of_" + args.country + ".csv", 
                  header="predicted temperature of " + args.country, index=False)
    
    