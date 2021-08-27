# Mission_Planner

## Introduction
Mission Planner is a tool for planning interplanetary missions between any two planets in our solar system via dynamic, interactive porkchop plots. <br>

The tool uses the Vallado algorithm for solving Lambert's targeting problem.
Assumptions: Patched conic approximation, impulsive maneuvers, ballistic trajectory<br>

## Search Recommenations
If performing a search yourself for dates different than those listed below, use the following strategy:
switch to a delta-V plot, increase the date increment to between 10-30 (higher values require less calculation 
time), set the contour upper bound to 60, increase the contonour line increment to 2, pick a departure year 
(ie: 2022-01-01 -> 2023-12-31), then set a large range of arrival dates (actual range depends on planet, 
see above values for an idea). After loading, when you see contours on the plot, adjust the dates until you 
have centered the contours. Once centered, lower the date increment to 1 for the highest resolution plot,
and adjust other values as you see fit.<br>

Tip: If you don't see anything while searching, increase the date range and increase the contour upper bound.<br>

Some convenient search windows for 2022 to view the minimal requisite delta-V and specific orbital energy from Earth to each planet in our solar system are as follows:<br>

Earth -> Mercury:<br>
Departure: [2022-08-01 ,2022-12-01]<br>
Arrival: [2023-01-01, 2023-03-01]<br>

Earth -> Venus:<br>
Departure: [2022-11-01, 2023-11-01]<br>
Arrival: [2023-07-01, 2024-02-01]<br>

Earth -> Mars:<br>
Departure: [2022-07-01, 2022-11-01]<br>
Arrival: [2023-01-01, 2024-01-01]<br>

Earth -> Jupiter<br>
Departure: [2022-04-01, 2022-09-01]<br>
Arrival: [2023-01-01, 2029-01-01]<br>

Earth -> Saturn<br>
Departure: [2022-01-01, 2022-09-01]<br>
Arrival: [2025-01-01, 2032-01-01]<br>

Earth -> Uranus<br>
Departure: [2022-05-01, 2022-09-01]<br>
Arrival: [2029-01-01, 2049-01-01]<br>

Earth -> Neptune<br>
Departure: [2022-03-01, 2022-08-01]<br>
Arrival: [2040-01-01, 2075-01-01]<br>

Earth -> Pluto<br>
Departure: [2022-01-01, 2022-06-01]<br>
Arrival: [2035-01-01, 2080-01-01]<br>
