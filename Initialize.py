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

        plt_type = st.sidebar.selectbox(
            "Plot Type",
            (
                "Total C3", "Departure C3", "Arrival C3",
                "Total dV", "Departure dV", "Arrival dV"
            )
        )

        bodies_select = st.sidebar.expander(label='Departure and Arrival settings')
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

            departure0 = st.text_input('Earliest Departure (YYYY-MM-DD)', '2022-07-01')
            departure1 = st.text_input('Latest Departure (YYYY-MM-DD)', '2022-11-01')
            arrival0 = st.text_input('Earliest Arrival (YYYY-MM-DD)', '2023-01-01')
            arrival1 = st.text_input('Latest Arrival (YYYY-MM-DD)', '2024-01-01')
            dinc = st.text_input("Increment (Default 2)", '2')

        plot_settings = st.sidebar.expander(label="Plot Settings")
        with plot_settings:
            # plt_lb = st.text_input('Lower Bound: Contour', '0')
            plt_ub = st.text_input('Contour Upper Bound', '50')
            plt_i = st.text_input('Contour Increment', '1')
            plt_lbl = st.checkbox("Contour Labels", value=True)
            plt_tofi = st.text_input('TOF Increment', 50)
            show_tof = st.checkbox("TOF Lines", value=False)
            tof_lbl = st.checkbox("TOF Labels", value=False)

        if (plt_type == "Total C3" or plt_type == "Arrival C3" or plt_type == "Departure C3"):
            plt_units = "[km3/s2]"
        else:
            plt_units = "[km/s]"
            
        config = {
            "db"       : departure_body, # Departure Body
            "ab"       : arrival_body, # Arrival Body
            "k"        : 1.32712440018e11, # Gravitational parameter of main attractor (heliocentric) [km^3/s^2]
            "dd"       : [departure0, departure1], # Departure Dates Array
            "ad"       : [arrival0, arrival1], # Arrival Dates Array
            "dinc"     : int(dinc), # Date Increment
            # "plt_lb"   : int(plt_lb), # plot lower bound for displaying contour lines
            "plt_ub"   : int(plt_ub), # plot upper bound for displaying contour lines
            "plt_i"    : int(plt_i),  # plot increment between 
            "plt_u"    : plt_units, # Plot units to be displayed
            "plt_type" : plt_type, # Name of Plot
            "plt_tofi" : int(plt_tofi), # Increment between lines of constant flight time
            "plt_lbl"  : bool(plt_lbl), # Display Labels
            "tof_lbl"  : bool(tof_lbl), # Display Time of Flight Labels
            "plt_size" : [800,550], # Size of the Porkchop Plot (width (index = 0) currently unused)
            "show_tof" : show_tof
        }
        
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