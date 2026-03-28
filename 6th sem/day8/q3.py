from itertools import permutations


def solve_send_more_money():
    letters = ("S", "E", "N", "D", "M", "O", "R", "Y")
    digits = range(10)

    attempts = 0

    for perm in permutations(digits, len(letters)):
        mapping = dict(zip(letters, perm))

        if mapping["S"] == 0 or mapping["M"] == 0:
            continue

        send = (
            mapping["S"] * 1000
            + mapping["E"] * 100
            + mapping["N"] * 10
            + mapping["D"]
        )
        more = (
            mapping["M"] * 1000
            + mapping["O"] * 100
            + mapping["R"] * 10
            + mapping["E"]
        )
        money = (
            mapping["M"] * 10000
            + mapping["O"] * 1000
            + mapping["N"] * 100
            + mapping["E"] * 10
            + mapping["Y"]
        )

        attempts += 1

        if send + more == money:
            return mapping, send, more, money, attempts

    return None, None, None, None, attempts


def print_solution(mapping, send, more, money, attempts):
    print("=" * 60)
    print("Cryptarithmetic Problem: SEND + MORE = MONEY")
    print("=" * 60)

    if mapping is None:
        print("No solution found.")
        print(f"Checked assignments: {attempts}")
        return

    print("\nDigit Assignment:")
    for key in sorted(mapping.keys()):
        print(f"{key} = {mapping[key]}")

    print("\nVerification:")
    print(f"  SEND  = {send}")
    print(f"  MORE  = {more}")
    print(f"  MONEY = {money}")
    print(f"\n  {send} + {more} = {money}")
    print("  Equation satisfied: ✓")
    print(f"\nChecked assignments before solution: {attempts}")


def main():
    mapping, send, more, money, attempts = solve_send_more_money()
    print_solution(mapping, send, more, money, attempts)


if __name__ == "__main__":
    main()