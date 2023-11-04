from datetime import datetime

# Get the current date
current_date = datetime.now()

# Format the date to get the day as a string
time_string = current_date.strftime("%Y%m%d%H%M")

day_string = current_date.strftime("%m%d")

year_string = current_date.strftime("%Y")[2:4]
# Print the day string
print(time_string)
print(day_string)
print(year_string)