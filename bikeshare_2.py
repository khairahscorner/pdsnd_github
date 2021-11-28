import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_month(months_dict):
    """
    Asks user to specify a month.

    Arguments:
        (dict) months_dict - dictionary of months

    Returns:
        (str) month - name of the month to filter by
    """
    print('Which month would you like to filter by? Select one of JAN, FEB, MAR, APR, MAY or JUN.')
    month = input('Month: ').upper()
    while (month not in months_dict):
        month = input('Please choose the month correctly. Select one of JAN, FEB, MAR, APR, MAY or JUN: \n').upper()   
    return month


def get_day(days_dict):
    """
    Asks user to specify a day.

    Arguments:
        (dict) days_dict - dictionary of days

    Returns:
        (str) day - name of the day to filter by
    """
    print('Which day would you like to filter by? Select one of Mon, Tue, Wed, Thu, Fri, Sat or Sun.')
    day = input('Day: ').title()
    while (day not in days_dict):
        day = input('Please choose the day correctly. Select one of Mon, Tue, Wed, Thu, Fri, Sat or Sun: \n').title()
    return day


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
    print("""\nFirst things first! We have three cities, each with its own city code : Chicago (CC), New York City (NYC) and Washington (DC).
    \nWhich city would you like to get statistics on?\n""")

    city = input('City code: ').lower()
    city_dict = { 'cc': 'Chicago', 
                  'nyc': 'New York City',
                  'dc': 'Washington' }
    
    while city not in city_dict:
        print('\nLooks like you entered the city code wrong. Let\'s try again, make sure to enter one of CC, NYC, DC.\n')
        city = input('City code: ').lower()
    city = city_dict[city]
    print('\nGreat! We will be exploring data for {}'.format(city))

    print('\nNext: Would you like to filter through the data? Please choose Y for Yes and N for No')
    response = input('Y or N: ').lower()

    while response not in ('y','n'):
        print('\nPlease choose either \'Y\' or \'N\'')
        response = input('Y or N: ').lower()
    if(response == 'n'):
        print('\nOkay! We will show the city data with no filters. ')
        month = 'all'
        day = 'all'
    else:
        print('\nGreat! We can filter by month, day or both. Which would you like to filter by? ')
        response = input('Type M for month, D for day or B for both: ').title()

        filter_dict = {'M': 'month', 
                        'D': 'day',
                        'B': 'both'}

        months_dict = {'JAN': 'January', 
                        'FEB': 'February',
                        'MAR': 'March',
                        'APR': 'April',
                        'MAY': 'May',
                        'JUN': 'June'}

        days_dict = {'Mon': 'Monday', 
                     'Tue': 'Tuesday',
                     'Wed': 'Wednesday',
                     'Thu': 'Thursday',
                     'Fri': 'Friday',
                     'Sat': 'Saturday',
                     'Sun': 'Sunday' }
                   
        while (response not in filter_dict):
            print('Please choose the filter correctly: Type M for month, D for day or B for both')
            response = input('M, D or B? : ').title()
        print('\nGreat! We will filter by {} '.format(filter_dict[response]))

        # get user input for month only filter (all, january, february, ... , june)
        if(response == 'M'):
            month = months_dict[get_month(months_dict)]
            day = 'all'
            print('\nOkay! We will show {} city data filtered for the month of {}. '.format(city, month))

        # get user input for day only filter (all, monday, tuesday, ... sunday)
        elif(response == 'D'):
            day = days_dict[get_day(days_dict)]
            month = 'all'
            print('\nOkay! We will show {} city data filtered for {}s. '.format(city, day))

        # get user input for both filters
        else:
            month = months_dict[get_month(months_dict)]
            day = days_dict[get_day(days_dict)]
            print('\nOkay! We will show {} city data filtered for the month of {} and {}s. '.format(city, month, day))

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
    print('Now loading data...')
    start = time.time()
    original = pd.read_csv(CITY_DATA[city.lower()]) # main data with no filters

    #make clone
    df = original.copy()
    #remove unnamed column
    if('Unnamed: 0' in df):
        df.drop(columns=['Unnamed: 0'], inplace=True)

    #convert Start and end time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    df['Month'] = df['Start Time'].dt.month_name()
    df.insert(0, 'Day', (df['Start Time'].dt.day_name()))
    
    # filter by month only
    if(day == "all" and month != 'all'):
        df = df[df['Month'] == month]
    #filter by day
    elif(month == "all" and day != 'all'):
        df = df[df['Day'] == day]
    #filter by both
    elif('all' not in (month, day)):
        df = df[(df['Month'] == month) & (df['Day'] == day)]
    
    count = df.count()[0]
    time_elapsed = time.time() - start
    print('\n\nData successfully loaded! Returned {} rows of data in {} seconds.'.format(count, time_elapsed))
    return df, original


def mode_stats(df,series):
    """Calculate mode of the given series and its count
    Arguments:
        (pandas series) series - series to evaluate
        (pandas dataframe) df - main dataframe

    Returns:
        (str) mode - mode stats
        (str) count - number of mode occurrence
    """
    mode_stat = series.mode()[0]
    mode_rows = df[series == mode_stat]
    return mode_stat, mode_rows


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nLet\'s begin analysis')

    print('\n\nNow Displaying Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month
    mode_month, mode_rows = mode_stats(df, df['Month'])
    print('\n\n1) Most frequent month of travel is: {}'.format(mode_month))
    print('  A total of {} trips were made.'.format(mode_rows['Month'].count()))

    # display the most common day of week
    mode_day, mode_rows = mode_stats(df, df['Day'])
    print('\n2) Most frequent day of travel is: {}'.format(mode_day))
    print('  A total of {} trips were made.'.format(mode_rows['Day'].count()))

    # display the most common start hour
    hour_series = pd.to_datetime(df['Start Time']).dt.strftime('%I%p')
    mode_hour, mode_rows = mode_stats(df, hour_series)
    print('\n3) Most frequent hour of day of travel is: {}'.format(mode_hour.lstrip("0").replace("0", "")))
    print('  A total of {} trips were made.'.format(mode_rows.count()[0]))

    print("\n\nThis took %s seconds.\n\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n\nNow Displaying The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station
    mode_start, mode_rows = mode_stats(df, df['Start Station'])
    print('\n\n1) Most popular start station is: {}'.format(mode_start))
    print('  A total of {} trips were started the station.'.format(mode_rows['Start Station'].count()))


    # display most commonly used end station
    mode_end, mode_rows = mode_stats(df, df['End Station'])
    print('\n2) Most popular end station is: {}'.format(mode_end))
    print('  A total of {} trips were ended at the station.'.format(mode_rows['End Station'].count()))

    # display most frequent combination of start station and end station trip
    mode_both = df['Start Station'].mode()[0] and df['End Station'].mode()[0]
    count = df[(df['Start Station'] == mode_both) & (df['End Station'] == mode_both)]['Start Station'].count()
    print('\n3) The station with the most requent combination of start and end station trip is: {}'.format(mode_both))
    print('  A total of {} trips were started and ended at the station.'.format(count))

    print("\n\nThis took %s seconds.\n\n" % (time.time() - start_time))
    print('-'*40)


def duration_format(series):
    """Format result of trip duration
    Arguments:
        (pandas series) series - series to evaluate

    Returns:
        (str) output - output format of trip duration
    """
    #total_td is components of timedelta of total duration, converted to dictionary type
    total_td = pd.to_timedelta(series, unit='S').components._asdict()
    non_zero_total = {key: value for key,value in total_td.items() if key in ('days', 'hours', 'minutes', 'seconds') and value != 0}

    output = "travel time for all trips is: "
    for i,item in enumerate(non_zero_total):
        if(i == len(non_zero_total) - 1):
            output += 'and {} {}.'.format(non_zero_total[item], item) #last item
        elif(i == len(non_zero_total) - 2):
            output += '{} {} '.format(non_zero_total[item], item) #second to last item
        else:
            output += '{} {}, '.format(non_zero_total[item], item) #others
    return output


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n\nNow Displaying Trip Duration Stats...')
    start_time = time.time()

    # display total travel time
    output = duration_format(df['Trip Duration'].sum())
    print('\n\n1) Total {}'.format(output))
    
    # display mean travel time
    output = duration_format(df['Trip Duration'].mean())
    print('\n2) Average {}'.format(output))

    print("\n\nThis took %s seconds.\n\n" % (time.time() - start_time))
    print('-'*40)


def users_format(col,df):
    """Format result of user stats depending on col
    Arguments:
        (pandas dataframe) df - dataframe to evaluate
        (str) col - column to evaluate
    Returns:
        (str) output - output format
    """
    user_dict = df.groupby([col])[col].count().to_dict()
    output = 'There were '
    for i,item in enumerate(user_dict):
        if(i == len(user_dict) - 1):
            output += 'and {} {}s.'.format(user_dict[item], item) #last item
        elif(i == len(user_dict) - 2):
            output += '{} {}s '.format(user_dict[item], item) #second to last item
        else:
            output += '{} {}s, '.format(user_dict[item], item) #others
    return len(user_dict), output


def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\n\nNow Showing User Statistics...')
    start_time = time.time()

    # Display counts of user types
    length, output = users_format('User Type', df)
    print('\n\n1) There are {} types of BikeShare users.'.format(length))
    print(' {}'.format(output))

    # Display counts of gender
    has_col = lambda col, df: col not in df
    if(has_col('Gender', df)):
        print('\n\n2) No Gender data is available for {}'.format(city))
    else:
        length, output = users_format('Gender', df)
        print('\n\n2) {}'.format(output))
    
    # Display earliest, most recent, and most common year of birth
    if(has_col('Birth Year', df)):
        print('\n\n2) No Birth Year data is available for {}'.format(city))
    else:
        birth_years = df['Birth Year'].convert_dtypes()
        birth_years.loc[birth_years == birth_years.min()].count()
        min_year = birth_years.min()
        min_count = birth_years.loc[birth_years == min_year].count()

        print('\n\n 3) Birth Year Stats:')
        print('\nThe earliest year of birth is {}.'.format(min_year))
        print('  {} people listed it as their birth year'.format(min_count))
        
        max_year = birth_years.max()
        max_count = birth_years.loc[birth_years == max_year].count()      
        print('\nThe most recent year of birth is {}.'.format(max_year))
        print('  {} people listed it as their birth year'.format(max_count))

        most_common_year = birth_years.mode()[0]
        mode_count = birth_years.loc[birth_years == most_common_year].count()      
        print('\nThe most common year of birth is {}.'.format(most_common_year))
        print('  {} people listed it as their birth year'.format(mode_count))

    print("\n\nThis took %s seconds.\n\n" % (time.time() - start_time))
    print('-'*40)

    #start_end gives number of trips that had their start time as the last day of a month and end time as first day of next month
    start_end = df['Start Time'].loc[(df['Start Time'].dt.is_month_end) & (df['End Time'].dt.is_month_start)].count()
    if(start_end != 0):
        print("\n\nFUN FACT")
        print("\n\n {} trips started on last days of month and ended on first days of the next month.\n\n".format(start_end))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df, original = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)

        total_df = original.count()[0]
        # get_data = input('\nWould you like to view the raw data? There are {} lines of data. Choose Y for Yes or N for No.\n'.format(total_df)).lower()

        # while get_data not in ('y','n'):
        #     print('\nPlease choose either \'Y\' or \'N\'')
        #     get_data = input('Y or N: ').lower()
        
        # if get_data.lower() == 'y':
        #     print("\n Now Showing 5 lines of raw data for {}".format(city))
        #     print(original.iloc[:5])
        #     count = 5
        #     get_data = input('\nWould you like to see the next 5 lines? Choose Y for Yes or N for No.\n').lower()
        #     while get_data not in ('y','n'):
        #         print('\nPlease choose either \'Y\' or \'N\'')
        #         get_data = input('Y or N: ').lower()
        #     while get_data == 'y':
        #         if count >= total_df:
        #             print('\n\n No more data available. \n\n')
        #             break
        #         else:
        #             print(original.iloc[count:count+5])
        #             count += 5
        #             get_data = input('\nWould you like to see the next 5 lines? Choose Y for Yes or N for No.\n').lower()
            
        # if get_data.lower() != 'y':
            restart = input('\nOkay. Would you like to restart the analysis? Choose Y for Yes or N for No.\n').lower()
            while restart not in ('y','n'):
                print('\nPlease choose either \'Y\' or \'N\'')
                restart = input('Y or N: ').lower()
            if restart.lower() != 'y':
                break   


if __name__ == "__main__":
	main()
