import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import sys
import streamlit as st
import plotly.express as px
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import mpld3
import streamlit.components.v1 as components


def ensure_streamlit_running():
    if not os.getenv("STREAMLIT_RUNNING"):
        os.environ["STREAMLIT_RUNNING"] = "true"
        command = f"streamlit run {sys.argv[0]}"
        os.system(command)
        sys.exit()
def main():
    ensure_streamlit_running()
    
     # Create a simple DataFrame for testing
    data = {
        'X': [1, 2, 3, 4, 5],
        'Y': [2, 4, 6, 8, 10],
        'Label': ['A', 'B', 'C', 'D', 'E']
    }
    df = pd.DataFrame(data)

    # Create a scatter plot using Plotly
    fig = px.scatter(df, x='X', y='Y', text='Label', title="Interactive Scatter Plot with Plotly")
    
    # Show the interactive plot in Streamlit
    st.plotly_chart(fig)



if __name__ == "__main__":
    main()