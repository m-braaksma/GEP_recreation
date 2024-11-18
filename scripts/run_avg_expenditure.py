"""
Purpose: Use the UNWTO country expenditure data and country level inbound arrivals by mode of transportation, 
to estimate the average expenditure by inbound visitor by mode of transportation for each country and each year.  
"""


# Dependencies



# Clean Expenditure Data

- convert to long format

# Clean Inbound arrivals by mode of transportation 

- convert to long format


# Merge arrivals and expenditure on country and year 


# Estimate the average expenditure by mode of transportation 

    # TODO: Can combine the following into a function, and then use 'air' 'water' or 'land' as the argument to create these variables.
prec_mode_air = air arrivals / total for the year 
prec_mode_water = water arrivals / total for the year 
prec_mode_land = land arrivals / total for the year 

avg_price_air = total exp * prec_mode_air
avg_price_water = total exp * prec_mode_water
avg_price_land = total exp * prec_mode_land


# Save data set as average expenses data set

