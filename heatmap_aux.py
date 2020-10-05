"""Heatmap Auxiliary Functions

These functions are not public, they are for inner use of the Heatmap tool.
This file is required to be in the same folder as:
    create_heatmap.py
    heatmap_config.py
"""

from heatmap_config import *
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
from matplotlib.widgets import Slider, RadioButtons
from collections import namedtuple
import matplotlib.pyplot as plt
import math


INTERPOLATION_DICT = {'Gradient': 'bilinear', 'Sharp': 'none'}


def create_x_labels(ax, X_labels):
    ax.set_xlim([0, 2*len(X_labels)])
    ax.set_xticks(range(1, 2*len(X_labels), 2))
    ax.set_xticklabels(X_labels, fontsize=FONTSIZE)
    

def value_on_hover(ax, img):
    _Event = namedtuple('_Event', 'xdata ydata')
    ax.format_coord = lambda x, y : 'Value = ' + str(img.get_cursor_data(_Event(x, y)))
    img.format_cursor_data = lambda val : ''    
    
def create_radio_buttons(ax):
    radio_ax = plt.axes([0, 0, 1, 1], facecolor=RADIO_BUTTON_BG_COLOR) #[posx, posy, width, height]
    radio_pos = InsetPosition(ax, [0, 1.02, 0.3, 0.14])
    radio_ax.set_axes_locator(radio_pos)
    radio = RadioButtons(radio_ax, INTERPOLATION_DICT.keys())
    return radio


def create_scrollbar(fig, img, ax, data_names, data_values):
    axpos = plt.axes([0.95, 0.01, 0.03, 0.9], facecolor='darkgrey')
    max_val = 2*(len(data_names) - PAGE_DISPLAY_AMOUNT)
    spos = Slider(axpos, 'Scroll', 0, max_val, valinit=2*(len(data_names) - PAGE_DISPLAY_AMOUNT), valstep=2, orientation='vertical', color='lightgrey')
    spos.valtext.set_visible(False)
    
    def update(val): # val is always a positive even integer
        update_scroll(int(max_val-val), img, ax, data_values, list(data_names)) #The slider is backwards so reverse val
        plt.draw()

    spos.on_changed(update)
    
    def mouse_scroll(event):
        new_val = spos.val + event.step
        if new_val > max_val:
            new_val = max_val
        if new_val < 0:
            new_val = 0
        spos.set_val(new_val)
            
    fig.canvas.mpl_connect('scroll_event', mouse_scroll)


def update_scroll(val, img, ax, graph_data, data_names, display_amount=PAGE_DISPLAY_AMOUNT):
    data_index = int(val / 2)
    current_display_data = graph_data[data_index:data_index + display_amount]
    current_display_data.reverse() # Reversed to show the original list first values at the top of the heatmap
    img.set_data(current_display_data) 
    left, right, bottom, top = img.get_extent()
    img.set_extent([left, right, val, val + 2*display_amount])
    
    ax.set_ylim([val + 2*display_amount, val])
    y_label_list = data_names[int(val/2):int(val/2) + display_amount]
    ax.set_yticks(range(val + 1, val + 2*display_amount, 2))
    ax.set_yticklabels(y_label_list)
    plt.tight_layout(rect=[0,0,1,0.9])