from datetime import datetime, timedelta
import calendar


def time_management_system(start_date_str, start_year):
    start_date = datetime.strptime(f"{start_year}/{start_date_str}", '%Y/%m/%d') #2024/3/4
    gap_day = start_date + timedelta(days=7) #2024/3/11
    next_month = gap_day.month + 1 #2024/4/11
    year = gap_day.year #2024
                                                                                            

    if next_month > 12:
        next_month = 1
        year += 1

    try:
        end_date = datetime(year, next_month, gap_day.day)
    except ValueError:
        last_day = calendar.monthrange(year, next_month)[1]
        end_date = datetime(year, next_month, last_day)
    
    end_date_returned = str(end_date.year) + "/" + end_date.strftime('%m/%d')
    end_date_year = str(end_date.year)
    gap_day_returned = str(gap_day.year) + "/" + str(gap_day.month) + "/" + str(gap_day.day)

    next_gap_day = end_date + timedelta(days=7)
    next_gap_day_month = next_gap_day.month + 1
    next_gap_day_year = next_gap_day.year
    if next_gap_day_month > 12:
        next_gap_day_month = 1
        next_gap_day_year += 1
    try:
        next_end_day = datetime(next_gap_day_year, next_gap_day_month, next_gap_day.day)
    except ValueError:
        next_last_day = calendar.monthrange(next_gap_day_year, next_gap_day_month)[1]
        next_end_day = datetime(next_gap_day_year, next_gap_day_month, next_last_day)
    return end_date_returned, gap_day_returned, end_date_year, start_date, next_gap_day, next_end_day