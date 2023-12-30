
# Maçã Analytics

Este projeto analisa o comportamento dos preços de maçã e o volume de maçãs vendidas no Brasil entre os anos de 2008 e 2023. A análise é dividida entre os vendedores "produtor" e "atacado", com visualizações gráficas interativas usando Dash, Plotly e Pandas.


## Conteúdo do Projeto

O projeto é composto pelos seguintes arquivos e diretórios:

### Arquivos Principais

    1 - app.py: O principal script Dash que configura a interface do usuário e define as callbacks para atualizar os gráficos.
    
    2 -  macas_Brasil.csv: O conjunto de dados contendo informações sobre preços e vendas de maçãs.

### Diretórios

    assets: Contém recursos estáticos, como logotipos e imagens.

## Como Executar o Projeto

1 - Certifique-se de ter todas as bibliotecas necessárias instaladas. Você pode fazer isso executando:
```bash
  pip install pandas plotly dash numpy
```
2 - Execute o aplicativo Dash:
```bash
  python app.py
``` 
3 - Abra um navegador da web e vá para http://127.0.0.1:8050/ para acessar o painel interativo.
## Detalhes da Implementação

### Estrutura do Layout

O layout do aplicativo consiste em uma barra de cabeçalho, um menu lateral para filtros e dois gráficos para exibir as visualizações de dados.

### Filtros

Os filtros permitem ao usuário selecionar a região e o tipo de maçã para analisar. O aplicativo usa esses filtros para gerar gráficos interativos.

### Gráficos

O aplicativo exibe dois gráficos, um para o vendedor "produtor" e outro para o vendedor "atacado". Cada gráfico mostra a variação do preço por tipo e ano, permitindo uma análise visual rápida.

### Callbacks

As callbacks são utilizadas para atualizar os gráficos conforme as seleções do usuário nos filtros.


## Melhorias

O projeto pode ser expandido com as seguintes melhorias:

- Adição de um filtro para o ano.
- Aprimoramento da estética dos gráficos.
- Inclusão de mais análises estatísticas.

Sinta-se à vontade para explorar e expandir este projeto de acordo com suas necessidades e objetivos.
