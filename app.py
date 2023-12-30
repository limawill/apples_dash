import pandas as pd
import plotly.express as px
import numpy as np
from dash import Dash, Input, Output, dcc, html

data = pd.read_csv('macas_Brasil.csv')

regions = data["Região"].sort_values().unique()
tipo_macas = data["Tipo"].sort_values().unique()
ano = data["Ano"].sort_values().unique()

regions = np.concatenate(([""], regions))
tipo_macas = np.concatenate(([""], tipo_macas))
ano = np.concatenate(([""], ano))

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Análise da venda de maçãs no Brasil!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Img(src="/assets/apple_logo.png", className="header-logo center-image"),
                html.H1(
                    children="Maçã Analytics", className="header-title"
                ),
                html.P(
                    children=(
                        "Análise do comportamento dos preços de maçã e do número"
                        " de maçãs vendidas no Brasil entre 2008 e 2023"
                    ),
                    className="header-description",
                ),
            ],  # Adicionei a vírgula aqui
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Região", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in regions
                            ],
                            value=None,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Tipo de Maçã", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {
                                    "label": tipo_maca.title(),
                                    "value": tipo_maca,
                                }
                                for tipo_maca in tipo_macas
                            ],
                            value=None,
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                #html.Div(
                #    children=[
                #        html.Div(children="Ano", className="menu-title"),
                #        dcc.Dropdown(
                #            id="ano-filter",
                #            options=[
                #                {"label": str(ano), "value": ano}
                #                for ano in ano
                #            ],
                #            value=None,
                #            clearable=False,
                #            className="dropdown",
                #        ),
                #    ]
                #),
            ],
            className="menu",
        ),
        
        dcc.Graph(id="produtor-grafico", config={"displayModeBar": False}),
        dcc.Graph(id="atacado-grafico", config={"displayModeBar": False}),
    ]
)




def gerar_grafico_produtor(region, tipo_macas):
    graf_produtor = data[data["Vendedor"] == "produtor"]
    graf_produtor = graf_produtor.groupby(['Tipo', 'Ano', 'Região'])['Preço'].sum().reset_index()

    # Filtrar por região, se fornecida
    if region is not None and region != "":
        graf_produtor = graf_produtor[graf_produtor["Região"] == region]

    # Filtrar por tipo de maçã, se fornecido
    if tipo_macas is not None and tipo_macas != "":
        tipo_macas = tipo_macas.strip()
        graf_produtor["Tipo"] = graf_produtor["Tipo"].str.strip()
        graf_produtor = graf_produtor[graf_produtor["Tipo"].str.lower() == tipo_macas.lower()]

    # Se tanto região quanto tipo estão em branco, agrupar por tipo para evitar duplicatas
    if (region is None or region == "") and (tipo_macas is None or tipo_macas == ""):
        graf_produtor = graf_produtor.groupby(['Tipo', 'Ano']).agg({'Preço': 'sum'}).reset_index()
        region = "Todos"  # Define a região como "Todos" para a cor

    # Criar o gráfico de linha usando Plotly Express
    fig = px.line(graf_produtor, x='Ano', y='Preço', color='Tipo', markers=True)

    # Atualizar o layout conforme necessário
    fig.update_layout(title=f"Variação do Preço por Tipo e Ano (Produtor - {region})", xaxis_title='Ano', yaxis_title='Média de Preço')

    return fig




def gerar_grafico_atacado(region, tipo_macas):
    graf_atacado = data[data["Vendedor"] == "atacado"]
    graf_atacado = graf_atacado.dropna(subset=['Tipo', 'Ano', 'Região', 'Preço'])
    graf_atacado = graf_atacado.drop_duplicates(['Tipo', 'Ano', 'Região', 'Preço'])
    graf_atacado['Tipo'] = graf_atacado['Tipo'].str.strip()
    graf_atacado = graf_atacado.groupby(['Tipo', 'Ano', 'Região'])['Preço'].mean().reset_index()

    if region is not None and region != "":
        graf_atacado = graf_atacado[graf_atacado["Região"] == region]

    if tipo_macas is not None and tipo_macas != "":
        tipo_macas = tipo_macas.strip()
        graf_atacado["Tipo"] = graf_atacado["Tipo"].str.strip()
        graf_atacado = graf_atacado[graf_atacado["Tipo"].str.lower() == tipo_macas.lower()]


    # Criar o gráfico de linha usando Plotly Express
    fig = px.line(graf_atacado, x='Ano', y='Preço', color='Tipo', markers=True)

    # Atualizar o layout conforme necessário
    fig.update_layout(title="Variação do Preço por Tipo e Ano (Atacado)", xaxis_title='Ano', yaxis_title='Média de Preço')

    return fig



@app.callback(
    Output("produtor-grafico", "figure"),
    Output("atacado-grafico", "figure"),
    Input("region-filter", "value"),
    Input("type-filter", "value"),
)
def update_graficos(region, tipo_macas):
    
    produtor_fig = gerar_grafico_produtor(region, tipo_macas)
    
    atacado_fig = gerar_grafico_atacado(region, tipo_macas)
    
    return produtor_fig, atacado_fig


if __name__ == "__main__":
    app.run_server(debug=True)
