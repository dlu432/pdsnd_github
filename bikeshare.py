import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june']
WEEK_DATA = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
RAW_KEYS = []

def valid_column(column, df):
    return column in df.columns


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    cities = list(CITY_DATA.keys())
    city_options = ', '.join(CITY_DATA.keys())

    while True:
        print("\nSelect city to analyze: {}".format(city_options))
        city = input("Enter name of a city: ").lower()

        if city in CITY_DATA.keys():
            break

    while True:
        print("\nFilter data by a specific month or by all for no filtering")
        print("Valid input: all, january, february, ... june")
        month = input('Enter a valid month: ').lower()
        if (month in MONTH_DATA) or (month == 'all'):
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print("\nFilter data by a day of the week or all for no filtering")
        print("Valid inputs: all, monday, tuesday, ... sunday")
        day = input('Enter a valid day of the week: ').lower()
        if (day in WEEK_DATA) or (day == 'all'):
            break

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    global RAW_KEYS
    RAW_KEYS = df.columns


    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        month_index = MONTH_DATA.index(month)+1
        df = df[df['month'] == month_index]


    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('\tMost common month: ',
        MONTH_DATA[df['month'].value_counts().index[0] - 1].title())


    # display the most common day of week
    print('\tMost common day of week: ', df['day_of_week'].value_counts().index[0])


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\tMost common start hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\tMost popular start station: ', df['Start Station'].mode()[0])
    print('\tStart Station Count: ', df['Start Station'].value_counts()[0])


    # display most commonly used end station
    print('\tMost popular end station: ', df['End Station'].mode()[0])
    print('\tEnd Station Count: ', df['End Station'].value_counts()[0])


    # display most frequent combination of start station and end station trip
    station_df = df['Start Station'] + ' - '+ df['End Station']
    #print(type(station_df))
    print('\tMost popular route: ', station_df.mode()[0])
    print('\tRoute count: ', station_df.value_counts()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\tTotal travel time: ', df['Trip Duration'].sum())
    #print(df.columns)

    # display mean travel time
    print('\tMean travel time: ', df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if valid_column('User Type', df):
        user_types = df['User Type'].value_counts()
        user_index = user_types.index
        print('\tUser Types:')
        for index in user_index:
            print('\t\t{}: {}'.format(index, user_types.loc[index]))
    else:
        print('\t\tUser Type: No data available')

    # Display counts of gender
    if valid_column('Gender', df):
        gender_types = df['Gender'].value_counts()
        gender_index = gender_types.index
        print('\tGender:')
        for index in gender_index:
            print('\t\t{}: {}'.format(index, gender_types.loc[index]))
    else:
        print('\t\tGender: No data available')

    # Display earliest, most recent, and most common year of birth
    if valid_column('Birth Year', df):
        print('\tYear of birth:')
        print('\t\tOldest: ', int(df['Birth Year'].max()))
        print('\t\tYoungest: ', int(df['Birth Year'].min()))
        print('\t\tMost common popular: ', int(df['Birth Year'].mode()[0]))
    else:
        print('\t\tBirth Year: No data available')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def yesno_input(msg):
    next_items = ''
    while next_items not in ('yes', 'no'):
        next_items = input(msg)
        next_items = next_items.lower()
    return next_items


def raw_data(df):
    index = df.index
    keys = df.columns
    index_start = 0
    max_display = 5
    displayed = 0
    next_items = ''

    while displayed < len(index):
        if (displayed + 5) > len(index):
            max_display = len(index) - displayed

        for i in range(max_display):
            print('\nIndex: {}'.format(index[index_start + i]))

            for j in RAW_KEYS[1:]:
                print('\t{}: \t{}'.format(j, df.iloc[index_start+i][j]))
            displayed += 1

        # move start pointer forward
        index_start = displayed - 1


        while next_items not in ('yes', 'no'):
            next_items = yesno_input('\nDo you want to continue? Enter yes or no.\n')


        if next_items == 'yes':
            # reset variable for next continue
            next_items = ''
        if next_items == 'no':
            break


def main():
    next_analysis = ''
    while True:

        city, month, day = get_filters()
        df = load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        if yesno_input("\nDo you want to see data 5 enteries at a time?  Enter yes or no.\n") == 'yes':
            raw_data(df)


        while next_analysis not in ('yes', 'no'):
            next_analysis = yesno_input("\nWould you like to restart? Enter yes or no.\n")

        if next_analysis == 'yes':
            # reset flag
            next_analysis = ''
        elif next_analysis == 'no':
            break


if __name__ == "__main__":
	main()
