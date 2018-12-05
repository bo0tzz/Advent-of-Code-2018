import re


shift_re = re.compile('Guard #(\d*) begins shift')


def parse_to_sorted(lines):
    lines = {line.split(']')[0].strip('['): line.split(']')[1].strip() for line in lines}
    return {key: lines[key] for key in sorted(lines.keys())}


def minutes_of(timestamp: str) -> int:
    return int(timestamp.split(' ')[1].split(':')[1])


with open('in.txt') as puzzle_input:
    timestamped = parse_to_sorted(puzzle_input.readlines())
    guard_sleeps = {}  # {guard : {minute : asleep-count}}
    guard_on_shift = None
    fell_asleep = None
    for time, text in timestamped.items():
        match = shift_re.match(text)
        if match:
            guard_on_shift = match.group(1)
            continue
        if text == 'falls asleep':
            fell_asleep = minutes_of(time)
            continue
        if text == 'wakes up':
            minute = minutes_of(time)
            slept = minute - fell_asleep
            for minute in range(fell_asleep, minutes_of(time)):
                # The guard slept once on this minute
                guard_sleeps[guard_on_shift][minute] = guard_sleeps.setdefault(guard_on_shift, {}).setdefault(minute, 0) + 1
            fell_asleep = 0

    slept_most_guard = None
    slept_most_minutes = 0
    for guard, sleeps in guard_sleeps.items():
        total_slept = sum(sleeps.values())
        if total_slept > slept_most_minutes:
            slept_most_guard, slept_most_minutes = guard, total_slept

    slept_most = guard_sleeps[slept_most_guard]
    answer = int(max(slept_most, key=slept_most.get)) * int(slept_most_guard)
    print(answer)
