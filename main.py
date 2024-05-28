import pandas as pd
from pyproj import Transformer
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import os
import argparse

def convert_coordinates(input_csv, output_csv):
    # Read the input CSV file
    df = pd.read_csv(input_csv)

    # Initialize the transformer
    transformer = Transformer.from_crs("EPSG:3059", "EPSG:4326", always_xy=True)

    # Define a function to transform coordinates
    def transform_coords(x, y):
        return transformer.transform(y, x)

    # Apply the transformation to each pair of coordinates
    df[['X1', 'Y1']] = df.apply(lambda row: transform_coords(row['X1'], row['Y1']), axis=1, result_type='expand')
    df[['X2', 'Y2']] = df.apply(lambda row: transform_coords(row['X2'], row['Y2']), axis=1, result_type='expand')

    # Add a column with the WKT LINESTRING representation
    df['wkt'] = df.apply(lambda row: f"LINESTRING({row['X1']} {row['Y1']}, {row['X2']} {row['Y2']})", axis=1)
    
    df = df.drop(columns=['X1', 'Y1', 'X2', 'Y2'])
    df = df.rename(columns={'Iezīme': 'line_name', 'Tīkla elementu skaits': 'skaits'})


    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)

def main():
    parser = argparse.ArgumentParser(description='Convert LKS-92 coordinates to WGS-84 and add WKT LINESTRING representation')
    parser.add_argument('files', nargs='*', help='CSV files to be processed')

    args = parser.parse_args()

    if not args.files:
        # Hide the root window
        Tk().withdraw()

        # Open file dialog to select the input CSV files
        input_files = askopenfilenames(title="Select the input CSV files", filetypes=[("CSV Files", "*.csv")])
    else:
        input_files = args.files

    if input_files:
        for input_csv in input_files:
            # Automatically generate the output file name
            base_name = os.path.splitext(input_csv)[0]
            output_csv = f"{base_name}_wgs.csv"   

            # Convert the coordinates and save to the output file
            convert_coordinates(input_csv, output_csv)

            print(f"Conversion complete. Saved to {output_csv}")
    else:
        print("No files selected.")

if __name__ == "__main__":
    main()
