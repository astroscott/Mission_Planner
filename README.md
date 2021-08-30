# Mission_Planner

## Download and Run a Local Copy (Python 3.6+)

Basic setup:

`cd /your/directory`<br>
`git clone https://github.com/astroscott/Mission_Planner`<br>
`pip -r requirements.txt`<br>
`streamlit run app.py`<br>

Or optionally install within its own virtual environment:

`cd /your/directory`<br>
`python3 -m venv env`<br>
`source env/bin/activate`<br>
`git clone https://github.com/astroscott/Mission_Planner`<br>
`pip -r requirements.txt`<br>
`streamlit run app.py`<br>

## Introduction
Mission Planner is a tool for planning interplanetary missions between any two planets in our solar system via dynamic, interactive porkchop plots. The tool uses the Vallado algorithm for solving Lambert's targeting problem.<br>

Assumptions: Patched conics, impulsive maneuvers, ballistic trajectories<br>

## Usage Recommenations
If performing a search yourself for dates different than those listed below, use the following strategy:
display only the Delta V plot, increase the calculation increment to between 10-30 (higher values require less calculation time), set the contour upper bound to 50, increase the contour line increment to 2, pick a departure year (ie: 2022-01-01 -> 2023-12-31), then set a large range of arrival dates (actual range depends on planet, 
see values below for an idea). After loading, when you see contours on the plot, adjust the dates until you 
have centered the contours. Once centered, lower the date increment to 1 for the highest resolution plot,
and adjust other values as you see fit.<br>

**Tip: Load times will increase quickly with increasing date ranges, raise calculation increment as needed**

**Tip: If you don't see anything after load, increase the date range and increase the contour upper bound.**<br>

## 2022 Launch Windows

Some convenient search windows for 2022 to view the minimal requisite delta-V and specific orbital energy from Earth to each planet in our solar system are as follows:<br>

...to be updated...