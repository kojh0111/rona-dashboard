import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from data import (
    countries_df,
    make_country_df,
    make_global_df,
    totals_df,
    dropdown_options,
)
from builders import make_table

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

bubble_map = px.scatter_geo(
    countries_df,
    color_continuous_scale="blues",
    size="Confirmed",
    hover_name="Country_Region",
    color="Confirmed",
    locations="Country_Region",
    locationmode="country names",
    projection="natural earth",
    size_max=40,
    template="plotly_dark",
    title="Confirmed By Country",
    hover_data={
        "Confirmed": ":,2f",
        "Deaths": ":,2f",
        "Recovered": ":,2f",
        "Country_Region": False,
    },
)

bars_graph = px.bar(
    totals_df,
    x="condition",
    hover_data={"count": ":,"},
    y="count",
    template="plotly_dark",
    title="Total Global Cases",
    labels={"condition": "Condition", "count": "Count", "color": "Condition"},
)

bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px"},
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(7, 1fr)",
            },
            children=[
                html.Div(
                    style={"grid-column": "span 5"},
                    children=[dcc.Graph(figure=bubble_map)],
                ),
                html.Div(
                    style={"grid-column": "span 2"}, children=[make_table(countries_df)]
                ),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(children=[dcc.Graph(figure=bars_graph)]),
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Dropdown(
                            placeholder="Choose Country",
                            id="country",
                            options=[
                                {"label": country, "value": country}
                                for country in dropdown_options
                            ],
                            style={
                                "width": 320,
                                "margin": "0 auto",
                                "color": "#111111",
                            },
                        ),
                        dcc.Graph(id="country_graph"),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(Output("country_graph", "figure"), [Input("country", "value")])
def update_hello(value):
    df = make_country_df(value) if value else make_global_df()
    fig = px.line(
        df,
        x="date",
        y=["confirmed", "deaths", "recovered"],
        template="plotly_dark",
        labels={"value": "Cases", "variable": "Condition", "date": "Date"},
        hover_data={"value": ":,", "variable": False, "date": False},
    )
    fig.update_xaxes(rangeslider_visible=True)
    fig["data"][0]["line"]["color"] = "#e74c3c"
    fig["data"][1]["line"]["color"] = "#8e44ad"
    fig["data"][2]["line"]["color"] = "#27ae60"
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
