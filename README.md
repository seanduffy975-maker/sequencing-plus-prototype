
# Sequencing Plus Prototype

**Name:** Sean Duffy
**Course:** CIS 1051
**Project:** Final Project
**Video Demo:** [PASTE VIDEO LINK HERE]

## Project Overview

Sequencing Plus Prototype is a Python program that analyzes real Statcast pitch data from Baseball Savant. The goal is to recommend the best pitch for different game situations.

The program uses count, batter side, pitcher throwing hand, and a selected goal to recommend pitches. The goal can be strike, strikeout, groundout, out, or avoid damage.

## What the Program Does

The program asks the user for:

- Count
- Batter side
- Pitcher hand
- Goal

Then it analyzes the Statcast data and recommends the best pitch for that situation.

## Example

If the user enters:

- Count: 1-2
- Batter side: R
- Pitcher hand: L
- Goal: strikeout

The program looks through the data and recommends the pitch with the highest strikeout rate for that situation.

## Challenges

One challenge was keeping the project realistic. My original idea was much bigger and would include things like weather, player hot streaks, and more advanced scouting data. For this class, I narrowed it down into a prototype that still shows the main idea.

Another challenge was working with real Statcast data because the file had a lot of columns. I had to figure out which columns mattered most for the project.

## What I Learned

I learned how Python can be used to analyze real sports data. I also learned how to read CSV files, use dictionaries, filter data by conditions, and make basic recommendations from the results.

## Future Improvements

In the future, I would like to add:

- Weather
- Batter hot/cold streaks
- Pitch location
- More advanced sequencing
- Real pitcher-specific reports