import streamlit as st

class Initialize():
    @staticmethod
    def config():
        st.set_page_config(
            page_title="Mission Planner",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.sidebar.title("Transfer Parameters")

        show_c3 = st.sidebar.checkbox("Plot Departure C3", value=True)
        show_vinf = st.sidebar.checkbox("Plot Arrival V Infinity", value=True)
        show_dv = st.sidebar.checkbox("Plot Total Delta V", value=False)
        show_tof = st.sidebar.checkbox("Plot Time of Flight (TOF)", value=False)

        bodies_select = st.sidebar.expander(label='Flight Settings')
        with bodies_select:
            departure_body = st.selectbox(
                "Departure Body",
                (
                    "Mercury", "Venus", "Earth", "Mars", 
                    "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"
                ),
                index=2
            )

            arrival_body = st.selectbox(
                "Arrival Body",
                (
                    "Mercury", "Venus", "Earth", "Mars", 
                    "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"
                ),
                index=3
            )
            dep_cols = st.columns(2)
            departure0 = dep_cols[0].text_input('Earliest Departure', '2022-07-01')
            departure1 = dep_cols[1].text_input('Latest Departure', '2022-11-01')
            arr_cols = st.columns(2)
            arrival0 = arr_cols[0].text_input('Earliest Arrival', '2023-01-01')
            arrival1 = arr_cols[1].text_input('Latest Arrival', '2024-01-01')
            d_inc = st.text_input("Calculation Increment (days)", '2')

        plot_settings = st.sidebar.expander(label="Plot Settings")
        with plot_settings:
            st.write("Plot Labels")
            lbl_cols1 = st.columns(2)
            lbl_cols2 = st.columns(2)
            c3_lbl = lbl_cols1[0].checkbox("C3", value=True)
            vinf_lbl = lbl_cols1[1].checkbox("V Infinity", value=True)
            dv_lbl = lbl_cols2[0].checkbox("Delta V", value=True)
            tof_lbl = lbl_cols2[1].checkbox("TOF", value=True)
            
            st.write("Contour Upper Bounds")
            ctr_cols = st.columns(3)
            c3_ub = ctr_cols[0].text_input('C3', 40)
            vinf_ub = ctr_cols[1].text_input('V Infinity', 15)
            dv_ub = ctr_cols[2].text_input('Delta V', 20)

            st.write("Plot Increments")
            plt_cols = st.columns(3)
            inc = plt_cols[0].text_input('Contours', 1)
            tof_inc = plt_cols[1].text_input('TOF Lines', 50)
        
        config = {
            # Flight Settings:
            "db"       : departure_body, # Departure Body
            "ab"       : arrival_body, # Arrival Body
            "k"        : 1.32712440018e11, # Gravitational parameter of main attractor (heliocentric) [km^3/s^2]
            "dd"       : [departure0, departure1], # Departure Dates Array
            "ad"       : [arrival0, arrival1], # Arrival Dates Array
            "d_inc"    : int(d_inc), # Date Increment (ie: for a given date range, d_inc = 1 calculates a transfer every day, d_inc = 2 calculates a transfer every two days and so on)

            # Plot Settings:
            "c3_ub"    : int(c3_ub), # plot upper bound for displaying c3 contour lines
            "vinf_ub"  : int(vinf_ub), # plot upper bound for displaying vinf contour lines
            "dv_ub"    : int(dv_ub), # plot upper bound for displaying dv contour lines

            "c3_lbl"   : c3_lbl, # Display c3 Labels
            "vinf_lbl" : vinf_lbl, # Display vinf Labels
            "dv_lbl"   : dv_lbl, # Display dv Labels
            "tof_lbl"  : tof_lbl, # Display tof Labels
            "inc"      : int(inc),  # Increment between contour lines
            "tof_inc"  : int(tof_inc), # Increment between lines of constant flight time

            "plt_size" : {"width" : 800, "height" : 550}, # Size of the Porkhop Plot (width (index = 0) currently unused)
            "make_plt" : {"c3": show_c3, "vinf" : show_vinf, "dv" : show_dv, "tof" : show_tof} # Check which plots to make, type: [bool, bool, bool, bool]
        }

        # Label Setup:
        if not config["make_plt"]["c3"]:
            config["c3_lbl"] = False
        if not config["make_plt"]["vinf"]:
            config["vinf_lbl"] = False
        if not config["make_plt"]["dv"]:
            config["dv_lbl"] = False
        if not config["make_plt"]["tof"]:
            config["tof_lbl"] = False
        
        # Remove excess HTML:

        st.markdown(f""" <style>
            .reportview-container .main .block-container{{
                padding-top: {0}rem;
                padding-bottom: {0}rem;
                }} 
            </style> """, unsafe_allow_html=True)

        hide_streamlit_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

        return config