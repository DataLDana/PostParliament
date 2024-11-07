import pandas as pd
import matplotlib as plt
import seaborn as sns
import streamlit as st

def make_pie_2(df,col,titles):

    # Plotting the pie chart
    sns.set_theme(style="whitegrid")
    
    # Create a figure with two side-by-side subplots
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # (1, 2) for 1 row, 2 columns
    
    # Function to format pie chart labels
    def label_formatter(pct, values):
        absolute = int(round(pct/100. * sum(values)))  # Calculate absolute count
        return f"{pct:.1f}%\n({absolute})"             # Return as percentage and count
        
    # First Pie Chart
    axes[0].pie(df[col[0]], labels=list(df.index), autopct='%1.1f%%')
    axes[0].set_title(titles[0])
    
    # Second Pie Chart - Example with another column or different data
    # Replace 'another_column' with the appropriate column from your DataFrame
    axes[1].pie(df[col[1]], labels=list(df.index),autopct='%1.1f%%')
    axes[1].set_title(titles[1])
    
    # Display the plots
    plt.tight_layout()  # Adjust spacing to prevent overlap
    st.pyplot(fig)

# ******************************
# change datatypes of posts dataframes 
def change_types(df):
    df['name'] = df['name'].astype('category')
    df['date'] = pd.to_datetime(df['date'])
    df['likes'] = df['likes'].astype('int32')
    df['comments'] = df['comments'].astype('uint16')
    df['video_views'] = df['video_views'].fillna(0)
    df['video_views'] = df['video_views'].astype('uint32')
    
    return df

# ********************************
def wrap_text(text):
    width = 40
    if isinstance(text,str):  # check if text is string
        return '\n'.join([text[i:i+width] for i in range(0, len(text), width)])
    else:
        return text
