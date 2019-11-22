from typing import List, Set, Tuple
from aoc_utils import read_input_file
from dataclasses import dataclass
from datetime import datetime


@dataclass(init=False, order=True)
class LogRow:
    ts: datetime
    message: str

    def __init__(self, log_row):
        self.ts = datetime.strptime(log_row[1:17], '%Y-%m-%d %H:%M')
        self.message = log_row[19:]

    def __str__(self):
        return f'{str(self.ts)} : {self.message}'


@dataclass(init=False)
class Guard:
    id: int
    sleep_periods: Set[Tuple[int]]
    total_sleep: int

    def __init__(self, guard_id: int):
        self.id = guard_id
        self.sleep_periods = set()
        self.total_sleep = 0

    def add_sleep_period(self, start: datetime, end: datetime):
        self.total_sleep += int((end - start).seconds / 60)
        self.sleep_periods.add(tuple(range(start.minute, end.minute)))

    def most_sleep(self) -> (int, int):
        sleeps = [0] * 60
        for period in self.sleep_periods:
            for minute in period:
                sleeps[minute] += 1
        sleepiest_minute = 0
        for minute, _ in enumerate(sleeps):
            if sleeps[minute] > sleeps[sleepiest_minute]:
                sleepiest_minute = minute
        return sleepiest_minute, sleeps[sleepiest_minute]


def get_guards(log_rows: List[LogRow]):
    guards = dict()
    fell_asleep: datetime = None
    guard = None
    for row in log_rows:
        if row.message.startswith('Guard'):
            guard_id = int(row.message.split()[1][1:])
            if guard_id not in guards:
                guards[guard_id] = Guard(guard_id)
            guard = guards[guard_id]
            fell_asleep = None
        elif row.message == 'falls asleep':
            fell_asleep = row.ts
        elif row.message == 'wakes up':
            guard.add_sleep_period(fell_asleep, row.ts)
            fell_asleep = None
    return guards


def phase_1(log_rows: List[LogRow]) -> int:
    guards = get_guards(log_rows)
    max_sleep = 0
    chosen_one = 0
    for guard_id, guard in guards.items():
        # print(f'Guard {guard.id}: total sleep: {guard.total_sleep}, sleepiest minute: {guard.most_sleep()}')
        if guard.total_sleep > max_sleep:
            max_sleep = guard.total_sleep
            chosen_one = guard_id
    return chosen_one * guards[chosen_one].most_sleep()[0]


def phase_2(log_rows: List[LogRow]) -> int:
    guards = get_guards(log_rows)
    max_frequency = 0
    chosen_minute = 0
    chosen_one = 0
    for guard_id, guard in guards.items():
        sleep = guard.most_sleep()
        if sleep[1] > max_frequency:
            chosen_one = guard_id
            chosen_minute = sleep[0]
            max_frequency = sleep[1]
    return chosen_one * chosen_minute


if __name__ == "__main__":
    log_rows = sorted(list(map(LogRow, read_input_file('04'))))
    # log_rows = sorted(list(map(LogRow, read_input_file('04_example'))))
    print(f'Phase 1: {phase_1(log_rows)}')
    print(f'Phase 2: {phase_2(log_rows)}')
