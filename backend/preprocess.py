import pandas as pd

# Load raw data (World Bank GDP CSV format)
def load_raw_data(path):
    df = pd.read_csv(path, skiprows=4)  # World Bank CSVs often have 4 metadata rows
    return df

# Clean and reformat data
def clean_gdp_data(df):
    df = df[["Country Name", "Country Code"] + [str(y) for y in range(2000, 2023)]]
    df = df.melt(id_vars=["Country Name", "Country Code"], 
                 var_name="Year", 
                 value_name="GDP per capita")
    df.dropna(inplace=True)
    df["Year"] = df["Year"].astype(int)
    return df

# Save processed data
def save_clean_data(df, path):
    df.to_csv(path, index=False)

# Workflow
if __name__ == "__main__":
    raw_df = load_raw_data("data/raw/rawgdp.csv")
    cleaned_df = clean_gdp_data(raw_df)
    save_clean_data(cleaned_df, "data/clean/gdp_cleaned.csv")
    print("Data preprocessing complete.")
