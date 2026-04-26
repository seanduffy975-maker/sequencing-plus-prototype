# Sequencing Plus Prototype

**Name:** Sean Duffy  
**Course:** CIS 1051  
**Project:** Final Project  
**Video Demo:** [PASTE VIDEO LINK HERE]

## Project Overview

Sequencing Plus Prototype is a Python project that analyzes real Statcast pitch data from Baseball Savant and recommends the best pitch for specific game situations.

The goal of the project is to build a prototype pitch sequencing model that uses situational variables to support pitch selection decisions.

## What the Program Does

The program asks the user for:

- Count
- Batter handedness
- Pitcher throwing hand
- Number of outs
- Whether runners are on base
- Desired goal (strike, strikeout, groundout, out, or avoid damage)

Using those inputs, the program filters real Statcast data and ranks the top five pitch options based on success rate and sample size, then gives a final pitch recommendation.

## Example

Example input:

- Count: 1-2  
- Batter Side: R  
- Pitcher Hand: L  
- Outs: 1  
- Runners On Base: Yes  
- Goal: Strikeout

Example output:

1. Curveball  
2. Slider  
3. Split-Finger  

Final Recommendation: Throw Curveball

In this example, the recommendation is based on the highest strikeout success rate in that specific scenario.

## Challenges

One challenge was taking a much larger idea and turning it into a realistic prototype for a class project. My original concept included many more variables, but I narrowed it down to core situational inputs while keeping the main sequencing idea intact.

Another challenge was working through a large real Statcast dataset and identifying which variables were most useful for the model.

## What I Learned

Through this project I learned how Python can be used for sports analytics, how to work with CSV data, organize information with dictionaries, filter data by multiple conditions, and build a basic recommendation engine from real data.

I also learned how model complexity has to be balanced with usability and sample size.

## Future Improvements

Future versions could include:

- Weather conditions
- Batter hot and cold streaks
- Pitch location and tunneling
- Multi-pitch sequence prediction
- Pitcher-specific scouting models
- Expanded expected outcome modeling