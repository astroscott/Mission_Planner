from Tools import *
from Planet import *
from Initialize import *
import streamlit as st

# Initialize Configuration
config = Initialize.config()

# Initialize Data:
dd, jdd = Tools.Date.getRange(config["dd"][0], config["dd"][1], config["d_inc"]) # Departure dates
ad, jad = Tools.Date.getRange(config["ad"][0], config["ad"][1], config["d_inc"]) # Arrival dates
Body0 = Planet(config["db"]) # Depature Body
Body1 = Planet(config["ab"]) # Arrival Body

# Solve for departure/arrival body position and velocity, as well as 
# requisite characteristic energy, arrival excess velocity, velocity increment, and time of flight.
(rP0, vP0, rP1, vP1, c3s0, c3l0, vinfs1, vinfl1, dVs, dVl, tofs) = Tools.Transfer.solve(config["k"], Body0, Body1, jdd, jad)

# Create Plot
st.title(config["plt_title"])
st.write("By [Aaron Scott](https://www.linkedin.com/in/aaron-scott-899797216/), visit the [GitHub repository](https://www.github.com/astroscott/Mission_Planner) for full source code.")
config["plt_title"] = "Mission: " + config["db"] + " to " + config["ab"] + " " + str(dd[0].tolist().year) + ", Type 1, 2 Transfers"
st.plotly_chart(Tools.Plot.porkchop(config, dd, ad, c3s0, c3l0, vinfs1, vinfl1, dVs, dVl, tofs), use_container_width=True)