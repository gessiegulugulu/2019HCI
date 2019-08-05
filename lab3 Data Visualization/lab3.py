"""
The dataset here is a sample of the transactions made in a retail store.
The store wants to know better the customer purchase behavior against different products.
Specifically, here the problem is a regression problem where we are trying to predict
 the dependent variable (the amount of purchase) with the help of the information contained in the other variables.
Classification problem can also be settled in this dataset since several variables are categorical,
 and some other approaches could be "Predicting the age of the consumer" or even "Predict the category of goods bought".
This dataset is also particularly convenient for clustering and maybe find different clusters of consumers within it.

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors={
    'background':'#f2f2f2',
    'text':'##635c65'
}#color type

df_Region = pd.read_csv('salaries-by-region.csv')
df_College = pd.read_csv('salaries-by-college-type.csv')
df_Degree = pd.read_csv('degrees-that-pay-back.csv')
available_SchoolType = df_College['School Type'].unique()

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis',
                options=[
                    {'label': 'Starting Median Salary', 'value': 'Starting Median Salary'},
                    {'label': 'Mid-Career Median Salary', 'value': 'Mid-Career Median Salary'},
                    {'label': 'Mid-Career 10th Percentile Salary', 'value': 'Mid-Career 10th Percentile Salary'},
                    {'label': 'Mid-Career 25th Percentile Salary', 'value': 'Mid-Career 25th Percentile Salary'},
                    {'label': 'Mid-Career 75th Percentile Salary', 'value': 'Mid-Career 75th Percentile Salary'},
                    {'label': 'Mid-Career 90th Percentile Salary', 'value': 'Mid-Career 90th Percentile Salary'}
                ],
                value='Starting Median Salary'
            )
        ],
        style={'width': '33%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis',
                options=[
                    {'label': 'Starting Median Salary', 'value': 'Starting Median Salary'},
                    {'label': 'Mid-Career Median Salary', 'value': 'Mid-Career Median Salary'},
                    {'label': 'Mid-Career 10th Percentile Salary', 'value': 'Mid-Career 10th Percentile Salary'},
                    {'label': 'Mid-Career 25th Percentile Salary', 'value': 'Mid-Career 25th Percentile Salary'},
                    {'label': 'Mid-Career 75th Percentile Salary', 'value': 'Mid-Career 75th Percentile Salary'},
                    {'label': 'Mid-Career 90th Percentile Salary', 'value': 'Mid-Career 90th Percentile Salary'}
                ],
                value='Mid-Career Median Salary'
            )
        ],
            style={'width': '33%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='SchoolType',
                options=[{'label':i,'value':i} for i in available_SchoolType],
                value='Engineering'
            ),
        ],
        style={'width': '33%', 'display': 'inline-block'})
    ],
        style={
        'borderBottom': colors['text'],
        'backgroundColor': colors['background'],
        'padding': '10px 5px'
    }),

    html.Div(
        [dcc.Graph(id='scatter')],
        style={
            'width': '49%',
            'display': 'inline-block',
            'backgroundcolor':colors['background'],
            'text':colors['text']
        }),
    html.Div([dcc.Graph(id='bar'),dcc.Graph(id='Line')],
        style={
            'display': 'inline-block',
            'width': '49%',
            'backgroundcolor':colors['background'],
            'text':colors['text']})
])

@app.callback(
    dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('xaxis', 'value'),
     dash.dependencies.Input('yaxis', 'value')
     ])
def graph_scatter(xx,yy):
    temp='Region'
    print(xx,yy,temp)
    return {
        'data': [go.Scatter(
            x=df_Region[df_Region[temp]==i][xx],
            y=df_Region[df_Region[temp]==i][yy],
            text=df_Region[df_Region[temp]==i]['School Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i)
            for i in df_Region[temp].unique()
        ],
        'layout': go.Layout(
            xaxis={'title': xx},
            yaxis={ 'title': yy},
            height=800,
            title='Salaries by Region',
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('Line','figure'),
    [
        dash.dependencies.Input('xaxis','value'),
        dash.dependencies.Input('yaxis','value')
    ]
)

def graph_Line(xaxis,yaxis):
    return{
        'data':[go.Scatter(
            x=df_Degree['Undergraduate Major'],
            y=df_Degree['Percent change from Starting to Mid-Career Salary'],
            mode='lines+markers'
        )],
        'layout':go.Layout(
            height=380,
            title= 'Percent change from Starting to Mid-Career Salary'
        )

    }

@app.callback(
    dash.dependencies.Output('bar', 'figure'),
    [
        dash.dependencies.Input('SchoolType', 'value'),
        dash.dependencies.Input('xaxis', 'value'),
        dash.dependencies.Input('yaxis', 'value')
    ]
)
def graph_bar(t,xx,yy):
    #for i in available_SchoolType:
     #   print(i+'@//')
    return {
        'data': [
            go.Bar(
                x=df_College['School Name'],
                y=df_College[df_College['School Type']==t][xx],
                name=xx
            ),
            go.Bar(
                x=df_College['School Name'],
                y=df_College[df_College['School Type'] == t][yy],
                name=yy
            )
        ],
        'layout': go.Layout(
            title='Salaries by College Type',
            barmode='group',
          #  height=400
        )
    }



if __name__ == '__main__':
    app.run_server()