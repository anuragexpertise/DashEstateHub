from dash import html, dcc

layout = html.Div([
    html.H2("Upload Accounts"),

    dcc.Upload(
        id='upload-accounts',
        children=html.Button("Upload Accounts Excel"),
        multiple=False
    ),

    html.Div(id='upload-status')
])