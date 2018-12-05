import re
import collections


shift_re = re.compile('Guard #(\d*) begins shift')
slept_moments_tpl = collections.namedtuple('slept_moments', 'guard sleep_moments')


def parse_and_sort(lines) -> dict:
    p = {line.split(']')[0].strip('['): line.split(']')[1].strip() for line in lines}
    return {key: p[key] for key in sorted(p.keys())}


def minutes_of(timestamp: str) -> int:
    return int(timestamp.split(' ')[1].split(':')[1])


def find_guard_who_slept_most(slept: dict) -> slept_moments_tpl:
    slept_moments = None
    most_sleep = 0
    for guard, sleeps in slept.items():
        total_slept = sum(sleeps.values())
        if total_slept > most_sleep:
            slept_moments = slept_moments_tpl(guard, sleeps)
            most_sleep = total_slept

    return slept_moments


def most_fqt_sleep_on_same_minute(slept: dict):
    guard = None
    minute, asleep_count = 0, 0
    for g, sleeps in slept.items():
        # m, c = None, None  # Clear the loop variables cause python is dumb
        for m, c in sleeps.items():
            if c > asleep_count:
                minute, asleep_count = m, c
                guard = g
    return guard, minute


def get_slept_moments(sorted_input: dict) -> dict:
    slept = {}  # {guard : {minute : asleep-count}}
    fell_asleep = 0
    for time, event in sorted_input.items():
        match = shift_re.match(event)
        if match:
            guard_on_shift = match.group(1)
            slept.setdefault(guard_on_shift, {})
            continue
        if event == 'falls asleep':
            fell_asleep = minutes_of(time)
            continue
        if event == 'wakes up':
            for minute in range(fell_asleep, minutes_of(time)):
                current = slept[guard_on_shift].setdefault(minute, 0)
                slept[guard_on_shift][minute] = current + 1
    return slept


with open('in.txt') as puzzle_input:
    parsed = parse_and_sort(puzzle_input.readlines())  # {time: event}
    print(parsed)
    guard_sleeps = get_slept_moments(parsed)

    slept_most_guard, slept_most_minute = most_fqt_sleep_on_same_minute(guard_sleeps)
    answer = int(slept_most_guard) * int(slept_most_minute)
    print(slept_most_guard, slept_most_minute, answer)
