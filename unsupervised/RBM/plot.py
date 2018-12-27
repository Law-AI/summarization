import plotly.plotly as py
import plotly.graph_objs as go

trace1 = go.Scatter(
    x=[1, 2, 3, 4, 5, 
       6, 7, 8, 9, 10,
       11, 12, 13, 14, 15],
    y=[10, 20, None, 15, 10,
       5, 15, None, 20, 10,
       10, 15, 25, 20, 10],
    name = '<b>No</b> Gaps', # Style name/legend entry with html tags
    connectgaps=True
)
trace2 = go.Scatter(
    x=[1, 2, 3, 4, 5,
       6, 7, 8, 9, 10,
       11, 12, 13, 14, 15],
    y=[5, 15, None, 10, 5,
       0, 10, None, 15, 5,
       5, 10, 20, 15, 5],
    name = 'Gaps',
)

data = [trace1, trace2]

fig = dict(data=data)
py.iplot(fig, filename='simple-connectgaps')
