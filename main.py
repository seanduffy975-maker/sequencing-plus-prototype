
import csv

DATA_FILE = "savant_data.csv"

# minimum pitches needed before trusting a scenario
MIN_ATTEMPTS = 10


def make_count(row):
    return row["balls"] + "-" + row["strikes"]


def is_success(row, goal):
    description = row.get("description", "").lower()
    events = row.get("events", "").lower()
    bb_type = row.get("bb_type", "").lower()

    if goal == "strike":
        return description in [
            "called_strike",
            "swinging_strike",
            "swinging_strike_blocked",
            "foul",
            "foul_tip"
        ]

    if goal == "strikeout":
        return events == "strikeout"

    if goal == "groundout":
        return ("ground" in bb_type and "out" in events) or events == "grounded_into_double_play"

    if goal == "out":
        return events in [
            "strikeout",
            "field_out",
            "force_out",
            "grounded_into_double_play",
            "double_play",
            "fielders_choice_out"
        ]

    # default: avoid damage
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
        rows.append(row)

    return rows


def analyze_pitch_groups(rows, goal):
    groups = {}

    for row in rows:
        key = (
            row["count"],
            row["stand"],
            row["p_throws"],
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
        count, batter_side, pitcher_hand, pitch = key
        attempts = value["attempts"]
        successes = value["successes"]
        rate = successes / attempts

        avg_velo = None
        if value["velo_count"] > 0:
            avg_velo = value["velo_total"] / value["velo_count"]

        avg_spin = None
        if value["spin_count"] > 0:
            avg_spin = value["spin_total"] / value["spin_count"]

        results.append({
            "count": count,
            "batter_side": batter_side,
            "pitcher_hand": pitcher_hand,
            "pitch": pitch,
            "attempts": attempts,
            "successes": successes,
            "rate": rate,
            "avg_velo": avg_velo,
            "avg_spin": avg_spin
        })

    return results


def find_best_pitch(results, count, batter_side, pitcher_hand):
    # fallback levels from most specific to least specific
    levels = [
        ("Exact count + batter side + pitcher hand",
         lambda r: r["count"] == count and r["batter_side"] == batter_side and r["pitcher_hand"] == pitcher_hand),

        ("Same count + batter side",
         lambda r: r["count"] == count and r["batter_side"] == batter_side),

        ("Same count + pitcher hand",
         lambda r: r["count"] == count and r["pitcher_hand"] == pitcher_hand),

        ("Same count only",
         lambda r: r["count"] == count),

        ("All data",
         lambda r: True)
    ]

    for label, condition in levels:
        filtered = [r for r in results if condition(r) and r["attempts"] >= MIN_ATTEMPTS]

        if len(filtered) > 0:
            filtered.sort(key=lambda r: (r["rate"], r["attempts"]), reverse=True)
            return label, filtered[:5]

    return "No reliable data found", []


def print_top_overall(results):
    filtered = [r for r in results if r["attempts"] >= MIN_ATTEMPTS]
    filtered.sort(key=lambda r: (r["rate"], r["attempts"]), reverse=True)

    print("\nTop Overall Pitch Scenarios:")
    print("----------------------------")

    for r in filtered[:10]:
        print(
            r["count"],
            "vs", r["batter_side"],
            "batter,",
            r["pitcher_hand"], "pitcher,",
            r["pitch"],
            "-",
            round(r["rate"] * 100, 1), "%",
            "success on",
            r["attempts"],
            "pitches"
        )


def print_recommendations(recommendations, label, goal):
    print("\nRecommendation Method:")
    print(label)

    print("\nBest Pitch Options:")
    print("-------------------")

    for r in recommendations:
        velo = "N/A"
        spin = "N/A"

        if r["avg_velo"] is not None:
            velo = str(round(r["avg_velo"], 1)) + " mph"

        if r["avg_spin"] is not None:
            spin = str(round(r["avg_spin"], 0)) + " rpm"

        print(
            r["pitch"],
            "-",
            round(r["rate"] * 100, 1), "%",
            goal,
            "rate |",
            r["attempts"],
            "pitches |",
            "Avg velo:",
            velo,
            "| Avg spin:",
            spin
        )


def main():
    rows = load_data()

    print("SEQUENCING PLUS PROTOTYPE")
    print("=========================")
    print("Real Statcast rows loaded:", len(rows))

    print("\nThis prototype recommends pitches based on:")
    print("- count")
    print("- batter side")
    print("- pitcher throwing hand")
    print("- goal: strike, strikeout, groundout, out, or avoid_damage")

    print("\nExample inputs:")
    print("Count: 1-2")
    print("Batter side: R or L")
    print("Pitcher hand: R or L")
    print("Goal: strikeout")

    count = input("\nEnter count, like 1-2: ")
    batter_side = input("Enter batter side, R or L: ")
    pitcher_hand = input("Enter pitcher hand, R or L: ")
    goal = input("Enter goal (strike, strikeout, groundout, out, avoid_damage): ")

    results = analyze_pitch_groups(rows, goal)

    print_top_overall(results)

    label, recommendations = find_best_pitch(results, count, batter_side, pitcher_hand)

    print("\nYour Scenario:")
    print("Count:", count)
    print("Batter side:", batter_side)
    print("Pitcher hand:", pitcher_hand)
    print("Goal:", goal)

    if len(recommendations) == 0:
        print("\nNo recommendation found.")
    else:
        print_recommendations(recommendations, label, goal)

        best = recommendations[0]
        print("\nFinal Recommendation:")
        print(
            "Best pitch:",
            best["pitch"],
            "because it had a",
            round(best["rate"] * 100, 1),
            "%",
            goal,
            "rate in this sample."
        )


main()
