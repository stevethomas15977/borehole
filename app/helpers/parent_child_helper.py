
from datetime import datetime
from dateutil.relativedelta import relativedelta

def months_between_dates(date_1, date_2):
    # Parse the input strings to datetime objects
    date_format = "%Y-%m-%d"
    d1 = datetime.strptime(date_1, date_format)
    d2 = datetime.strptime(date_2, date_format)
    
    # Ensure d1 is the later date
    if d2 > d1:
        d1, d2 = d2, d1
    
    # Calculate difference in months and remaining days
    delta_years = d1.year - d2.year
    delta_months = d1.month - d2.month
    delta_days = d1.day - d2.day
    
    # Total months calculation
    months = delta_years * 12 + delta_months + (1 if delta_days > 0 else 0)
    
    return months

def is_at_least_6_months_earlier(parent_date:str, child_date:str) -> bool:
    date_format = "%Y-%m-%d"
    try:
        parent_date = datetime.strptime(parent_date, date_format).date()
        child_date = datetime.strptime(child_date, date_format).date()
    except ValueError as e:
        error(f"Error parsing dates: {parent_date} and {child_date} {e}")
        return False
    # Calculate the date that is 6 months before the child's first production date
    six_months_earlier = child_date - relativedelta(months=6)
    return parent_date <= six_months_earlier