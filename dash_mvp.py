import dash
import dash_table
import pandas as pd
import dash_core_components as dcc

df = pd.read_csv('full_dataframe.csv', nrows=50)

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    filter_action='native',
    style_table={
        'height': 400,
    },
    style_data={
    'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
    'overflow': 'hidden',
    'textOverflow': 'ellipsis',
    }
    
    )




if __name__ == '__main__':
    app.run_server()