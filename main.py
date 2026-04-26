

import csv

DATA_FILE = "savant_data.csv"
MIN_ATTEMPTS = 8


def make_count(row):
    return row["balls"] + "-" + row["strikes"]


def runners_on(row):
    return row["on_1b"] != "" or row["on_2b"] != "" or row["on_3b"] != ""


def is_success(row, goal):
    description = row.get("description", "").lower()
    events = row.get("events", "").lower()
    bb_type = row.get("bb_type", "").lower()

    if goal == "strike":
        return description in ["called_strike", "swinging_strike", "swinging_strike_blocked", "foul", "foul_tip"]

    if goal == "strikeout":
        return events == "strikeout"

    if goal == "groundout":
        return "ground" in bb_type and events in ["field_out", "force_out", "grounded_into_double_play"]

    if goal == "out":
        return events in ["strikeout", "field_out", "force_out", "grounded_into_double_play", "double_play", "fielders_choice_out"]

    if goal == "avoid_damage":
        return events not in ["single", "double", "triple", "home_run", "walk", "hit_by_pitch"]

    return False


def load_data():
    file = open(DATA_FILE, encoding="utf-8")
    reader = csv.DictReader(file)
    rows = []

    for row in reader:
        if row["pitch_name"] == "":
            continue

        row["count"] = make_count(row)
        row["runners_on"] = "yes" if runners_on(row) else "no"
        rows.append(row)

    return rows


def analyze_pitch_groups(rows, goal):
    groups = {}

    for row in rows:
        key = (
            row["count"],
            row["stand"],
            row["p_throws"],
            row["outs_when_up"],
            row["runners_on"],
            row["pitch_name"]
        )

        if key not in groups:
            groups[key] = {
                "attempts": 0,
                "successes": 0,
                "velo_total": 0,
                "velo_count": 0,
                "spin_total": 0,
                "spin_count": 0
            }

        groups[key]["attempts"] += 1

        if is_success(row, goal):
            groups[key]["successes"] += 1

        if row["release_speed"] != "":
            groups[key]["velo_total"] += float(row["release_speed"])
            groups[key]["velo_count"] += 1

        if row["release_spin_rate"] != "":
            groups[key]["spin_total"] += float(row["release_spin_rate"])
            groups[key]["spin_count"] += 1

    results = []

    for key, value in groups.items():
        count, batter_side, pitcher_hand, outs, runners, pitch = key
        attempts = value["attempts"]
        successes = value["successes"]
        rate = successes / attempts

        avg_velo = "N/A"
        avg_spin = "N/A"

        if value["velo_count"] > 0:
            avg_velo = round(value["velo_total"] / value["velo_count"], 1)

        if value["spin_count"] > 0:
            avg_spin = round(value["spin_total"] / value["spin_count"], 0)

        results.append({
            "count": count,
            "batter_side": batter_side,
            "pitcher_hand": pitcher_hand,
            "outs": outs,
            "runners_on": runners,
            "pitch": pitch,
            "attempts": attempts,
            "successes": successes,
            "rate": rate,
            "avg_velo": avg_velo,
            "avg_spin": avg_spin
        })

    return results


def find_best_pitch(results, count, batter_side, pitcher_hand, outs, runners):
    levels = [
        ("Exact situation: count + batter side + pitcher hand + outs + runners",
         lambda r: r["count"] == count and r["batter_side"] == batter_side and r["pitcher_hand"] == pitcher_hand and r["outs"] == outs and r["runners_on"] == runners),

        ("Count + batter side + pitcher hand + runners",
         lambda r: r["count"] == count and r["batter_side"] == batter_side and r["pitcher_hand"] == pitcher_hand and r["runners_on"] == runners),

        ("Count + batter side + pitcher hand",
         lambda r: r["count"] == count and r["batter_side"] == batter_side and r["pitcher_hand"] == pitcher_hand),

        ("Same count only",
         lambda r: r["count"] == count),

        ("All data fallback",
         lambda r: True)
    ]

    for label, condition in levels:
        filtered = [r for r in results if condition(r) and r["attempts"] >= MIN_ATTEMPTS]

        if len(filtered) > 0:
            filtered.sort(key=lambda r: (r["rate"], r["attempts"]), reverse=True)
            return label, filtered[:5]

    return "No reliable data found", []


def main():
    rows = load_data()

    print("SEQUENCING PLUS PROTOTYPE")
    print("=========================")
    print("Real Statcast rows loaded:", len(rows))

    print("\nThis prototype recommends a pitch based on:")
    print("- count")
    print("- batter side")
    print("- pitcher throwing hand")
    print("- outs")
    print("- runners on base")
    print("- goal")

    count = input("\nEnter count, like 1-2: ")
    batter_side = input("Enter batter side, R or L: ")
    pitcher_hand = input("Enter pitcher hand, R or L: ")
    outs = input("Enter outs, 0, 1, or 2: ")
    runners = input("Are runners on base? yes or no: ")
    goal = input("Enter goal (strike, strikeout, groundout, out, avoid_damage): ")

    results = analyze_pitch_groups(rows, goal)
    label, recommendations = find_best_pitch(results, count, batter_side, pitcher_hand, outs, runners)

    print("\nYour Scenario:")
    print("Count:", count)
    print("Batter side:", batter_side)
    print("Pitcher hand:", pitcher_hand)
    print("Outs:", outs)
    print("Runners on:", runners)
    print("Goal:", goal)

    print("\nRecommendation Method:")
    print(label)

    if len(recommendations) == 0:
        print("\nNo recommendation found.")
    else:
        print("\nTop 5 Pitch Options:")
        print("--------------------")

        for i, r in enumerate(recommendations, start=1):
            print(
                str(i) + ".",
                r["pitch"],
                "-",
                round(r["rate"] * 100, 1),
                "%",
                goal,
                "rate |",
                r["attempts"],
                "pitches |",
                "Avg velo:",
                r["avg_velo"],
                "mph | Avg spin:",
                r["avg_spin"],
                "rpm"
            )

        best = recommendations[0]

        print("\nFinal Recommendation:")
        print("Throw:", best["pitch"])
        print("Reason:", best["pitch"], "had the best", goal, "rate for this situation.")


main()
