import plotly.plotly as py
import plotly.graph_objs as go

# trace1 = go.Scatter(
#     x=[1, 2, 3, 4, 5, 
#        6, 7, 8, 9, 10,
#        11, 12, 13, 14, 15],
#     y=[10, 20, None, 15, 10,
#        5, 15, None, 20, 10,
#        10, 15, 25, 20, 10],
#     name = '<b>No</b> Gaps', # Style name/legend entry with html tags
#     connectgaps=True
# )
trace1 = go.Scatter(
    y=[0.777777777778,0.8,0.866666666667,0.833333333333,0.791666666667,0.833333333333,0.861111111111,0.836363636364],
    x=[16,20,30,35,47,61,71,109],
    name = '<b>No</b> Gaps', # Style name/legend entry with html tags
    connectgaps=True
)


# trace2 = go.Scatter(
#     y=[0.823, 0.677,0.75,0.79],
#     x=[25,30,40,45],
#     name = 'Gaps'
# )


# trace2 = go.Scatter(
#     x=[1, 2, 3, 4, 5,
#        6, 7, 8, 9, 10,
#        11, 12, 13, 14, 15],
#     y=[5, 15, None, 10, 5,
#        0, 10, None, 15, 5,
#        5, 10, 20, 15, 5],
#     name = 'Gaps',
# )

data = [trace1]

fig = dict(data=data)
py.iplot(fig, filename='precision')
