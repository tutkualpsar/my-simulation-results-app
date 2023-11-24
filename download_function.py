import streamlit as st
import pandas as pd
import base64

def download_button(df, button_text, file_name):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Convert dataframe to bytes
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}.csv">{button_text}</a>'
    return href