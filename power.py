# Classroom Timetable Generator (PS No. 75) 

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


def get_input():
    # number of days 

    while True:
        try:
            days = int(input("Enter number of days (1 to 6): "))
            if 1 <= days <= 6:
                break
            print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Enter a whole number.")

    
    while True:
        try:
            periods_in_a_day = int(input("Enter periods per day: "))
            if periods_in_a_day > 0:
                break
            print("Please enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Enter a whole number.")

    # subjects and weekly periods :

    subjects = []
    seen = []
    print("Enter subjects and periods (e.g. Maths 3, Physics 2 or one by one, blank line to finish):")

    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            if len(subjects) > 0:
                break
            raise

        if line == "" or line.lower() == "done":
            if len(subjects) == 0:
                print("Please enter at least one subject.")
                continue
            break


        if "," in line:
            parts = line.split(",")
            temp = []
            temp_seen = list(seen)
            ok = True

            for part in parts:
                words = part.strip().rsplit(None, 1)
                if len(words) != 2:
                    print("Invalid format. Use: Subject Periods")
                    ok = False
                    break

                name = words[0].strip()
                if name == "" or name.lower() in temp_seen:
                    print("Subject name cannot be empty or duplicate.")
                    ok = False
                    break

                try:
                    count = int(words[1])
                except ValueError:
                    print("Periods must be a whole number.")
                    ok = False
                    break

                if count <= 0:
                    print("Periods must be greater than 0.")
                    ok = False
                    break

                temp.append((name, count))
                temp_seen.append(name.lower())

            if ok:
                subjects.extend(temp)
                seen = temp_seen
                break
            continue

        # One-by-one input: "Maths 3" or just "Maths"

        words = line.rsplit(None, 1)
        if len(words) == 2:
            try:
                count = int(words[1])
                name = words[0].strip()
                if name == "" or name.lower() in seen:
                    print("Subject name cannot be empty or duplicate.")
                elif count <= 0:
                    print("Periods must be greater than 0.")
                else:
                    subjects.append((name, count))
                    seen.append(name.lower())
                continue
            except ValueError:
                pass

        # If only subject name was given,  periods: 

        name = line
        if name.lower() in seen:
            print("Duplicate subject. Enter a different subject.")
            continue

        while True:
            try:
                count = int(input(f"Enter weekly periods for {name}: "))
                if count > 0:
                    break
                print("Periods must be greater than 0.")
            except ValueError:
                print("Invalid input. Enter a whole number.")

        subjects.append((name, count))
        seen.append(name.lower())

    return days, periods_in_a_day, subjects


def validate(days, periods_per_day, subjects):
    # Now Checking total weekly periods against total slots
    total_slots = days * periods_per_day
    total_periods = 0
    for _, count in subjects:
        total_periods += count

    if total_periods != total_slots:
        print(f"Error: Total weekly periods ({total_periods}) must equal available slots ({total_slots}).")
        return False

    for name, count in subjects:
        if count > days * 2:
            day_word = "day" if days == 1 else "days"
            print(f"Timetable cannot be generated: {name} needs {count} periods in {days} {day_word}, but the limit is 2 per day.")
            return False

    return True


def generate_timetable(days, periods_per_day, subjects):
    
    remaining = {}
    order = []
    for name, count in subjects:
        remaining[name] = count
        order.append(name)

    timetable = []

    for d in range(days):

        # Now TRacking how many times each subject is used today '''

        used_today = {}
        for name in order:
            used_today[name] = 0

        day_slots = []

        for p in range(periods_per_day):
            best_subject = None
            best_left = 0

            # Picking eligible subject with most periods left 

            for name in order:
                if remaining[name] > 0 and used_today[name] < 2:
                    if remaining[name] > best_left:
                        best_subject = name
                        best_left = remaining[name]

            if best_subject is None:
                print(f"Timetable cannot be generated: stuck at {DAYS[d]} period {p + 1}.")
                return None

            day_slots.append(best_subject)
            remaining[best_subject] -= 1
            used_today[best_subject] += 1

        timetable.append((DAYS[d], day_slots))

    return timetable


def print_timetable(timetable):
    # Print each day's schedule
    for day_name, slots in timetable:
        print(f"{day_name}: {', '.join(slots)}")


def main():
    days, periods_per_day, subjects = get_input()
    if validate(days, periods_per_day, subjects):
        timetable = generate_timetable(days, periods_per_day, subjects)
        if timetable is not None:
            print_timetable(timetable)


if __name__ == "__main__":
    main()