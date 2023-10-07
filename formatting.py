def highlight_diff(val):
    color = 'white'
    if val < 0:
        color = 'lightcoral'  # Light red for negative values
    elif val > 0:
        color = 'lightgreen'  # Light green for positive values
    return f'background-color: {color}'