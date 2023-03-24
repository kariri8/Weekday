from typing import List, Tuple, Dict, Optional, Union, Literal
import random


class WrongDate(Exception):
    def __init__(self, reason):
        self.__reason = reason

    def __repr__(self):
        return self.__reason


class Date:
    year: int
    month: int
    day: int

    # In monthnames, the first name is the 'preferred name', which will be used
    # when printing. Any further names are optional names.
    # One can also add different languages.

    monthnames: Tuple[List[Union[str, int]], ...] = (
        ['january', 'jan', 1, '1'], ['february', 'feb', '2', 2],
        ['march', 3, '3'],
        ['april', 4, '4'], ['may', 5, '5'], ['june', 6, '6'],
        ['july', 7, '7'], ['august', 8, '8'],
        ['september', 'sept', 9, '9'], ['october', 'oct', 10, '10'],
        ['november', 'nov', 11, '11'],
        ['december', 'dec', 12, '12'])

    monthindex: Dict[Union[str, int], int] = {name: ind
                                              for ind, names in enumerate(monthnames) for name in names}

    normalyear = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    leapyear = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    weekdays = ('sunday', 'monday', 'tuesday', 'wednesday',
                'thursday', 'friday', 'saturday')

    @classmethod
    def __init__(self, year : int, month : Union[ int, str ], day : int ):
        if not isinstance( year, int ):
            raise WrongDate( f"year {year} is not an integer " )
        if year < 1900 or year > 2100:
            raise WrongDate( f"year {year} is not between 1900 and 2100" )
        if month not in self.monthindex:
            raise WrongDate( f"unknowm month {month}" )
        if not isinstance( day, int):
            raise WrongDate( f"day {day} is not an integer")
        if isleapyear( year ):
            if day < 1 or day > self.leapyear[self.monthindex[month]]:
                raise WrongDate( f"month {month} does not have {day} in year {year}" )
        else :
            if day < 1 or day > self.normalyear[self.monthindex[month]]:
                raise WrongDate( f"month {month} does not have {day} in year {year}" )
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def __repr__(self) -> str :
        return f"({self.year}, {self.month}, {self.day} )"

    @classmethod
    def __str__(self) -> str :
        return f"{self.day} {self.monthnames[self.monthindex[self.month]][0]} {self.year} "

    @classmethod
    def weekday( self ) -> str:
        d = 0
        for i in range (1900, self.year):
            if isleapyear(i):
                d = d + 366
            else:
                d = d + 365
        if isleapyear(self.year):
            for j in range(self.monthindex[self.month]):
                d = d + self.leapyear[j]
        else:
            for j in range(self.monthindex[self.month]):
                d = d + self.normalyear[j]
        d = d + self.day
        return f"{self.weekdays[d%7]}"


def lucky_dates():
    return [(1956, 1, 31, 'tuesday', 'birthday of Guido Van Rossum'),
            (1945, 'october', 24, 'wednesday', 'Founding of UN'),
            (1969, 'july', 20, 'sunday', 'first moon landing'),
            (1991, 'dec', 16, 'monday', 'independence of Kazakhstan'),
            (1961, 'april', 12, 'wednesday', 'space flight of Yuri Gagarin'),
            (2022, 'september', 17, 'saturday', 'Nursultan renamed into Astana')]


def unlucky_dates():
    return [(1912, 'april', 15, 'monday', 'sinking of Titanic'),
            (1929, 'october', 29, 'tuesday',
             'Wall Street Market Crash (Black Tuesday)'),
            (1959, 'february', 3, 'tuesday', 'the day the music died'),
            (1977, 'march', 27, 'sunday', 'Los Rodeos collision'),
            (2019, 'march', 23, 'saturday', 'Astana renamed into Nursultan'),
            (2022, 'october', 21, 'friday', '!! deadline of this exercise !!')]

@staticmethod
def isleapyear( y : int ) -> bool:
    if y % 4 == 0:
        if y % 100 == 0:
            if y % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def tester():
    for date in (('a', 1, 1), (2, 'x', 3), (3, 4, 'y'),
                 (1900, 'x', 12),
                 (1899, 1, 1), (1900, 1, 1), (1900, 'jan', 1),
                 (1910, 12, 31), (1911, 3.14, 8),
                 (1900, 'feb', 28), (1900, 'feb', 29)):
        try:
            y, m, d = date
            print("testing {} {} {}".format(y, m, d))

            dt = Date(y, m, d)
            print("date = {}".format(dt))

        except WrongDate as w:
            print("   exception {}".format(w))
        print("")

    dates = lucky_dates() + unlucky_dates()
    random.shuffle(dates)

    for date in dates:
        y, m, d, w1, importance = date
        dt = Date(y, m, d)
        w2 = dt.weekday()
        print("{} : {} ({})".format(importance, dt, w2))
        if w1 != w2:
            print("function weekday returned {} but correct day is {} !!!".format(w2, w1))
        print("")

    print("tests finished")
