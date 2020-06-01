import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_mode(column, dataframe):
    """
    Takes in a column name (str) and returns a mode for that column from a given dataframe.
    """
    return dataframe[column].mode()[0]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Gets user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city, month, day = "", "", ""

    i = 0
    while i == 0:
        city = str(input("Enter city name: Chicago, New York City, Washington: ")).lower()
        if city not in CITY_DATA.keys():
            print("Please enter a city name.")
        else:
            i += 1

    # Gets user input for month (all, january, february, ... , june)
    i = 0
    while i == 0:
        month = str(input("Enter the month you want to explore as a string. (Enter 'all' for all months): ")).lower()
        if month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            print("Please enter a month name as a string.")
        else:
            i += 1

    # Gets user input for day of week (all, monday, tuesday, ... sunday)
    i = 0
    while i == 0:
        day = str(input("Enter the day of the week you want to explore as a string. (Enter 'all' for all days of the week): ")).lower()
        if day not in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
            print("Please enter a day of the week name as a string.")
        else:
            i += 1


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of the week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month
    month_mode = get_mode('month', df)

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month_mode = months[month_mode - 1]

    print("The common month was " + str(month_mode).title() + '.')

    # Displays the most common day of week
    day_mode = get_mode('day_of_week', df)

    print("The most common day of the week was " + str(day_mode) + '.')

    # Displays the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    hour_mode = get_mode('hour', df)
    print("The most common start hour was " + str(hour_mode) + '.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station
    start_station_mode = get_mode('Start Station', df)
    print("The most common start station was {}.".format(start_station_mode))

    # Displays most commonly used end station
    end_station_mode = get_mode('End Station', df)
    print("The most common end station was {}.".format(end_station_mode))

    # Displays most frequent combination of start station and end station trip
    # Combines Start Station and End Station columns, then gets the mode:
    df['Both Stations'] = df['Start Station'] + " and " + df['End Station']
    combo_mode = get_mode('Both Stations', df)
    print('The most common combination of start and end station trip was {}.'.format(combo_mode))

    #Delete columns after using them.
    df.drop(columns=['Both Stations'], inplace=True)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time
    total_travel_time = df['Trip Duration'].sum() / 60
    print("Total travel time was {} minutes.".format(total_travel_time))

    # Displays mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 60
    print("Mean travel time was {} minutes.".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    print("User Type values counts:")
    print(df['User Type'].value_counts())
    print('\n')

    # Displays counts of gender
    if "Gender" in df.columns:
        print("Gender counts:")
        print(df['Gender'].value_counts())
        print('\n')

    # Displays earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest = df['Birth Year'].min()
        latest = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]

        print("Birth years:\nEarliest year: {}\nMost recent: {}\nMost common: {}".format(earliest, latest, most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_print(dataframe):
    # Asks to print first 5 rows of a dataframe.
    # If the user goes through every row in the table, will start the table from the beginning.

    cont = 0
    limit = dataframe.shape[0]
    move_on = 0

    while move_on == 0:
        print_data = input("\nDo you want to see the next 5 rows of data? Enter yes or no.\n")
        if print_data.lower() == 'yes' and cont + 5 < limit:
            print(dataframe.iloc[cont:cont + 5])
            cont += 5
        elif print_data.lower() == 'yes':
            print(dataframe.iloc[cont:limit])
            print("Reached end of table, restarting.")
            cont = 0
        else:
            move_on += 1


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_print(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
