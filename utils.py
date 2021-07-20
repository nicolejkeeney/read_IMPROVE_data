"""utils.py 

Helper functions for IMPROVE notebooks 

Author: Nicole Keeney 
Date Created: 05-28-2021 
Modification History: n/a

"""

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats


def create_df_from_txt(txt_tbl): 
    """ Remove annoying whitespaces from row of data, then format as a pandas DataFrame object 
    
        Args: 
            txt_tbl(np array): unformatted array with whitespaces separating each element, and each row representing a different row in the table 
            
        Returns: 
            df (pd.DataFrame): txt_tbl reformatted all nice, with the first row set to the column names 
    """
    
    # Separate each element in the line into its own element
    # The text file is super annoying to work with. Each string is split by a seemingly random number of whitespaces 
    lines_splt = []
    for line in txt_tbl: 
        split_whitespaces = [s.strip() for s in line.split('  ') if s]
        lines_splt.append(split_whitespaces)

    # Create a dataframe
    df = pd.DataFrame(lines_splt)
    df.columns = df.iloc[0] # Set first row to column names
    df = df.drop(0).reset_index(drop = True) 
    df.drop(df.columns[-1],axis=1,inplace=True) # Drop weird empty column 
    return df 


def plot_iron_proxy(df, figsize = (7,5), title = "All CA"): 
    """ Plot iron vs. fine soil with a regression line with equation 
    Ensure that the index of df is a time series

    Args: 
        df (pd.DataFrame): dataframe object containing the variables [time_col, y_col1, y_col2]
        figsize (tuple, optional): size of figure (default to (7,5))
        title (str, optional): title to give plot (default to "IMPROVE Iron vs. Soil")
        
    Returns: 
        Figure displayed in axis
    
    """

    # Set up plot 
    fig, ax = plt.subplots(figsize = figsize)

    # Plot regression line
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html
    x_vals = df["Iron"]
    y_vals = df["Soil"]
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x = x_vals, y = y_vals)
    reg_line = intercept + slope*x_vals
    reg_plot = ax.plot(x_vals, reg_line, linestyle = '-', color = 'red', zorder = 5)
    reg_line_str = "y = " + str(round(slope, 2)) + "x + " + str(round(intercept,2)) 

    # Add text description
    reg_line_txt = ax.text(x = 0.04, y = 0.93, s = reg_line_str, fontsize = 13, transform = ax.transAxes)
    r_squared_txt = ax.text(x = 0.04, y = 0.85, s = 'r = ' + str(round(r_value,2)), fontsize = 13, transform = ax.transAxes)


    # Plot data
    data_scattered = df.plot.scatter(x = "Iron", y = "Soil", ax = ax, marker = 'x', color = 'black', zorder = 10)

    # Make plot pretty
    plt.title(title)
    plt.show()      