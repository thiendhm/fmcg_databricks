# import pandas as pd
# from dash import Dash, dcc, html
# import plotly.express as px
# import dash_bootstrap_components as dbc

# # Initialize the Dash app with Bootstrap styling
# dash_app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# chart_data = pd.DataFrame({'x': [x for x in range(30)],
#                            'y': [2 ** x for x in range(30)]})

# # Define the app layout
# dash_app.layout = dbc.Container([
#     dbc.Row([dbc.Col(html.H1('Hello world!!!'), width=12)]),
#     dcc.Graph(
#         id='fare-scatter',
#         figure=px.scatter(chart_data, x='x', y='y',
#             labels={'x': 'Apps', 'y': 'Fun with data'},
#             template='simple_white'),
#         style={'height': '500px', 'width': f'{min(100 + 50 * 30, 1000)}px'}
#     )
# ], fluid=True)

# Data Catalog app
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

# 1. Mock Data - Representing your Data Catalog
data = [
    {"name": "Sales Forecast 2024", "description": "Predictive model for regional sales performance.", "status": "Published", "type": "Dataset"},
    {"name": "Customer Churn", "description": "Raw data from CRM regarding user retention.", "status": "Published", "type": "Table"},
    {"name": "Inventory Levels", "description": "Real-time stock levels across warehouses.", "status": "Draft", "type": "API"},
    {"name": "Marketing ROI", "description": "Attribution model for Q3 digital campaigns.", "status": "Published", "type": "Dashboard"},
]
df = pd.DataFrame(data)

# 2. App Initialization (Using a Bootstrap theme)
dash_app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP])

# 3. Helper Function: Create a Card
def create_card(name, description, status):
    # Determine badge color based on status
    badge_color = "success" if status == "Published" else "secondary"
    
    return dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.H5(name, className="card-title mb-0"),
                                dbc.Badge(
                                    [html.I(className="bi bi-check-circle-fill me-1"), status],
                                    pill=True,
                                    color=badge_color,
                                    className="ms-2"
                                ),
                            ],
                            className="d-flex align-items-center mb-2"
                        ),
                        html.P(description, className="card-text text-muted small"),
                        dbc.Button("View Details", color="primary", size="sm", className="mt-auto"),
                    ],
                    className="d-flex flex-column"
                ),
            ],
            className="h-100 shadow-sm hover-shadow",
        ),
        xs=12, sm=6, md=4, lg=3, # Responsive column widths
        className="mb-4"
    )

# 4. App Layout
dash_app.layout = dbc.Container([
    # Header Section
    dbc.Row([
        dbc.Col([
            html.H1("Data Catalog", className="text-primary mt-4"),
            html.P("Search and manage organizational data assets.", className="text-muted mb-4"),
        ])
    ]),

    # Search Section
    dbc.Row([
        dbc.Col([
            dbc.InputGroup([
                dbc.InputGroupText(html.I(className="bi bi-search")),
                dbc.Input(
                    id="search-input",
                    placeholder="Search by name or description...",
                    type="text",
                    debounce=True # Triggers callback after user stops typing
                ),
            ], className="mb-4")
        ], width={"size": 8, "offset": 2})
    ]),

    # Results Gallery
    dbc.Row(id="card-gallery")
], fluid=True, className="px-5")

# 5. Interactivity Logic (Callback)
@dash_app.callback(
    Output("card-gallery", "children"),
    Input("search-input", "value")
)
def update_gallery(search_term):
    # Filter the DataFrame
    if not search_term:
        filtered_df = df
    else:
        search_term = search_term.lower()
        filtered_df = df[
            df['name'].str.lower().str.contains(search_term) |
            df['description'].str.lower().str.contains(search_term)
        ]
    
    # Handle empty results
    if filtered_df.empty:
        return dbc.Col(html.P("No assets found matching your search.", className="text-center text-muted mt-5"))

    # Map filtered data to Card components
    return [
        create_card(row['name'], row['description'], row['status']) 
        for _, row in filtered_df.iterrows()
    ]


if __name__ == '__main__':
    dash_app.run(debug=True)
