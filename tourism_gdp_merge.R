# Title: Data Processing for GEP Recreation
# Author: Matt Braaksma
# Date: 2024-06-20
# Description: This script reads in tourism and GDP data, cleans and reshapes it,
#              and merges it for further analysis.
# Usage: Set the working directory to the folder containing the data files before running the script.
# Data: 
#   World Bank, GDP by current USD: API_NY.GDP.MKTP.CD_DS2_en_excel_v2_451842.xls
#   UN, Annual Tourism direct GDP as a proportion of total GDP (%): Indicator-8_9_1-2022-UN_Tourism_april2024_update.xlsx
#   country code spreadsheet for merging: country_codes.xlsx


# Load necessary libraries
library(tidyverse)

# Set the working directory
setwd("/Users/mbraaksma/Library/CloudStorage/GoogleDrive-braak014@umn.edu/Shared drives/Johnson-Polasky Lab Drive/Global GEP/Ecosystem Services SubFolders/Recreation")

# Read the data from Excel files
tourism_df <- readxl::read_xlsx("Indicator-8_9_1-2022-UN_Tourism_april2024_update.xlsx")
gdp_wide_df <- readxl::read_xls("API_NY.GDP.MKTP.CD_DS2_en_excel_v2_451842.xls", range = "B4:BO270")
country_codes <- readxl::read_xlsx("country_codes.xlsx")

# Rename columns in the tourism dataframe
names(tourism_df)[names(tourism_df) == 'GeoAreaCode'] <- 'iso_num'
names(tourism_df)[names(tourism_df) == 'TimePeriod'] <- 'year'
names(tourism_df)[names(tourism_df) == 'Total'] <- 'gdp_tourism_prop'

# Rename columns in the GDP dataframe
names(gdp_wide_df)[names(gdp_wide_df) == 'Country Code'] <- 'iso3'

# Reshape GDP data from wide to long format
gdp_df <- gdp_wide_df %>%
  pivot_longer(
    cols = `1960`:`2022`,  # specify the range of columns to pivot
    names_to = "year",     # new column to hold the names of the columns being pivoted
    values_to = "gdp_usd"  # new column to hold the values of the columns being pivoted
  )

# Convert 'year' column to numeric type
gdp_df$year <- as.numeric(gdp_df$year)

# Select only the necessary columns
tourism_df <- tourism_df[, c("iso_num", "year", "gdp_tourism_prop")]
gdp_df <- gdp_df[, c("iso3", "year", "gdp_usd")]

# Merge GDP dataframe with country codes
gdp_df <- inner_join(gdp_df, country_codes)

# Merge tourism dataframe with country codes
tourism_df <- left_join(tourism_df, country_codes)

# Merge the two dataframes together
df_join <- left_join(gdp_df, tourism_df)

# Generate Tourism GDP
df_join$gdp_tourism_usd <- df_join$gdp_usd * (df_join$gdp_tourism_prop/100)

