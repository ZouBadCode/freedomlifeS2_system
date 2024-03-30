from datetime import datetime
import pytz
def compare_time(strat_time_to_compare, end_time_to_compare, submit_time_to_compare):
    utc_zone = pytz.utc
    taiwan_zone = pytz.timezone('Asia/Taipei')
    tran_start_time_to_compare = datetime.strptime(strat_time_to_compare, "%Y-%m-%d %H:%M:%S")
    tran_end_time_to_compare = datetime.strptime(end_time_to_compare, "%Y/%m/%d")
    tran_submit_time_to_compare = datetime.fromisoformat(submit_time_to_compare.replace('Z','+00:00')).replace(tzinfo=utc_zone)
    tran_submit_time_to_compare_taiwan = tran_submit_time_to_compare.astimezone(taiwan_zone)
    tran_submit_time_to_compare_taiwan_strftime = tran_submit_time_to_compare_taiwan.strftime('%Y-%m-%d %H:%M:%S')
    print(tran_start_time_to_compare,tran_end_time_to_compare,tran_submit_time_to_compare_taiwan_strftime)
compare_time("2024-03-04 00:00:00","2024/04/11","2024-03-03T16:27:28.204Z")