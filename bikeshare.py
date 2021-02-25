import time
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    possible_cities = ["chicago", 'new york city', 'washington']  # provide a list of correct answers
    while True:
        city = input('What city would you like to explore? Your options are Chicago, New York City, or Washington:').lower()
        if not city in possible_cities:
            print(
                "Sorry, you didn't input the correct city, please look at the spelling and options above and try again")
            continue
        else:
            print("Ok! let's take a look at {}".format(city))
            break

    possible_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june'] # provide list of correct months
    while True:
        month = input(
            "What month would you like to look at data for? your options are either 'all' or any month from January to June:").lower()
        if not month in possible_months:
            print("Sorry, you didn't input a valid answer: please check to see if you have spelled the month in full,"
                  " or that you have selected one of the valid months. Let's try again")
            continue
        else:
            print("Ok! let's take a look at {}".format(month))
            break
    possible_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input(
            "What day would you like to look at data for? your options are either 'all' or any day of the week spelled in full:").lower()
        if not day in possible_days:
            print("Sorry, you didn't input a valid answer: please check to see if you have spelled the day in full."
                  " Let's try again")
            continue
        else:
            print("Ok! let's take a look at {}".format(day))
            break
    print('-' * 40)
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
    df = pd.DataFrame(pd.read_csv(CITY_DATA[city]))
    df['Start Time'] = pd.to_datetime(df['Start Time'])  # converting column to date
    df['month'] = df['Start Time'].dt.month  # creating a column of numerical month values 1 - 6
    df['weekday'] = df['Start Time'].dt.weekday  # creating a column of  character weekdays

    # Dictionaries to match input names to numeric column elements
    month_list = {'january': 1, 'february': 3, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
    day_list = {'monday': 1, 'tuesday': 3, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7}

    # Conditionals to account for "all" vs. filters
    if month != 'all' and day != 'all':
        df = df.loc[
            (df['month'] == month_list[month]) & (df['weekday'] == day_list[day])]  # filtering df for month and day
    elif month == 'all' and day != 'all':
        df = df.loc[(df['weekday'] == day_list[day])]  # filtering df for day
    elif month != 'all' and day == 'all':
        df = df.loc[(df['month'] == month_list[month])]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    # Dictionaries to match mode values to characters
    month_list = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june'}
    day_list = {1: 'monday', 2: 'tuesday', 3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday', 7: 'sunday'}

    df['hour_start'] = df['Start Time'].dt.hour  # create variable for hour start

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # assigning character values to the mode (most common) month, day and hour values
    common_month = month_list[df['month'].mode()[0]]
    common_day = day_list[df['weekday'].mode()[0]]
    common_hour = df['hour_start'].mode()[0]

    # No need to report filtered column data - conditionals to filter these
    if len(df.month.unique()) == 1 and len(df.weekday.unique()) == 1:
        print("The most common hour to start travel: {}".format(common_hour))
    elif len(df.month.unique()) != 1 and len(df.weekday.unique()) == 1:
        print("The most common month of travel: {}".format(common_month))
        print("The most common hour to start travel: {}".format(common_hour))
    elif len(df.month.unique()) == 1 and len(df.weekday.unique()) != 1:
        print("The most common day of the week for travel: {}".format(common_day))
        print("The most common hour to start travel: {}".format(common_hour))
    elif len(df.month.unique()) != 1 and len(df.weekday.unique()) != 1:
        print("The most common month of travel: {}".format(common_month))
        print("The most common day of the week for travel: {}".format(common_day))
        print("The most common hour to start travel: {}".format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_station = dict(
        df['Start Station'].value_counts())  # create a dictionary of ordered value counts to find most common
    start_station = next(iter(start_station))  # call the key for the most common

    end_station = dict(
        df['End Station'].value_counts())  # create a dictionary of ordered value counts to find most common
    end_station = next(iter(end_station))  # call the key for the most common

    df['Combo Station'] = "start station = "df['Start Station'] + "end station =  " + df[
        'End Station']  # paste both start and stop together to form a new variable
    combo_station = dict(
        df['Combo Station'].value_counts())  # create a dictionary of ordered value counts to find most common
    combo_station = next(iter(combo_station))  # call the key for the most common

    print("The most commonly used start station: {}".format(start_station))
    print("The most commonly used end station: {}".format(end_station))
    print("The most frequent combination of start station and end station trip: {}".format(combo_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_days = ((df['Trip Duration'].sum() / 60) / 60) / 24  # providing a more intuitive answer in days
    total_travel = df['Trip Duration'].sum()
    print("Total travel time in seconds: {}\n This is approximately {} days".format(total_travel, total_travel_days))

    average_travel = df['Trip Duration'].mean()
    print("The average travel time (in seconds): {}".format(average_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = dict(df['User Type'].value_counts())
    user_types_list = []  # set up for loop by creating list
    for key, value in user_types.items():  # loop to create list from dictionary
        temp = (key, value)
        user_types_list.append(temp)
    user_types_df = pd.DataFrame(user_types_list)  # convert to dataframe for better display
    user_types_df.columns = ['User Type', 'Count']  # rename columns for aesthetics
    print("Here are the counts of different user types:\n {}".format(user_types_df))

    #  Display counts of gender with a conditional for df's that don't have gender data
    if "Gender" in df.columns:
        gender_types = dict(df['Gender'].value_counts())
        gender_types_list = []  # set up for loop by creating list
        for key, value in gender_types.items():  # loop to create list from dictionary
            temp = (key, value)
            gender_types_list.append(temp)
        gender_types_df = pd.DataFrame(gender_types_list)  # convert to dataframe for better display
        gender_types_df.columns = ['Gender', 'Count']  # rename columns for aesthetics
        print("Here are the counts of Gender: \n{}".format(gender_types_df))
    else:
        print("Your chosen city did not report Gender data")

    # Display earliest, most recent, and most common year of birth, with a conditional for df's that don't have birth data
    if "Birth Year" in df.columns:
        birth_year = df['Birth Year'].dropna().astype(int)  # create series, drop NaNs, and remove decimals
        earliest = birth_year.min()
        latest = birth_year.max()
        most_common = birth_year.mode()[0]
        print(
            "The earliest year of birth is {}, the latest year of birth is {}, and the most common birth year is {} ".format(
                earliest, latest, most_common))
    else:
        print("Your chosen city did not report Birth Year Data")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_data(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
    if view_data == "no":
        return("ok")
    start_loc = 0
    while start_loc +5 < len(df):
         print(df.iloc[start_loc:start_loc+5])
         start_loc += 5
         view_display = input("Do you wish to continue? please answer 'yes' or 'no': ").lower()
         if view_display =='no':
            break
    return("ok that's it for raw data")

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
