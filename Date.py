import Restrict


@Restrict.check_attribute
class Date:
    day = int  # DD
    month = int  # MM
    year = int  # YY or YYYY

    def __init__(self, day=0, month=0, year=0):
        # 0-0-0 indicates animal have not departed or date has not been specified
        if day == 0 and month == 0 and year == 0:
            self.day = 0
            self.year = 0
            self.month = 0
        elif self.month_check(month) and self.year_check(year) and self.day_check(month, day, year):
            self.day = day
            self.month = month
            self.year = year
        else:
            print("Wrong date format or date does not exist")

    def month_check(self, m):
        return 1 <= m <= 12 and 1 <= len(str(m)) <= 2

    def year_check(self, y):
        return 1 <= len(str(y)) <= 2 or len(str(y)) == 4

    def day_check(self, m, d, y):
        if len(str(d)) > 2:
            return False

        if m in [1, 3, 5, 7, 8, 10, 12]:
            return 1 <= d <= 31

        if m in [4, 6, 9, 11]:
            return 1 <= d <= 30

        if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) and m == 2:  # leap year
            return 1 <= d <= 29

        if m == 2:
            return 1 <= d <= 28

    def __str__(self):
        if self.day == 0 and self.month == 0 and self.year == 0:
            return ""
        else:
            return "{}-{}-{}".format(str(self.day).zfill(2), str(self.month).zfill(2),
                                     ("20" + str(self.year)) if (self.year != 0 and len(str(self.year)) != 4)
                                     else str(self.year).zfill(4))

def date_format(date):
    if date != '':
        delimiter = '-' if ('-' in date) else '/'
        items = list(map(int, date.split(delimiter)))
        return Date(items[0], items[1], items[2])
    else:
        return Date()

