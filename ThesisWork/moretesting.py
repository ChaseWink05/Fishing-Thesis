import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import sys
import streamlit as st
import plotly.express as px
import pandas as pd


def ensure_streamlit_running():
    if not os.getenv("STREAMLIT_RUNNING"):
        os.environ["STREAMLIT_RUNNING"] = "true"
        command = f"streamlit run {sys.argv[0]}"
        os.system(command)
        sys.exit()
def main():
    ensure_streamlit_running()
    
    # Sample data for demonstration
    data = pd.DataFrame({
        'x': range(1, 101),
        'y': [i**2 for i in range(1, 101)]
    })

    # Create a Plotly figure (interactive by default)
    fig = px.line(data, x='x', y='y', title='Zoomable Chart')

    # Display the Plotly figure in Streamlit
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()