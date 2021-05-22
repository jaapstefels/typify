import os, sys
import warnings
from scholarly import scholarly, ProxyGenerator
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import classifier.classifier as CSO
from collections import Counter
import time
import numpy as np
import pandas as pd
import itertools
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from collections import defaultdict
import copy
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from io import BytesIO
import dash
import dash_table
import base64

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def setup_proxy(http_code):
    """
    Establish connection between Scholarly and a given proxy http code.
    """

    pg = ProxyGenerator()
    pg.SingleProxy(http = http_code, https = http_code)
    scholarly.use_proxy(pg)

def search_pub_titles(author_name):
    """
    Returns all publications for a given author on Google Scholar.
    """

    search_query = scholarly.search_author(author_name)
    try:
        while True:
            author = scholarly.fill(next(search_query))

            title_dict = {pub['bib']['title'] : {'pub_year' : pub['bib']['pub_year'],
                           'num_citations' : pub['num_citations']} for pub in author['publications']
                           if 'pub_year' in pub['bib']}

            author_stats =  {'Name': author.get('name'),
                             'Affiliation': author.get('affiliation'),
                             'Scholar id': author.get('scholar_id'),
                             #'interests': author.get('interests'),
                             'Cited by': author.get('citedby'),
                             'H-index': author.get('hindex'),
                             'i10-index': author.get('i10index'),
                             'Cited by (past 5 years)': author.get('citedby5y'),
                             'H-index (past 5 years)': author.get('hindex5y'),
                             'i10-index (past 5 years)': author.get('i10index5y'),
                             'cites_per_year': author.get('cites_per_year'),
                             'url_picture': author.get('url_picture')}

            return title_dict, author_stats

    except StopIteration:
        return False, False

def extract_keywords(author_dict, workers = 4, modules = 'both', enhancement = "first"):
    papers = {title : {'title' : title} for title in author_dict}

    with HiddenPrints():
        key_words = CSO.run_cso_classifier_batch_mode(papers, workers, modules, enhancement)

    for title in author_dict:
        author_dict[title]['key_words'] = key_words[title]

    return author_dict


def search_abstracts(pub_titles):
    """
    Returns list of all abstracts for a given list of pub_titles.
    """

    abstract_list = []

    for title in tqdm(pub_titles):
        search_query_pub = scholarly.search_pubs(title)
        abstract = next(search_query_pub)['bib']['abstract']
        abstract_list.append(abstract)

    return abstract_list

def create_wordcloud(text):
    """
    Plots a wordcloud for a given piece of text.
    """

    wordcloud = WordCloud(max_font_size = 50, max_words = 15, background_color = "white").generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation = "bilinear")
    plt.axis("off")
    plt.show()

def log_convert(citation_count):
    if citation_count == 0:
        return 0

    return int(np.round(np.log(citation_count)))

def filter_years(years, reject_value = 40):
    return [year for year in years if (year >= int((np.median(years) - reject_value))
            and year <= int((np.median(years) + reject_value)))]

def filter_key_words(key_words, detection_types, quintile_scores, year_range, quintile_factor,
                     reject_value = 40, citation_min = 1, citation_impact = None):
    filtered_key_words = copy.deepcopy(key_words)
    years = np.array([int(key_words[topic]['pub_year']) for topic in filtered_key_words])
    filtered_years = filter_years(years)
    citation_counts = np.array([int(key_words[topic]['num_citations']) for topic in filtered_key_words])
    quintiles = np.percentile(citation_counts, quintile_scores)
    out = np.searchsorted(quintiles, citation_counts)

    for i, title in enumerate(key_words):
        year = int(filtered_key_words[title]['pub_year'])
        all_key_words = [topic for topic_type in detection_types
                         for topic in filtered_key_words[title]['key_words'][topic_type]]

        if (year in filtered_years and year >= year_range[0] and year <= year_range[1]
            and int(filtered_key_words[title]['num_citations']) >= citation_min):
            if citation_impact == 'none':
                filtered_key_words[title]['key_words'] = all_key_words

            if citation_impact == "multiply_cite":
                filtered_key_words[title]['key_words'] = (all_key_words +
                (all_key_words * int(filtered_key_words[title]['num_citations'])))

            if citation_impact == "multiply_log":
                filtered_key_words[title]['key_words'] = (all_key_words +
                (all_key_words * log_convert(int(filtered_key_words[title]['num_citations']))))

            if citation_impact == "quintile":
                filtered_key_words[title]['key_words'] = all_key_words * (out[i] ** quintile_factor)

        else:
            del filtered_key_words[title]

    return filtered_key_words

def generate_occurence_dataframe(filtered_key_words, top):
    topic_per_year = {}

    for title in filtered_key_words:
        year = int(filtered_key_words[title]['pub_year'])
        if year in topic_per_year:
            topic_per_year[year] += filtered_key_words[title]['key_words']

        else:
            topic_per_year[year] = filtered_key_words[title]['key_words']

    incomplete_years = topic_per_year.keys()
    years =  list(range(min(incomplete_years), max(incomplete_years)+1))

    d = {'years' : years}

    for topic in top:
        topic_occurence = [0] * len(years)

        for i, year in enumerate(years):
            if year in topic_per_year:
                occurences = Counter(topic_per_year[year])

                if topic in occurences:
                    topic_occurence[i] = occurences[topic]

        d[topic] = topic_occurence

    df = pd.DataFrame(data=d).set_index('years')

    return df

def plot_topic_evolution(df, stacking = 'stacked'):

    if stacking == 'stacked':
        fig = px.area(df, x=df.index.array, y=df.columns, line_shape='spline')

    if stacking == 'non_stacked':
        fig = go.Figure()
        fig.add_traces([go.Scatter(x=df.index.array, y=df[column].tolist(), fill='tozeroy',
                        line_shape='spline', name=column) for column in df
                        if column != 'years'])

    # Add range slider
    fig.update_layout(
        title= "Topic evolution of top-{} topics.".format(len(df.columns)),
        xaxis_title = "Years",
        yaxis_title= "Topic count",
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ), type="date"
        )
    )

    return fig

def plot_occurences(dictionary, x_label, y_label, fig_title):
    fig = px.bar(pd.DataFrame.from_dict({x_label: list(dictionary.keys()),
                                         y_label: list(dictionary.values())}), x = x_label, y = y_label)
    fig.update_layout(

        title= fig_title,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         step="year",
                         stepmode="backward"),
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
        )
    )

    return fig

def create_author_fig(author_stats):
    fig = go.Figure(data=[go.Table(header=dict(values=[]),
                     cells=dict(values=[list(author_stats.keys())[:9], list(author_stats.values())[:9]]))
                         ])
    fig.layout['template']['data']['table'][0]['header']['fill']['color']='rgba(0,0,0,0)'
    fig.update_layout(
        title= "Author information and statistics"
    )
    return fig

def plot_wordcloud(data, max_word):
        wc = WordCloud(width = 400, height = 200,
                       background_color ='white', max_words = max_word,
                       scale = 2).generate_from_frequencies(data)
        return wc.to_image()

def RepresentsInt(i):
    try:
        int(i)
        if 0 <= int(i) and int(i) <=100:
            return True

    except ValueError:
        return False

def create_citation_figure(filtered, num_top, overlay, top):

    # Create dictionary with yearly citation count.
    citation_per_year = {}
    for title in filtered:
        pub_year = int(filtered[title]['pub_year'])
        num_citations = filtered[title]['num_citations']

        if pub_year in citation_per_year:
            citation_per_year[pub_year] += num_citations

        else:
            citation_per_year[pub_year] = num_citations

    citation_per_year_df = pd.DataFrame.from_dict(citation_per_year, orient='index')

    if len(overlay) == 0:
        fig_cites_year =  px.bar(citation_per_year_df, x=citation_per_year_df.index.array,
                                 y=citation_per_year_df.columns)

    else:
        df_all = generate_occurence_dataframe(filtered, dict(top))
        df_top = generate_occurence_dataframe(filtered, dict(top[:num_top]))
        df_top["Other"] = df_all.sum(axis=1) - df_top.sum(axis=1)

        df_top = df_top.div(df_top.sum(axis = 1), axis = 0)
        df_top["Citations"] = citation_per_year_df
        df_top = df_top.fillna(0)
        df_top = df_top.mul(df_top['Citations'], axis = 0).iloc[:,:-1]

        fig_cites_year =  px.bar(df_top, x=df_top.index.array, y=df_top.columns)

    fig_cites_year.update_layout(
        title= "Citation counts for publications from a specific year",
        xaxis_title = "Years",
        yaxis_title= "Counts",
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ), type="date"
        )
    )

    return fig_cites_year

def select_key_words(key_words, author_selection):
    selected_key_words = {}

    for i in author_selection:
        selected_key_words = {**selected_key_words, **key_words[int(i)]}

    return selected_key_words