import pandas as pd
import bokeh

from bokeh.io import output_file, show
from bokeh.models import BasicTicker, ColorBar, ColumnDataSource, LinearColorMapper, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.transform import transform

data = pd.read_csv("data.csv")

data.t_sec = data.t_sec.astype(str)

data = data.set_index('t_sec')

data.columns.name = 'subject id'

# reshape to 1D array - "mode of fixations" for a time period and subject for each row.
df = pd.DataFrame(data.stack(), columns=['mode_fixation']).reset_index()

df.head(10)

source = ColumnDataSource(df)

df.info


# set colours 
colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878"]
mapper = LinearColorMapper(palette=colors, low=df.mode_fixation.min(), high=df.mode_fixation.max())

#set up figure
p = figure(plot_width=800, plot_height=300, title="Area of Focus in 10s Units",
           x_range=list(data.index), y_range=list(reversed(data.columns)),
           toolbar_location=None, tools="", x_axis_location="below", x_axis_label="Time (s)", 
           y_axis_label="Subject ID")

p.rect(x="t_sec", y="subject id", width=1, height=1, source=source,
       line_color=None, fill_color=transform('mode_fixation', mapper))

color_bar = ColorBar(color_mapper=mapper, location=(0, 0),
                     ticker=BasicTicker(desired_num_ticks=len(colors)),
                     formatter=PrintfTickFormatter(format= "%d"))

p.add_layout(color_bar, 'right')

p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "5pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = 1.0

show(p)
