import sys
import csv
import math
import argparse

def parse_point(s):
    return tuple(map(float, s.strip().replace('"', "").strip("()").split(",")))

def format_point(p):
    return f'"({p[0]},{p[1]},{p[2]})"'

def vector_sub(a, b):
    return tuple(ai - bi for ai, bi in zip(a, b))

def vector_add(a, b):
    return tuple(ai + bi for ai, bi in zip(a, b))

def vector_scale(v, scale):
    return tuple(vi * scale for vi in v)

def vector_normalize(v):
    length = math.sqrt(sum(vi ** 2 for vi in v))
    if length == 0:
        raise ValueError("Zero-length vector")
    return tuple(vi / length for vi in v)

def generate_continuation_chargers(front_left, front_right, back_right, length, width, count, power, efficiency, reverse=False):
    right_vector = vector_sub(front_right, front_left)
    right_unit = vector_normalize(right_vector)

    back_vector = vector_sub(back_right, front_right)
    length_unit = vector_normalize(back_vector)

    if reverse:
        length_unit = vector_scale(length_unit, -1)

    chargers = []
    current_front_left = front_left
    current_front_right = front_right

    for _ in range(count):
        current_back_right = vector_add(current_front_right, vector_scale(length_unit, length * -1))
        chargers.append((current_front_left, current_front_right, current_back_right, power, efficiency))
        current_front_left = vector_add(current_front_left, vector_scale(length_unit, -length))
        current_front_right = vector_add(current_front_right, vector_scale(length_unit, -length))

    return chargers

def main():
    parser = argparse.ArgumentParser(description="Generate charger CSV data")
    parser.add_argument("csv_file", help="Path to input CSV with a sample charger")
    parser.add_argument("length", type=float, help="Charger length")
    parser.add_argument("width", type=float, help="Charger width")
    parser.add_argument("power", type=float, help="Charger power")
    parser.add_argument("efficiency", type=float, help="Charger efficiency")
    parser.add_argument("count", type=int, help="Number of chargers to generate (including the head)")
    parser.add_argument("--reverse", action="store_true", help="Place chargers in reverse direction")

    args = parser.parse_args()

    with open(args.csv_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                front_left = parse_point(row[0])
                front_right = parse_point(row[1])
                back_right = parse_point(row[2])
                break
            except:
                continue  # skip header or malformed row

    print("front_left,front_right,back_right,power,efficiency")
    print(f"{format_point(front_left)},{format_point(front_right)},{format_point(back_right)},{args.power},{args.efficiency}")

    chargers = generate_continuation_chargers(
        front_left, front_right, back_right,
        args.length, args.width, args.count - 1,
        args.power, args.efficiency,
        reverse=args.reverse
    )

    for c in chargers:
        print(f"{format_point(c[0])},{format_point(c[1])},{format_point(c[2])},{c[3]},{c[4]}")

if __name__ == "__main__":
    main()
