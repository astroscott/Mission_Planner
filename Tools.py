import plotly.graph_objects as go
import streamlit as st
import jdcal as jd
import numpy as np
import datetime

from astropy import units as u
from poliastro.iod.vallado import lambert

class Tools:
    
    class Transfer:
        @classmethod
        @st.cache
        def solve(cls, k, Body0, Body1, jdd, jad):

            num_departures = len(jdd)
            num_arrivals = len(jad)

            # Initialize Data Arrays:
            c3s0 = np.zeros((num_arrivals, num_departures))
            c3s1 = np.zeros((num_arrivals, num_departures))
            c3l0 = np.zeros((num_arrivals, num_departures))
            c3l1 = np.zeros((num_arrivals, num_departures))
            dVs0 = np.zeros((num_arrivals, num_departures))
            dVs1 = np.zeros((num_arrivals, num_departures))
            dVl0 = np.zeros((num_arrivals, num_departures))
            dVl1 = np.zeros((num_arrivals, num_departures))

            jdd_grid, jad_grid = np.meshgrid(jdd, jad)
            tofs = jad_grid - jdd_grid

            rP0, vP0 = Body0.getCoords(jdd) # [km, km/s]
            rP1, vP1 = Body1.getCoords(jad) # [km, km/s]
            rP0 = rP0.transpose()
            rP1 = rP1.transpose()
            vP0 = vP0.transpose()
            vP1 = vP1.transpose()   

            for ai in range(num_arrivals):
                for di in range(num_departures):
                    # Populate C3 Array
                    (c3s0[ai, di], c3s1[ai, di],
                    c3l0[ai,di], c3l1[ai,di],
                    dVs0[ai,di], dVs1[ai,di], 
                    dVl0[ai,di], dVl1[ai,di]) = cls.solveLambert(k, rP0[di], rP1[ai], vP0[di], vP1[ai], tofs[ai][di] * 86400)

            return rP0, vP0, rP1, vP1, c3s0, c3s1, c3l0, c3l1, dVs0, dVs1, dVl0, dVl1, tofs

        @classmethod
        def solveLambert(cls, k, rP0, rP1, vP0, vP1, tof):
            try:
                (vs0, vs1), = lambert(k * u.km**3 / u.s**2, rP0 * u.km, rP1 * u.km, tof * u.s, True)
                vs0 = vs0.value
                vs1 = vs1.value
                c3s0 = np.linalg.norm(vs0 - vP0)**2
                c3s1 = np.linalg.norm(vs1 - vP1)**2
                dVs0 = np.linalg.norm(vs0 - vP0) + np.sqrt(c3s0)
                dVs1 = np.linalg.norm(vs1 - vP1) + np.sqrt(c3s1)
                
            except:
                vs0 = np.array([0,0,0])
                vs1 = np.array([0,0,0])
                c3s0 = None
                c3s1 = None
                dVs0 = None
                dVs1 = None

            try:
                (vl0, vl1), = lambert(k * u.km**3 / u.s**2, rP0 * u.km, rP1 * u.km, tof * u.s, False)
                vl0 = vl0.value
                vl1 = vl1.value
                c3l0 = np.linalg.norm(vl0 - vP0)**2
                c3l1 = np.linalg.norm(vl1 - vP1)**2
                dVl0 = np.linalg.norm(vl0 - vP0) + np.sqrt(c3l0)
                dVl1 = np.linalg.norm(vl1 - vP1) + np.sqrt(c3l1)
                
            except:
                vl0 = np.array([0,0,0])
                vl1 = np.array([0,0,0])
                c3l0 = None
                c3l1 = None
                dVl0 = None
                dVl1 = None

            return c3s0, c3s1, c3l0, c3l1, dVs0, dVs1, dVl0, dVl1
    
    class Plot:
        @staticmethod
        @st.cache(suppress_st_warning=True)
        def porkchop(config, dd, ad, short, long, tof):

            layout = go.Layout(
            margin=go.layout.Margin(
                    l=10, #left margin
                    r=10, #right margin
                    b=10, #bottom margin
                    t=10,  #top margin
                    pad=10
                ),
            xaxis=dict(
                title="Launch Date",
                tickformat="%Y-%m-%d",
                gridcolor = "#eee"),
            yaxis=dict(
                title="Arrival Date",
                tickformat="%Y-%m-%d",
                gridcolor = "#eee"),
            plot_bgcolor= 'rgba(255,255,255,0)',
            paper_bgcolor= 'rgba(255,255,255,0)',
            # width=config["plt_size"][0], # width
            height=config["plt_size"][1], # height
            hovermode="x",
            hoverlabel=dict(
                bgcolor="black",
                font_color="white",
                ),
            )

            try:
                min_short = round(np.nanmin(short))
                min_long = round(np.nanmin(long))
            except ValueError:
                st.error("No solutions in date range")
                
            trace1 = go.Contour(
                    name="",
                    x = dd,
                    y = ad,
                    z = short,
                    hovertemplate='Type 1, '+ config['plt_type'] + ': %{z} ' + config['plt_u'],
                    showscale=False,
                    colorscale="oranges_r",
                    contours_coloring='lines',
                    line_width=1,
                    contours=dict(
                        start=min_short,
                        end=config["plt_ub"],
                        size=config["plt_i"],
                        showlabels = config["plt_lbl"],
                        labelfont = dict(
                            size = 10,
                            color = "black"
                        )))

            trace2 = go.Contour(
                    name="",
                    x = dd,
                    y = ad,
                    z = long,
                    hovertemplate='Type 2, '+ config['plt_type'] + ': %{z} ' + config['plt_u'],
                    showscale=False,
                    colorscale = "blues_r",
                    contours_coloring='lines',
                    line_width=1,
                    contours=dict(
                        start=min_long,
                        end=config["plt_ub"],
                        size=config["plt_i"],
                        showlabels = config["plt_lbl"],
                        labelfont = dict(
                            size = 10,
                            color = "black"
                        )))

            trace3 = go.Contour(
                    name="",
                    x = dd,
                    y = ad,
                    z = tof,
                    hovertemplate='%{x} >> %{y}: %{z} days',
                    showscale=False,
                    colorscale=[[0, 'grey'], [1.0, 'grey']],
                    contours_coloring='lines',
                    line_width=1,
                    contours=dict(
                        start=0,
                        end=tof.max(),
                        size=config["plt_tofi"],
                        showlabels=config["tof_lbl"],
                        labelfont=dict(
                            size=10,
                            color="black"
                        )))
            
            fig = go.Figure(data=[trace2, trace1, trace3], layout=layout)

            if not config["show_tof"]:
                fig.update_traces(
                    selector=2,
                    overwrite=True,
                    colorscale=[[0, 'rgba(0,0,0,0)'], [1.0, 'rgba(0,0,0,0)']]
                )

            return fig

        @staticmethod
        def pick_plot_type(plt_type, c3s0, c3s1, c3l0, c3l1, dVs0, dVs1, dVl0, dVl1):

            if plt_type == "Total C3":
                in_s = c3s0+c3s1
                in_l = c3l0+c3l1
            if plt_type == "Departure C3":
                in_s = c3s0
                in_l = c3l0
            if plt_type == "Arrival C3":
                in_s = c3s1
                in_l = c3l1
            if plt_type == "Total dV":
                in_s = dVs0+dVs1
                in_l = dVl0+dVl1
            if plt_type == "Departure dV":
                in_s = dVs0
                in_l = dVl0
            if plt_type == "Arrival dV": 
                in_s = dVs1
                in_l = dVl1

            return (in_s, in_l)
    
    class Date:

        @classmethod
        def getRange(cls, start, end, increment):
            # start, end: a date string ... ex: "2021-10-1"
            # increment: an int to create array of datetime objects with increment
            
            # Split the strings into a string arrays -> ex: ["2021", "10", "1"]
            start = start.split('-')
            end = end.split('-')

            # Convert string arrays into datetime objects:
            start_date = datetime.date(int(start[0]), int(start[1]), int(start[2]))
            end_date = datetime.date(int(end[0]), int(end[1]), int(end[2]))

            # Generate an array of dates:
            date_list = np.arange(start_date, end_date + datetime.timedelta(increment), increment)
            jdate_list = [cls.date2julian(date) for date in date_list]

            return date_list, jdate_list

        @staticmethod
        def date2julian(date):
            # date: a date string to be converted to a Julian Date
            
            # We convert the date into J2000, and sum the return of gcal2jd function call for final Julian date
            date = date.tolist()
            jdate = sum(jd.gcal2jd(date.year, date.month, date.day))
            return jdate