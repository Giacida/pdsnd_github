import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['January', 'February','March','April','May','June']
days = ['Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

#####################################
def get_filters():
    """
    Asks user to specify city, month and day for analysis.
    If any input is 'stop', program stops.
    Returns:
        - city (str): valid input only among the keys of CITY_DATA
        - month (str/None): valid input only from january to june, or None if no month-filter is required
        - day (str/None): valid input days of the week, or None if no day-filter is required

    """
    stop_msg =  'You stopped the program, bye!'
    try_again_msg = 'Invalid input! Try again or type \'stop\' to stop:'
    print('-'*40)
    print('Hello! Let\'s explore some US bikeshare data!')

    city, month, day = None, None, None
    # get city
    while True:
        city = input('Enter a city among the following:\n{},\nor type \'stop\' to stop:\n'.format(list(CITY_DATA))).lower()
        if city in list(CITY_DATA):
            break
        elif city == 'stop':
            print(stop_msg)
            return('stop', month, day)
        else:
            print(try_again_msg)

    # get month
    while True:
        get_month = input('Would you like to filter the data by month? y/n\n').lower()
        if get_month == 'y':
            while True:
                month = input('Enter a month from January to June, or type \'stop\' to stop:\n').title()
                if month in months:
                    break
                elif month == 'Stop':
                    print(stop_msg)
                    return(city, 'stop', day)
                else:
                    print(try_again_msg)
            break
        elif get_month == 'n':
            break
        elif get_month == 'stop':
            print(stop_msg)
            return(city, 'stop', day)
        else:
            print(try_again_msg)

    # get day
    while True:
        get_day = input('Would you like to filter the data by day? y/n\n').lower()
        if get_day == 'y':
            while True:
                day = input('Enter a day of the week, in letters:\n').title()
                if day in days:
                    break
                elif day == 'Stop':
                    print(stop_msg)
                    return(city, month, 'stop')
                else:
                    print(try_again_msg)
            break
        elif get_day == 'n':
            break
        elif get_day == 'stop':
            print(stop_msg)
            return(city, month, 'stop')
        else:
            print(try_again_msg)

    return(city, month, day)






#####################################
def get_data(city,month,day):
    """
    Loads data from the required .csv file, applying month and day filters.
    Inputs:
        -city (str): name of the city to analyse
        -month (str/None): name of the month to filter by, or None if no filter is applied
        -day (str/None): name of the day to filter by, or None if no filter is applied
    Returns:
        - df: Pandas DataFrame containing city data filtered by month and day
    """

    # load file
    df = pd.read_csv(CITY_DATA.get(city))
    # create new columns extrapolating month and day from Start Time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Dow'] = df['Start Time'].dt.day_name()

    # check input filters and apply filters to data
    if month:
        month = months.index(month) + 1
        df = df[df['Month'] == month]
    if day:
        df = df[df['Dow'] == day]

    return df





#####################################
def time_stats(df):
    """
    Displays different stats regarding time of travel.
    Input:
        - df (Pandas DataFrame): data to analyse
    No output
    """
    print('-'*40)
    print('Analyis of most frequent times of travel returned:\n')
    t0 = time.time()

    mc_month = df['Month'].mode().values
    mc_dow = df['Dow'].mode().values
    df['Hour'] = df['Start Time'].dt.hour
    mc_hour = df['Hour'].mode().values

    # display most common month
    if mc_month.size == 1:
        print('MOST COMMON MONTH: ', months[mc_month[0]-1])
    else:
        print('MOST COMMON MONTHS, EX EQUO: ', [months[i-1] for i in mc_month])
    # display most common day of the week
    if mc_dow.size == 1:
        print('MOST COMMON DOW: ', mc_dow[0])
    else:
        print('MOST COMMON DOWS, EX EQUO: ', mc_dow)
    # display most common hour
    if mc_hour.size == 1:
        print('MOST COMMON HOUR: ', mc_hour[0])
    else:
        print('MOST COMMON HOURS, EX EQUO: ', mc_hour)

    print("\nDone in %s seconds." % round(time.time() - t0,2))










#####################################
def station_stats(df):
    """
    Displays most popular stations and trips.
    Input:
        - df (Pandas DataFrame): data to analyse
    No output
    """
    print('-'*40)
    print('Analyis of most popular stations and trips returned:\n')
    t0 = time.time()

    mc_ss = df['Start Station'].mode().values
    mc_es = df['End Station'].mode().values
    df['Full Trip'] = df['Start Station'] + '/' + df['End Station']
    mc_ft = df['Full Trip'].mode().values

    # display most common stations
    if mc_ss.size == 1:
        print('MOST COMMON START STATION: ', mc_ss[0])
    else:
        print('MOST COMMON START STATIONS, EX EQUO: ', mc_ss)
    print('with {} occurrences'.format(df['Start Station'].value_counts()[mc_ss[0]]))

    if mc_es.size == 1:
        print('MOST COMMON END STATION: ', mc_es[0])
    else:
        print('MOST COMMON END STATIONS, EX EQUO: ', mc_es)
    print('with {} occurrences'.format(df['End Station'].value_counts()[mc_es[0]]))

    if mc_ft.size == 1:
        print('MOST COMMON TRIP: ', mc_ft[0])
    else:
        print('MOST COMMON TRIPS, EX EQUO: ', mc_ft)
    print('with {} occurrences'.format(df['Full Trip'].value_counts()[mc_ft[0]]))

    print("\nDone in %s seconds." % round(time.time() - t0,2))


#####################################
def duration_stats(df):
    """
    Displays total and average travel time.
    Input:
        - df (Pandas DataFrame): data to analyse
    No output
    """
    print('-'*40)
    print('Analyis of trip duration returned:\n')
    t0 = time.time()

    tot_dur=df['Trip Duration'].sum()
    av_dur=df['Trip Duration'].mean()

    print('TOTAL TRIP DURATION: ', pd.to_timedelta(tot_dur, unit='seconds'))
    print('AVERAGE TRIP DURATION: ', pd.to_timedelta(av_dur, unit='seconds'))

    print("\nDone in %s seconds." % round(time.time() - t0,2))




#####################################
def user_stats(city, df):
    """
    Displays breakdown of type, gender and stats of the birth year of the bikeshare users.
    Input:
        - city (str): city chosen for the analysis
        - df (Pandas DataFrame): data to analyse
    No output
    """
    print('-'*40)
    print('Analyis of users returned:\n')
    t0 = time.time()

    print('COUNT OF EACH USER TYPE:\n', df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print('\nCOUNT OF USER GENDER:\n', df['Gender'].value_counts())
    else:
        print('\nDATA ABOUT GENDER ARE NOT AVAILABLE')

    if 'Birth Year' in df.columns:
        print('\nBIRTH YEAR OF OLDEST USER: ', int(df['Birth Year'].min()))
        print('BIRTH YEAR OF YOUNGEST USER: ', int(df['Birth Year'].max()))
        print('MOST COMMON BIRTH YEAR: ',int((df['Birth Year'].mean())))
    else:
        print('\nDATA ABOUT BIRTH YEAR ARE NOT AVAILABLE')

    print("\nDone in %s seconds." % round(time.time() - t0,2))







#####################################
def show_data(df):
    """
    Prompts 5 rows of df until user tells the program to stop.
    Input:
        - df (Pandas DataFrame): data to analyse
    No output
    """
    get_data = 'y'
    i=0
    while get_data == 'y':
        if i < df.shape[0]:
            print(df.iloc[i:i+5,:])
            i += 5
            while True:
                get_data = input('Would you like 5 more rows? y/n\n').lower()
                if get_data == 'y':
                    break
                elif get_data == 'n':
                    return
                else:
                    print('Invalid input! Try again:\n')
        else:
            print('You reached end of data!')
            break

    return








#####################################
#####################################
def main():
    bikeshare = True
    while bikeshare:
        c, m, d =get_filters()
        if 'stop' in [c, m, d]:
            bikeshare = False
        else:
            print('-'*40)
            print('Yay! I\'ll analyse the data with the following filters:\nCITY: {}\nMONTH: {}\nDAY: {}\n'.format(c.title(),m,d))
            df=get_data(c,m,d)
            print('FILTERED DATA CONTAIN {} ROWS'.format(df.shape[0]))

            time_stats(df)
            station_stats(df)
            duration_stats(df)
            user_stats(c, df)

            print('-'*40)
            while True:
                get_disp_data = input('Would you like to display the data? y/n\n').lower()
                if get_disp_data == 'y':
                    show_data(df)
                    break
                elif get_disp_data == 'n':
                    break
                else:
                    print('Invalid input! Try again:')


            while True:
                restart=input('Would you like to restart the analysis? y/n\n').lower()
                if restart == 'n':
                    bikeshare = False
                    break
                elif restart != 'y':
                    print('Invalid input! Try again:')
                else:
                    break



if __name__ == "__main__":
    main()
