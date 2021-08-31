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
            
            # Initialize indexes:
            num_departures = len(jdd)
            num_arrivals = len(jad)

            # Initialize Data Arrays:
            c3s0 = np.zeros((num_arrivals, num_departures))
            c3l0 = np.zeros((num_arrivals, num_departures))
            vinfs1 = np.zeros((num_arrivals, num_departures))
            vinfl1 = np.zeros((num_arrivals, num_departures))
            dVs = np.zeros((num_arrivals, num_departures))
            dVl = np.zeros((num_arrivals, num_departures))

            # Initialize and populate time of flight:
            jdd_grid, jad_grid = np.meshgrid(jdd, jad)
            tofs = jad_grid - jdd_grid

            # Get departure and arrival body coordinates:
            rP0, vP0 = Body0.getCoords(jdd) # [km, km/s]
            rP1, vP1 = Body1.getCoords(jad) # [km, km/s]
            rP0 = rP0.transpose()
            rP1 = rP1.transpose()
            vP0 = vP0.transpose()
            vP1 = vP1.transpose()   

            # Populate data arrrays with lambert solutions:
            for ai in range(num_arrivals):
                for di in range(num_departures):
                    (c3s0[ai, di], c3l0[ai, di], vinfs1[ai, di],
                     vinfl1[ai, di], dVs[ai, di], dVl[ai, di]) = cls.solveLambert(k, rP0[di], rP1[ai], vP0[di], vP1[ai], tofs[ai][di] * 86400)

            return rP0, vP0, rP1, vP1, c3s0, c3l0, vinfs1, vinfl1, dVs, dVl, tofs

        @classmethod
        def solveLambert(cls, k, rP0, rP1, vP0, vP1, tof):
            try: # Short path calculations
                (vs0, vs1), = lambert(k * u.km**3 / u.s**2, rP0 * u.km, rP1 * u.km, tof * u.s, True)
                vs0 = vs0.value # strip units
                vs1 = vs1.value # strip units
                c3s0 = np.linalg.norm(vs0 - vP0)**2 # Short path departure excess energy
                vinfs1 = np.linalg.norm(vs1 - vP1) # Short path arrival surplus velocity
                dVs = abs(vinfs1) + np.sqrt(c3s0) # Short path total delta V requirement
                
            except: # If lambert solver returns no solutions, do not plot:
                c3s0 = None
                vinfs1 = None
                dVs = None

            try: # Long path calculations
                (vl0, vl1), = lambert(k * u.km**3 / u.s**2, rP0 * u.km, rP1 * u.km, tof * u.s, False)
                vl0 = vl0.value # strip units
                vl1 = vl1.value # strip units
                c3l0 = np.linalg.norm(vl0 - vP0)**2 # Long path departure excess energy
                vinfl1 = np.linalg.norm(vl1 - vP1) # Long path arrival surplus velocity
                dVl = abs(vinfl1) + np.sqrt(c3l0) # Long path total delta V requirement
                
            except: # If lambert solver returns no solutions, do not plot:
                c3l0 = None
                vinfl1 = None
                dVl = None
            return c3s0, c3l0, vinfs1, vinfl1, dVs, dVl
    
    class Plot:
        @staticmethod
        @st.cache(suppress_st_warning=True)
        def porkchop(config, dd, ad, c3s0, c3l0, vinfs1, vinfl1, dVs, dVl, tofs):

            # Plot formatting:
            layout = go.Layout(
            margin=go.layout.Margin(
                    l=10, #left margin
                    r=10, #right margin
                    b=10, #bottom margin
                    t=10,  #top margin
                    pad=10 # Plot padding
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
            height=config["plt_size"]["height"],
            hovermode="x",
            hoverlabel=dict(
                bgcolor="black",
                font_color="white",
                )
            )

            # Create Traces    

            c3_color = "red"
            vinf_color = "blue"
            dv_color = "green"

            c3s_trace = go.Contour(
                    name="C3 [km2/s2]",
                    x = dd,
                    y = ad,
                    z = c3s0,
                    hovertemplate='C3, Type 1: %{z} km2/s2<extra></extra>',
                    showscale=False,
                    showlegend=True,
                    colorscale=[[0, c3_color], [1.0, c3_color]],
                    contours_coloring='lines',
                    line_width=1,
                    contours=dict(
                        start=0,
                        end=config["c3_ub"],
                        size=config["inc"],
                        showlabels = config["c3_lbl"],
                        labelfont = dict(
                            size = 10,
                            color = c3_color
                        )))

            c3l_trace = go.Contour(
                    name="C3 [km2/s2]",
                    x = dd,
                    y = ad,
                    z = c3l0,
                    hovertemplate='C3, Type 2: %{z} km2/s2<extra></extra>',
                    showscale=False,
                    colorscale = [[0, c3_color], [1.0, c3_color]],
                    contours_coloring='lines',
                    line_width=1,
                    contours=dict(
                        start=0,
                        end=config["c3_ub"],
                        size=config["inc"],
                        showlabels = config["c3_lbl"],
                        labelfont = dict(
                            size = 10,
                            color = c3_color
                        )))

            vinfs_trace = go.Contour(
                    name="V Infinity [km/s]",
                    x = dd,
                    y = ad,
                    z = vinfs1,
                    hovertemplate='V Infinity, Type 1: %{z} km/s<extra></extra>',
                    showscale=False,
                    showlegend=True,
                    colorscale=[[0, vinf_color], [1.0, vinf_color]],
                    contours_coloring='lines',
                    line_width=1,
                    contours=dict(
                        start=0,
                        end=config["vinf_ub"],
                        size=config["inc"],
                        showlabels=config["vinf_lbl"],
                        labelfont=dict(
                            size=10,
                            color=vinf_color
                        )))

            vinfl_trace = go.Contour(
                    name="V Infinity [km/s]",
                    x = dd,
                    y = ad,
                    z = vinfl1,
                    hovertemplate='V Infinty, Type 2: %{z} km/s<extra></extra>',
                    showscale=False,
                    colorscale=[[0, vinf_color], [1.0, vinf_color]],
                    contours_coloring='lines',
                    line_width=1,
                    contours=dict(
                        start=0,
                        end=config["vinf_ub"],
                        size=config["inc"],
                        showlabels=config["vinf_lbl"],
                        labelfont=dict(
                            size=10,
                            color=vinf_color
                        )))

            dVs_trace = go.Contour(
                    name="Delta V [km/s]",
                    x = dd,
                    y = ad,
                    z = dVs,
                    hovertemplate='Delta V, Type 1: %{z} km/s<extra></extra>',
                    showscale=False,
                    showlegend=True,
                    colorscale=[[0, dv_color], [1.0, dv_color]],
                    contours_coloring='lines',
                    line_width=1,
                    contours=dict(
                        start=0,
                        end=config["dv_ub"],
                        size=config["inc"],
                        showlabels=config["dv_lbl"],
                        labelfont=dict(
                            size=10,
                            color=dv_color
                        )))

            dVl_trace = go.Contour(
                    name="Delta V [km/s]",
                    x = dd,
                    y = ad,
                    z = dVl,
                    hovertemplate='Delta V, Type 2: %{z} km/s<extra></extra>',
                    showscale=False,
                    colorscale=[[0, dv_color], [1.0, dv_color]],
                    contours_coloring='lines',
                    line_width=1,
                    contours=dict(
                        start=0,
                        end=config["dv_ub"],
                        size=config["inc"],
                        showlabels=config["dv_lbl"],
                        labelfont=dict(
                            size=10,
                            color=dv_color
                        )))

            tof_trace = go.Contour(
                    name="TOF [s]",
                    x = dd,
                    y = ad,
                    z = tofs,
                    hovertemplate='%{x} >> %{y}: %{z} days<extra></extra>',
                    showscale=False,
                    showlegend=True,
                    colorscale=[[0, 'black'], [1.0, 'black']],
                    contours_coloring='lines',
                    line_width=1,
                    contours=dict(
                        start=0,
                        end=tofs.max(),
                        size=config["tof_inc"],
                        showlabels=config["tof_lbl"],
                        labelfont=dict(
                            size=10,
                            color="black"
                        )))
            
            # Prepare Traces:
            plottable_traces = []
            if config["make_plt"]["dv"]:
                plottable_traces.append(dVl_trace)
                plottable_traces.append(dVs_trace)
            if config["make_plt"]["vinf"]:
                plottable_traces.append(vinfl_trace)
                plottable_traces.append(vinfs_trace)
            if config["make_plt"]["c3"]:
                plottable_traces.append(c3l_trace)
                plottable_traces.append(c3s_trace)
            plottable_traces.append(tof_trace)

            # Plot Traces:
            fig = go.Figure(data=plottable_traces, layout=layout)

            if not config["make_plt"]["tof"]:
                fig.update_traces(
                    selector=len(plottable_traces)-1,
                    overwrite=True,
                    colorscale=[[0, 'rgba(0,0,0,0)'], [1.0, 'rgba(0,0,0,0)']],
                    name=""
                )

            return fig
    
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