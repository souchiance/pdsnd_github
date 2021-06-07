import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = {'january' : 1, 'february' : 2, 'march' : 3, 'april' : 4, 'may' : 5 , 'june' : 6}
cities = ['chicago','new york city','washington']
days = ['all', 'monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']

# Function to retrieve user preference about the get_filters
# Firstly the user must choose a city between three databases
# Secondly he/she must choose the type of filter : by month , by day , both  or none
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = 'none'
    month = 'none'
    day ='none'
    filter_type = ''
    filter_types = ['both','month','day','none']
    while not (city in cities ):
        city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()

    # Get user preferable filter (month ,day , both or none)
    # Get user input for month (all, january, february, ... , june)
    # Get user input for day of week (all, monday, tuesday, ... sunday)

    while not (filter_type in filter_types):
        filter_type = input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter ').lower()
    if  filter_type == 'both':
        while not (month in months ):
            month = input('Which month? January, February, March, April, May, or June? ').lower()
        while not (day in days ):
            day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday ').lower()
    elif filter_type == 'month':
        while not (month in months ):
            month = input('Which month? January, February, March, April, May, or June? ').lower()
            day = 'none'
    elif filter_type == 'day':
        while not (day in days ):
            day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday ').lower()
            month = 'none'
    else :
        month = 'none'
        day = 'none'

    print('-'*40)
    return city, month, day

# Function to load data from csv files and to add columns for Start Time, Month, Day and Hour according to the filters
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour
    if month != 'none' and day != 'none' :
        df = df[df['Month'] == months[month]]
        df = df[df ['Day']== day.capitalize() ]
        df ['Filter Type'] = 'both'
    elif month != 'none' and  day == 'none':
        df = df[df['Month'] == months[month]]
        df ['Filter Type'] = 'month'
    elif month == 'none' and  day != 'none':
        df = df[df ['Day']== day.capitalize() ]
        df ['Filter Type'] = 'day'
    else :
        df ['Filter Type'] = 'none'
    return df

# Function to display time statistics according to city data and filters
# The function must calculate the most common month, day and hour regarding to user's demande
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # Checking if the filter is none
    # TO DO: display the most common month
    most_common_month = df['Month'].mode()[0]
    #these two lines have been inspired from https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
    keys_list = list(months)
    key = keys_list[most_common_month-1]

    most_common_month_count = df[df['Month'] == most_common_month]['Month'].count()
    # TO DO: display the most common day of week
    most_common_day = df['Day'].mode()[0]
    most_common_day_count = df[df['Day'] == most_common_day]['Day'].count()
    # TO DO: display the most common start hour
    most_common_hour = df['Hour'].mode()[0]
    most_common_hour_count = df[df['Hour'] == most_common_hour]['Hour'].count()
    if  df['Filter Type'].count() == df[df['Filter Type'] == 'none']['Filter Type'].count():
        print('The most common month is {}, count : {} , filter : none'.format(key.capitalize(),most_common_month_count))
        print('The most common day is {}, count : {} , filter : none.'.format(most_common_day.capitalize(),most_common_day_count))
        print('The most common hour is {}, count : {} , filter : none.'.format(most_common_hour,most_common_hour_count))

    elif  df['Filter Type'].count() == df[df['Filter Type'] == 'day']['Filter Type'].count():
        print('The most common month is {}, count : {} , filter : by day : {}.'.format(key.capitalize(),most_common_day_count,most_common_day))
        print('The most common hour is {}, count : {} , filter : by day : {}.'.format(most_common_hour,most_common_hour_count,most_common_day))
    elif  df['Filter Type'].count() == df[df['Filter Type'] == 'month']['Filter Type'].count():
        print('The most common day is {}, count : {} , filter : by month : {}.'.format(most_common_day.capitalize(),most_common_day_count,key.capitalize()))
        print('The most common hour is {}, count : {} , filter : by month : {}.'.format(most_common_hour,most_common_hour_count,key.capitalize(),))
    else :
        print('The most common hour is {}, count : {} , filter : both(Month : {} , Day : {}).'.format(most_common_hour,most_common_hour_count,key.capitalize(),most_common_day))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    start_station_count = df[df['Start Station'] == start_station]['Start Station'].count()
    print('The most common start station is {} ,count : {}.'.format(start_station, start_station_count))
    # TO DO: display most commonly noused end station
    end_station = df['End Station'].mode()[0]
    end_station_count = df[df['End Station'] == end_station]['End Station'].count()
    print('The most common end station is {} ,count : {}.'.format(end_station, end_station_count))

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = 'From : ' + df['Start Station'] + ' To : ' + df['End Station']
    trip = df['Trip'].mode()[0]
    trip_count = df[df['Trip'] == trip]['Trip'].count()
    print('The most common trip is {} ,count : {}.'.format(trip, trip_count))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time_day = int(df['Trip Duration'].sum() // 86400)
    total_travel_time_hours = int((df['Trip Duration'].sum() % 86400) // 3600 )
    total_travel_time_minutes = int(((df['Trip Duration'].sum() % 86400) % 3600) // 60 )
    total_travel_time_seconds = int(((df['Trip Duration'].sum() % 86400) % 3600) % 60)
    print('Tha total travel time is {} seconds which is equal to : {} days , {} hours , {} minutes and {} seconds'.format(int(df['Trip Duration'].sum()),total_travel_time_day,total_travel_time_hours,total_travel_time_minutes,total_travel_time_seconds))

    # TO DO: display mean travel time
    mean_travel_time_hours = int(df['Trip Duration'].mean())//3600
    mean_travel_time_minutes = (int(df['Trip Duration'].mean())%3600) // 60
    mean_travel_time_seconds = (int(df['Trip Duration'].mean())%3600) % 60
    print('The average travel time is {} seconds which is equal to : {} hours , {} minutes and {} seconds'.format(df['Trip Duration'].mean(),mean_travel_time_hours,mean_travel_time_minutes,mean_travel_time_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('The statistic for user types are :')
    print(df['User Type'].value_counts())


    # TO DO: Display counts of gender
    try :
        print("The statistics for users' gender are :",'\n',df['Gender'].value_counts())
    except KeyError:
        print("There is no 'Gender' data available in this database")

    # TO DO: Display earliest, most recent, and most common year of birth
    try :
        print('The earliest year of birth is : {}.'.format(int(df['Birth Year'].min())))
        print('The most recent year of birth is : {}.'.format(int(df['Birth Year'].max())))
        print('The most common year of birth is : {}.'.format(int(df['Birth Year'].mode()[0])))

    except KeyError:
        print("There is no 'Birth Year' data available in this database")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Function to display data statistics by 5 rows.
# The function allows the user to stop data display anytime he/she likes
def display_data(df):
    # This line of code has been borrowed form https://towardsdatascience.com/pretty-displaying-tricks-for-columnar-data-in-python-2fe3b3ed9b83
    pd.options.display.max_columns = None

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while view_data != 'no' :
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to see the next 5 rows of data?: ").lower()

# main function which calls all the function by order
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
