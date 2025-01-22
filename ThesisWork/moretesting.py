import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import sys

def ensure_streamlit_running():
    if not os.getenv("STREAMLIT_RUNNING"):
        os.environ["STREAMLIT_RUNNING"] = "true"
        command = f"streamlit run {sys.argv[0]}"
        os.system(command)
        sys.exit()
def main():
    ensure_streamlit_running()
    # Example data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

# Create two columns
    col1, col2 = st.columns(2)

# First graph in the first column
    with col1:
        st.write("Graph 1: Sine Wave")
        fig1, ax1 = plt.subplots()
        ax1.plot(x, y1, label="sin(x)", color="blue")
        ax1.set_title("Sine Wave")
        ax1.set_xlabel("X-axis")
        ax1.set_ylabel("Y-axis")
        ax1.legend()
        st.pyplot(fig1)

# Second graph in the second column
    with col2:
        st.write("Graph 2: Cosine Wave")
        fig2, ax2 = plt.subplots()
        ax2.plot(x, y2, label="cos(x)", color="red")
        ax2.set_title("Cosine Wave")
        ax2.set_xlabel("X-axis")
        ax2.set_ylabel("Y-axis")
        ax2.legend()
        st.pyplot(fig2)


if __name__ == "__main__":
    main()