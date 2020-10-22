"""Heatmap Creator

This code creates a heatmap from a dictionary of data it recieves.
It includes an addition as part of the Register Access Heatmap tool.

This tool requires the following Python libraries be installed:
* mpl_toolkits.axes_grid1.inset_locator.InsetPosition
* matplotlib.pyplot (Matplotlib Version >= 3.1)
* matplotlib.widgets
   * Slider
   * RadioButtons
* collections.namedtuple
* packaging.version
* math

This tool requires the following files in the same folder:
    * heatmap_aux.py
    * heatmap_config.py - The variables in this file may be modified and will affect the heatmap appearance

This file contains the following functions:
* draw_heatmap - Creates a heatmap from a dictionary of data
* heatmap_from_reg_use - Creates a heatmap from reg_use data created as part of the Register Access Heatmap tool
"""

import heatmap_aux as aux
from heatmap_config import *
import matplotlib.pyplot as plt
from matplotlib import __version__ as mpl_version
from packaging import version

### CONSTS ####
MATPLOTLIB_VERSION = "3.1"
##############


class reg_use:
    """ The class that corresponds with the reg_use struct in the e file
    Class attributes:
    name - The register name
    read_count - The amount of read accesses
    write_count - The amount of write accesses
    """
    def get_name(self):
        """ Returns the name attribute of the reg_use """
        return self.name
    
    def get_read_count(self):
        """ Returns the read-count attribute of the reg_use """
        return self.read_count
    
    def get_write_count(self):
        """ Returns the write-count attribute of the reg_use """
        return self.write_count

def heatmap_from_reg_use(reg_uses):
    """Creates a dictionary of tuples from a list of reg_use
    Note - This function is called from E code.
    
    Parameters
    ----------
    reg_uses : a list of reg_use objects
        Represents the registers and the amount they have been accessed
    """
    reg_dict = {reg.get_name() : (reg.get_read_count(), reg.get_write_count()) for reg in reg_uses}
    draw_heatmap(['Read', 'Write'], reg_dict)
    

def draw_heatmap(X_labels, data_dict):
    """Creates a heatmap figure of the given dictionary data
    The X axis values are constants that are given
    
    Parameters
    ----------
    X_labels : list of strings
        Contains the labels that will be on the X axis of the heatmap
    data_dict : dict of tuples, where the key is the name and the data is the values
        Represents the rows of data to be displayed
        The amount of items in every tuple must be identical to the amount of X_labels, otherwise behavior is undefined
    """
    if version.parse(mpl_version) < version.parse(MATPLOTLIB_VERSION):
        print("\n *** Error: To create the heatmap, matplotlib version", MATPLOTLIB_VERSION, "is needed.")
        print("Current matplotlib version:", version.parse(mpl_version),"\n")
        return
    data_names = data_dict.keys()
    if len(data_names) == 0:
        print(">>>No information to display")
        return

    fig, ax = plt.subplots()
    display_amount = min(len(data_names), PAGE_DISPLAY_AMOUNT)
    try:
        all_vals = [item for sublist in data_dict.values() for item in sublist]
    except:
        print("Expected format of data_dict parameter is a dictionary of string keys and tuple values")
        return

    
    img = ax.imshow([[min(all_vals)], [max(all_vals)]], aspect='auto', cmap=HEATMAP_COLORS, interpolation='bilinear', origin='upper', extent=[0, 2*len(X_labels), 2*display_amount, 0]) # First param is dummy data before it is updated

    aux.create_x_labels(ax, X_labels)
    aux.update_scroll(0, img, ax, list(data_dict.values()), list(data_names), display_amount)
    
    fig.colorbar(img)
    img.set_clim(vmin=0)
    
    aux.value_on_hover(ax, img)

    radio = aux.create_radio_buttons(ax)
    def radio_func(label):
        current_interpolation = aux.INTERPOLATION_DICT[label]
        img.set_interpolation(current_interpolation)
        plt.draw()

    radio.on_clicked(radio_func)
    
    if len(data_names) > PAGE_DISPLAY_AMOUNT:
        aux.create_scrollbar(fig, img, ax, data_names, list(data_dict.values()))
    
    plt.show()

     

if __name__ == "__main__":
    print("This file is intended to be imported")
