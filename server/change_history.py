"""Calculates change statistics for all modules."""

import datetime
import sqlite3

import settings
import utils

# Aliases.
timedelta = datetime.timedelta
datetime = datetime.datetime
settings = settings.settings


class _TimeUnit:
    PERIOD_IN_DAYS = 14
    CUTOFF_PERIODS = -10

    def __init__(self, date):
        date = datetime.strptime(date, '%Y%m%d')
        period_index = ((date - datetime(date.year, 1,
                                         1)).days // self.PERIOD_IN_DAYS) + 1
        if period_index % 2 == 1:
            period_index += 1
        self._date = date
        self._year = date.year
        self._period_index = period_index

    @property
    def year(self):
        return self._year

    @property
    def period_index(self):
        return self._period_index

    @classmethod
    def get_cutoff_date(cls):
        now = datetime.now()
        cutoff_date = now + timedelta(cls.PERIOD_IN_DAYS * cls.CUTOFF_PERIODS)
        return cutoff_date.strftime('%Y%m%d')

    def count_periods_since_now(self):
        now = datetime.now()
        diff = (now - self._date).days
        return 1 + diff // self.PERIOD_IN_DAYS

    def __eq__(self, other):
        return self.period_index == other.period_index and self.period_index == other.period_index

    def __hash__(self):
        return hash((self.year, self.period_index))

    def __lt__(self, other):
        if self.year < other.year:
            return True
        if self.year > other.year:
            return False
        return self.period_index < other.period_index

    def __repr__(self):
        return f'Week({self.year}, {self.period_index})'


class _ChangeHistory:
    def __init__(self, filepath):
        self._module_name = utils.get_module_from_path(filepath)
        self._periods = set()
        self._latest_periods = set()

    def __repr__(self):
        """Make debugging easy!"""
        p = list(self._periods)
        p.sort()

        lp = list(self._latest_periods)
        lp.sort()

        return f'{self.changes_count} =>  {self.lifespan} => {self.change_rate}  => {self.latest_changes_count} =>  {self.name} => {p} => {lp}'

    def __lt__(self, other):
        return self.change_rate < other.change_rate

    @property
    def lifespan(self):
        """Returns the number of weeks since the module was created.

        :return: The number of weeks since the module was created.
        :rtype: int
        """
        return min(self._periods).count_periods_since_now()

    @property
    def lifespan_in_days(self):
        periods = min(self._periods).count_periods_since_now()
        return periods * _TimeUnit.PERIOD_IN_DAYS

    @property
    def changes_count(self):
        return len(self._periods)

    @property
    def latest_changes_count(self):
        return len(self._latest_periods)

    @property
    def change_rate(self):
        rate = int((len(self._periods) / self.lifespan) * 100)
        return rate if rate <= 100 else 100

    @property
    def name(self):
        return self._module_name

    def add_change_date(self, date):
        self._periods.add(_TimeUnit(date))
        cutoff_date = _TimeUnit.get_cutoff_date()
        if date >= cutoff_date:
            self._latest_periods.add(_TimeUnit(date))


def load_change_history():
    """Loads the history for each module.

    :returns: A list of _ChangeHistory instances.
    :rtype: list.
    """
    changes = {}
    conn = sqlite3.connect(settings.history_db)
    c = conn.cursor()
    for row in c.execute('SELECT name, date FROM history'):
        module_name = utils.get_module_from_path(row[0]).strip()
        date = row[1].strip()
        if module_name not in changes:
            changes[module_name] = _ChangeHistory(module_name)
        changes[module_name].add_change_date(date)
    conn.close()
    return changes


if __name__ == '__main__':
    changes = load_change_history()
    # changes.sort()

    for k, v in changes.items():
        print(v)
