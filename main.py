from functions import *

# warnings.filterwarnings('ignore')

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    # Store data used in callbacks.
    dcc.Store(id='key_words'),
    dcc.Store(id='all_author_stats'),
    dcc.Store(id='filtered'),
    dcc.Store(id='top'),

    # Title Div
    html.Div([
        html.Div([
                html.H2("Typify a researcher or research group")
            ], style={'width': '40%', 'display': 'inline-block'}),

        html.Div([
                html.H6("Created by Jaap Stefels", style = {'text-align':'right', 'margin-right' : '20px'}),
            ], style={'width': '60%', 'display': 'inline-block'})
    ]),


    # Author Entry Div
    html.Div([
        dcc.Input(id='input-on-submit', type='text', placeholder = "Enter author name(s)"),
        html.Button('Search', id='submit-val', n_clicks=0, style = {'margin-left': '10px'}),
        html.Div([
            dcc.Loading(
                id="loading-1",
                type="dot",
                children=html.Div(id="loading-output-1")
            )
        ], style = {'margin-left':'40px', 'display':'inline-block'})
    ], style={'margin-bottom': '15px', 'display': 'inline-block'}),

    html.Div([
        html.Div([
            html.H6("General topic extraction", style = {'font-weight': 'bold'}),
            html.Div([
                html.Label("Found author(s)", style = {'font-weight': 'bold'}),
                dcc.Checklist(
                    id="author_select_2",
                    options=[{'label': '', 'value': '_'}],
                    value=[]
                )
            ], style = {'margin': '5px 10px'}),

            html.Div([
                html.Label("Extraction method", style = {'font-weight': 'bold'}),
                dcc.Checklist(
                    id="topic_extraction_dropdown",
                    options=[
                        {'label': 'Semantic', 'value': 'semantic'},
                        {'label': 'Syntactic', 'value': 'syntactic'},
                        {'label': 'Enhanced', 'value': 'enhanced'}
                    ],
                    value=['semantic', 'syntactic']
                )
            ], style = {'margin': '5px 10px'}),

            html.Div([
                    html.Label("Year selection", style = {'font-weight': 'bold', "margin-left" : "10px"}),
                    dcc.RangeSlider(
                        id='my-range-slider-2',
                        min=0,
                        max=1,
                        step=1,
                        value=[0, 1],
                        pushable = True,
                        tooltip=dict(always_visible=False)
                    ),
                    html.Div(id='container_range_slider_years_2', style = {'text-align' : 'center'})
            ], style={'width': '70%'}),

            html.Div([
                html.Label("Citation minimum", style = {'font-weight': 'bold'}),
                dcc.Input(id='citation_min', type='number', value=1, placeholder = "Citation minimum")
            ], style={'margin': '5px 10px'}),

            html.Div([
                html.Label("Citation impact", style = {'font-weight': 'bold'}),
                dcc.Dropdown(
                    id="citation_impact",
                    options=[
                        {'label': 'No impact', 'value': 'none'},
                        {'label': 'Multiply citation', 'value': 'multiply_cite'},
                        {'label': 'Multiply log', 'value': 'multiply_log'},
                        {'label': 'Quintile', 'value': 'quintile'}
                    ],
                    value='none',
                    clearable=False
                )
            ], style={'margin': '5px 10px', 'width': '66%', 'display': 'inline-block'}),

            html.Div([
                html.Div([
                    html.Label("Quintile values", style = {'font-weight': 'bold'}),
                    dcc.Input(id='quantile_factor_input', type='text', value="20, 40, 60, 80", placeholder = "20, 40, 60, 80"),
                    html.Label("Recognised quintiles:"),
                    html.Div(id='quintile_values'),
                ], style={'margin': '5px 10px', 'width': '66%', 'display': 'inline-block'}),

            ], id='options_quintile', style = {'display' : 'block'}),

            # Options tab 1 - Graph
            html.Div([
                html.H6("Graph", style = {'font-weight': 'bold'}),

                html.Div([
                    html.Label("Amount topics plot 1", style = {'font-weight': 'bold'}),
                    dcc.Input(id='topic_num', type='number', value=5, placeholder = "Amount of topics")
                ], style = {'margin': '5px 10px'}),

                html.Div([
                    html.Label("Amount topics plot 2", style = {'font-weight': 'bold'}),
                    dcc.Input(id='topic_num_2', type='number', value=20, placeholder = "Amount of topics_2")
                ], style = {'margin': '5px 10px'}),

                html.Div([
                    html.Label("Smoothing", style = {'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id="smoothing_type",
                        options=[
                            {'label': 'No smoothing', 'value': 'none'},
                            {'label': 'Historical', 'value': 'his'},
                            {'label': 'Future', 'value': 'fut'},
                            {'label': 'Historical & future', 'value': 'hisfut'},
                        ],
                        value='none',
                        clearable=False
                    ),
                ], style={'margin': '5px 10px', 'width': '66%', 'display': 'inline-block'}),

                html.Div([
                    html.Label("Stacking type", style = {'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id="stacked_dropdown",
                        options=[
                                    {'label': 'Stacked', 'value': 'stacked'},
                                    {'label': 'Not stacked', 'value': 'non_stacked'}
                                ],
                        value='stacked',
                        clearable=False)
                ], style={'margin': '5px 10px', 'width': '66%', 'display': 'inline-block'})
            ], id="options_tab_1", style= {'display': 'none'}),

            # Options tab 2 - Word cloud
            html.Div([
                html.H6("Word cloud", style = {'font-weight': 'bold'}),

                html.Div([
                    html.Label("Max words", style = {'font-weight': 'bold'}),
                    dcc.Input(id='max_words', type='number', value=100, placeholder = "Words maximum")
                ], style = {'margin': '5px 10px'})
            ], id = 'options_tab_2', style= {'display': 'none'}),

            # Options tab 4 - Publication information
            html.Div([
                html.H6("Publication information ", style = {'font-weight': 'bold'}),

                html.Div([
                    html.Label("Topic overlay", style = {'font-weight': 'bold'}),
                    dcc.Checklist(
                        id="top_overlay",
                        options=[
                            {'label': 'Topic overlay', 'value': 'top_ov'},
                        ],
                        value=['top_ov']
                    )
                ], style = {'margin': '5px 10px'})
            ], id = 'options_tab_4', style= {'display': 'none'}),

            # Options tab 5 - Author information
            html.Div([
                html.H6("Author information", style = {'font-weight': 'bold'}),
                html.Div([
                    html.Label("Author selection", style = {'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id="author_select",
                        options=[{'label': '', 'value': '_'}],
                        value='_',
                        clearable=False
                    )
                ], style = {'margin': '5px 10px'})
            ], id = 'options_tab_5', style= {'display': 'none'})

        ], style={'width': '20%', 'display': 'inline-block'}),

        html.Div([
            dcc.Tabs(id="all_tabs", children = [
                ##### Tab 1 - Topic evolution - Graphs
                dcc.Tab(label='Topic evolution graphs', value='tab-1', children=[
                    html.Div([
                        html.Div([
                            html.Div([
                                dcc.Graph(id='fig_topic_evolution'),
                                html.P(["This plot shows the evolution of topics over time.", html.Br(),
                                        "Double click on one of the topic names to view the topic separately.", html.Br(),
                                        "Drag the slider underneath to zoom in on specific years."],
                                       style = {'font-size':'15px', 'text-align':'center'})
                            ]),
                            html.Div([
                                dcc.Graph(id='fig_topic_count'),
                                html.P(["This plot shows the occurence count of the found topics.",
                                        html.Br(), "Drag the slider underneath to zoom in on specific topics."],
                                       style = {'font-size':'15px', 'text-align':'center'})
                            ])
                        ], style={'vertical-align': 'top'})
                    ])
                ]),

                ##### Tab 2 - Topic evolution - Word cloud
                dcc.Tab(label='Word cloud', value='tab-2', children=[
                    html.Div([
                        html.Div([
                            html.Img(id="image_wc", style = {'margin':'50px 100px'}),
                            html.P(["This word cloud visualises the occurence count of the found topics.",
                                   html.Br(), "Drag the slider within the options menu to select specific years."],
                                   style = {'font-size':'15px', 'text-align':'center'})
                        ])
                    ], style={'width': '80%', 'display': 'inline-block'})
                ]),

                ##### Tab 3 - Topic table
                dcc.Tab(label='Topic table', value='tab-3', children=[
                    html.Div([
                        dash_table.DataTable(
                            id='table',
                            columns= [{"name": "Publication title", "id": "Publication title"},
                                      {"name": "Year", "id" : "Year"},
                                      {"name": "Cited", "id" : "Cited"},
                                      {"name": "Topics", "id" : "Topics"},],
                            data= [{}],
                            style_cell={'textAlign': 'left'},
                            style_data={
                                'whiteSpace': 'normal',
                                'height': 'auto',
                            },

                            style_as_list_view=True,
                            sort_action="native",
                            style_cell_conditional=[
                                {'if': {'column_id': 'Title'},
                                 'width': '40%'},
                                {'if': {'column_id': 'Year'},
                                 'width': '10%'},
                                {'if': {'column_id': 'Cited'},
                                 'width': '10%'},
                                {'if': {'column_id': 'Topics'},
                                 'width': '40%'},
                            ],
                            style_table={'height': '600px', 'overflowY': 'auto'}
                        )
                    ], style={'margin-top': '15px'})
                ]),

                ##### Tab 4 - Publication information
                dcc.Tab(label='Publication information', value='tab-4', children=[
                    html.Div([
                        html.Div([
                            dcc.Graph(id='fig_articles_year'),
                            html.P(["This plot shows the amount of publications published per year.",
                                    html.Br(), "Drag the slider underneath to zoom in on specific years."],
                                   style = {'font-size':'15px', 'text-align':'center'})
                        ]),

                        html.Div([
                            dcc.Graph(id='fig_cites_year'),
                            html.P(["This plot shows the amount of combined citations of all publications published in a specific publication year.",
                                    html.Br(), "The topic overlay option shows the distribution of topics found within these publications.",
                                    html.Br(), "Drag the slider underneath to zoom in on specific years."]
                                   , style = {'font-size':'15px', 'text-align':'center'})
                        ])
                    ], style={"text-align":'center'})
                ]),

                ##### Tab 5 - Author information
                dcc.Tab(label='Author information', value='tab-5', children=[
                    html.Div([
                        dcc.Graph(id='author_fig'),
                        html.P(["This table shows author information and statistics.",
                                html.Br(), "In case of multiple authors, select the desired author\
                                within the options menu."],
                               style = {'font-size':'15px', 'text-align':'center'})
                    ]),
                    html.Div([
                        dcc.Graph(id='fig_cites_year_google'),
                        html.P(["This plot shows the citation counts per year.",
                                html.Br(), "Drag the slider underneath to zoom in on specific years."],
                               style = {'font-size':'15px', 'text-align':'center'})
                    ])
                ])
            ])
        ], style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'top'})
    ], id='options_and_tabs', style = {'display':'block'}),

    html.Div(id='error_message', style = {'display':'none'})
])

@app.callback(
    Output('key_words', 'data'),
    Output('all_author_stats', 'data'),
    Output("loading-output-1", "children"),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)

def update_output(n_clicks, author_input):
    if author_input is None:
        raise dash.exceptions.PreventUpdate

    author_list = [author.strip() for author in author_input.split(",")]
    all_key_words = []
    all_author_stats = []

    for author in author_list:
        start = time.time()
        title_dict, author_stats = search_pub_titles(author)

        if title_dict:
            print("\n{} publications found for author {}.".format(len(title_dict), author),
                 "Searching for key words.")

            # Extract data
            key_words = extract_keywords(title_dict, workers = 4, modules = 'both', enhancement = "first")
            end = time.time()

            print("Searching took {} seconds. \n".format((end - start)))
            all_key_words.append(key_words)
            all_author_stats.append(author_stats)

        else:
            print("\nNo publications found for author {}. Did you spell the name correctly?".format(author))

    return all_key_words, all_author_stats, ""

@app.callback(
    Output('quintile_values', 'children'),
    Input('quantile_factor_input', 'value')
)

def callback_quintiles(quintile_input):
    quintile_values = [int(i) for i in list(quintile_input.split(",")) if RepresentsInt(i)]

    if len(quintile_values) == 0:
        raise dash.exceptions.PreventUpdate

    return '{}'.format(sorted(quintile_values))

@app.callback(
    Output('author_select', 'value'),
    Output('author_select', 'options'),
    Output('author_select_2', 'value'),
    Output('author_select_2', 'options'),
    Input('all_author_stats', 'data')
)

def callback_create_author_table(all_author_stats):
    if len(all_author_stats) == 0:
        raise dash.exceptions.PreventUpdate

    options = [{'label': stats['Name'], 'value' : str(i)}
               for i, stats in enumerate(all_author_stats)]

    return '0', options, [str(i) for i in range(len(options))], options

@app.callback(
    Output('my-range-slider-2', 'min'),
    Output('my-range-slider-2', 'max'),
    Output('my-range-slider-2', 'value'),
    Input('key_words', 'data')
)

def callback_prepare_range_slider(key_words):
    if key_words is None or len(key_words) == 0:
        raise dash.exceptions.PreventUpdate

    years = list(set([int(key_word_set[title]['pub_year']) for
                      key_word_set in key_words for title in key_word_set]))
    years_filtered = filter_years(years)
    min_year = min(years_filtered)
    max_year = max(years_filtered)

    return min_year, max_year, [min_year, max_year]

@app.callback(
    Output('container_range_slider_years_2', 'children'),
    Input('my-range-slider-2', 'value')
)

def callback_edit_year_range(year_value):
    if year_value == [0, 1]:
        return '- to -'

    return '{} to {}'.format(year_value[0], year_value[1])

@app.callback(
    Output('filtered', 'data'),
    Output('top', 'data'),
    Output('table', 'data'),
    Input('key_words', 'data'),
    Input('citation_min', 'value'),
    Input('topic_extraction_dropdown', 'value'),
    Input('citation_impact', 'value'),
    Input('quantile_factor_input', 'value'),
    Input('author_select_2', 'value'),
    Input('my-range-slider-2', 'value')
)

def callback_preprocess(key_words, citation, extraction_types, citation_impact,
                        quintile_input, author_selection, year_range):
    quintile_values = [int(i) for i in list(quintile_input.split(",")) if RepresentsInt(i)]

    if key_words is None or citation is None or author_selection is None:
        raise dash.exceptions.PreventUpdate

    if len(extraction_types) == 0 or len(quintile_values) == 0 or len(author_selection) == 0:
        raise dash.exceptions.PreventUpdate

    # Pre-process data
    key_words = select_key_words(key_words, author_selection)
    filtered = filter_key_words(key_words, extraction_types, quintile_values, year_range,
                                1, 40, citation, citation_impact)
    top = Counter([word for title in filtered for word in filtered[title]['key_words']]).most_common()

    dict_list = []

    for title in filtered:
        temp_dict = {}
        temp_dict["Publication title"] = title
        temp_dict["Year"] = filtered[title]['pub_year']
        temp_dict["Cited"] = filtered[title]['num_citations']
        temp_dict["Topics"] = str(filtered[title]['key_words'])
        dict_list.append(temp_dict)

    return filtered, top, dict_list

@app.callback(
    Output('author_fig', 'figure'),
    Output('fig_cites_year_google', 'figure'),
    Input('all_author_stats', 'data'),
    Input('author_select', 'value')
)

def callback_create_author_table(all_author_stats, author_value):
    if author_value == '_' or len(all_author_stats) == 0:
        raise dash.exceptions.PreventUpdate

    author_fig = create_author_fig(all_author_stats[int(author_value)])
    article_count = all_author_stats[int(author_value)]['cites_per_year']
    title = "Citations counts per year"
    fig_cites_year_google = plot_occurences(article_count, 'Year', 'Count', title)

    return author_fig, fig_cites_year_google

@app.callback(
    Output('fig_topic_count', 'figure'),
    Output('fig_topic_evolution', 'figure'),
    Output('fig_cites_year', 'figure'),
    Output('fig_articles_year', 'figure'),
    Input('filtered', 'data'),
    Input('top', 'data'),
    Input('topic_num', 'value'),
    Input('topic_num_2', 'value'),
    Input('stacked_dropdown', 'value'),
    Input('smoothing_type', 'value'),
    Input('top_overlay', 'value')
)

def callback_create_figs(filtered, top, topic_num, topic_num_2, stack_type, smoothing_type, topic_overlay):
    if (filtered is None or top is None or topic_num is None or topic_num_2 is None or
    len(filtered) == 0 or len(top) == 0):
        raise dash.exceptions.PreventUpdate

    df = generate_occurence_dataframe(filtered, dict(top[:topic_num]))
    kernels = {"none" : [1], "his" : [0.5,1,0], "fut" : [0,1,0.5], "hisfut" : [0.5,1,0.5]}
    modDfObj = df.transform(lambda x: np.convolve(x, kernels[smoothing_type], 'same'))

    fig_topic_evolution = plot_topic_evolution(modDfObj, stacking = stack_type)
    fig_topic_count = plot_occurences(dict(top[:topic_num_2]), 'Topic', 'Count', "Topic count of top-{} topics".format(topic_num_2))
    article_count = dict(Counter([int(filtered[title]['pub_year']) for title in filtered]).most_common())
    fig_articles_year = plot_occurences(article_count, 'Year', 'Count', "Amount of articles published per year")
    fig_cites_year = create_citation_figure(filtered, topic_num, topic_overlay, top)

    return fig_topic_count, fig_topic_evolution, fig_cites_year, fig_articles_year

@app.callback(
    Output('image_wc', 'src'),
    Input('filtered', 'data'),
    Input('max_words', 'value'),
)

def callback_create_word_cloud(filtered, max_words):
    if filtered is None or len(filtered) == 0:
        raise dash.exceptions.PreventUpdate

    top = Counter([word for title in filtered for word in filtered[title]['key_words']]).most_common()
    img = BytesIO()
    plot_wordcloud(dict(top), max_words).save(img, format='PNG')
    image_wc = 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

    return image_wc

@app.callback(
    Output(component_id='options_tab_1', component_property='style'),
    Output(component_id='options_tab_2', component_property='style'),
    Output(component_id='options_tab_4', component_property='style'),
    Output(component_id='options_tab_5', component_property='style'),
    Input('all_tabs', 'value')
)

def callback_tabs(tab):
    if tab == 'tab-1':
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

    if tab == 'tab-2':
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}

    if tab == 'tab-3':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

    if tab == 'tab-4':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}

    if tab == 'tab-5':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}

    return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

@app.callback(
    Output(component_id='options_quintile', component_property='style'),
    Input('citation_impact', 'value')
)

def callback_quintile(impact_option):
    if impact_option == 'quintile':
        return {'display': 'block'}

    else:
        return {'display': 'none'}

@app.callback(
    Output(component_id='options_and_tabs', component_property='style'),
    Output(component_id='error_message', component_property='style'),
    Output(component_id='error_message', component_property='children'),
    Input('all_author_stats', 'data'),
    State('input-on-submit', 'value')
)

def callback_no_author(all_author_stats, author_input):
    if len(all_author_stats) == 0:
        error_message = "No publications found for author(s) {}. \
        Use a comma to seperate multiple authors.".format(author_input)
        return {'display': 'none'}, {'display': 'block', 'margin-left':'10px'}, error_message

    else:
        return {'display': 'block'}, {'display': 'none'}, "-"

if __name__ == '__main__':
    app.run_server(debug=True)
