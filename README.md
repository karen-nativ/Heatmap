# Heatmap
Creates a visual heatmap from given data

----------------------
Prerequisites
----------------------
This tool requires the following libraries/modules installed:
* `mpl_toolkits.axes_grid1.inset_locator.InsetPosition`
* `matplotlib.pyplot` (Matplotlib Version >= 3.1)
* `matplotlib.widgets`
   * `Slider`
   * `RadioButtons`
* `collections.namedtuple`
* `math`

This tool requires the following files in the same folder:
* `create_heatmap.py`
* `heatmap_aux.py`
* `heatmap_config.py` - The variables in this file may be modified and will affect the heatmap appearance


----------------------
Usage
----------------------
To run the tool:
1. Import - 
`import create_heatmap as ch`
2. Call the `draw_heatmap` function -
`ch.draw_heatmap(dict_of_data)`


----------------------
Example
----------------------
```
import create_heatmap as ch
import random

X_labels = ["First_col", "Second_col", "Third_col"]
data = {"MY_REGISTER_" + str(num) : (random.randrange(1,10),random.randrange(1,10),random.randrange(1,10)) for num in range(1, 101)}
ch.draw_heatmap(X_labels, data)
```

---------------------
Output
----------------------
The tool creates an interactive heatmap of the given dictionary of data.

The terminal running the figure will wait for the figure to be closed before running additional commands.
