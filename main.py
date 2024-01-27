import pandas as pd
from datetime import timedelta

def analyze_csv(file_path):
    list1=[]
    list2=[]
    list3=[]
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(file_path)

    # Convert the 'Time Out' column to datetime format
    df['Time Out'] = pd.to_datetime(df['Time Out'])

    # Convert 'Timecard Hours' to numeric
    df['Timecard Hours (as Time)'] = pd.to_numeric(df['Timecard Hours (as Time)'].str.extract('(\d+):(\d+)', expand=False)[0]) + \
                           pd.to_numeric(df['Timecard Hours (as Time)'].str.extract('(\d+):(\d+)', expand=False)[1]) / 60

    # Sort the DataFrame by 'Employee Name' and 'Time Out'
    df = df.sort_values(by=['Employee Name', 'Time Out'])

    # Function to check if a timedelta is within a specified range
    def is_within_range(delta, min_range, max_range):
        return min_range <= delta <= max_range

    # Iterate through each employee
    current_employee = None
    consecutive_days_count = 0

    for index, row in df.iterrows():
        if row['Employee Name'] != current_employee:
            consecutive_days_count = 0
            current_employee = row['Employee Name']
            previous_time_out = None
            continue

        # Check for employees who have worked for 7 consecutive days
        if consecutive_days_count == 6:
            list1.append(current_employee)
            #print(f"Employee {current_employee} has worked for 7 consecutive days.")


        # Check for employees with less than 10 hours between shifts (greater than 1 hour)
        if previous_time_out is not None:
            time_diff = row['Time Out'] - previous_time_out
            if is_within_range(time_diff, timedelta(hours=1), timedelta(hours=10)):
                list2.append(current_employee)
                #print(f"Employee {current_employee} has less than 10 hours between shifts but greater than 1 hour.")

        # Check for employees who have worked for more than 14 hours in a single shift
        if pd.notna(row['Timecard Hours (as Time)']) and row['Timecard Hours (as Time)'] > 14:
            list3.append(current_employee)
            #print(f"Employee {current_employee} has worked for more than 14 hours in a single shift.")

        # Update variables for the next iteration
        previous_time_out = row['Time Out']
        consecutive_days_count += 1
    list1=set(list1)
    list2=set(list2)
    list3=set(list3)
    cnt=1
    print(f"\nBelow Employees have worked for 7 consecutive days.")
    for i in list1:
        print(f"Employee {cnt} - {i}")
        cnt=cnt+1
    print(f"\nThese Employees have less than 10 hours between shifts but greater than 1 hour.")
    cnt=1
    for i in list2:
        print(f"Employee {cnt} - {i}")
        cnt = cnt + 1
    print(f"\nEmployees have worked for more than 14 hours in a single shift.")
    cnt=1
    for i in list3:
        print(f"Employee {cnt} - {i}")
        cnt = cnt + 1

if __name__ == "__main__":
    # Replace 'your_file.csv' with the actual path to your CSV file
    file_path = '/Users/riddhishivhare/Downloads/Assignment_Timecard.csv'
    analyze_csv(file_path)
