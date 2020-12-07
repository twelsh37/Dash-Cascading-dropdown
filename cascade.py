import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read in our RACA raw data files and append them to the initial df dataframe
df = pd.read_excel('c:/Users/twelsh/data/racas/master/master1.xlsx')

# Rename all column headings to human readable and remove spaces, brackets in description names
# Take our imported data in df and reassign it with new headers to raca_df.
# We will use raca_df and the new column headings from here forward.
raca_df = df.rename(columns={'Process (Title)': 'process_title',
                             'Process description': 'process_description',
                             'Risk ID': 'risk_id',
                             'Risk Owner': 'risk_owner',
                             'Risk(Title)': 'risk_title',
                             'Risk Description': 'risk_description',
                             'Risk Category 1': 'risk_types',
                             'Risk Category 2': 'risk',
                             'Risk Category 3': 'level3',
                             'Associated KRIs': 'associated_kris',
                             'I': 'gross_impact',
                             'L': 'gross_likelihood',
                             'Control ID': 'control_id',
                             'Control Owner': 'control_owner',
                             'Control (Title)': 'control_title',
                             'Control Description': 'control_description',
                             'Control Activity': 'control_activity',
                             'Control Type': 'control_type',
                             'Control Frequency': 'control_frequency',
                             'DE & OE?': 'de_oe',
                             'Commentary on DE & OE assessment': 'de_oe_commentary',
                             'I.1': 'net_impact',
                             'L.1': 'net_likelihood',
                             'Commentary on Net Risk Assessment': 'net_risk_assesment_commentary',
                             'Risk Decision': 'risk_decision',
                             'Issue Description (if applicable)': 'issue_description',
                             'Action Description': 'action_description',
                             'Action Owner': 'action_owner',
                             'Action Due Date': 'action_due_date',
                             'Completion Date': 'completion_date'
                             }
                    )

# Reset our index colum so it is contiguous
raca_df.reset_index(drop=True,
                    inplace=True,
                    col_level=0)

# Start the row index at 1 just to make it easier for mortals
raca_df.index = raca_df.index + 1
# -----------------------------------------------------#

# Global variable to hold our data frame olutput from teh dropdown listboxes
output_dataframe = None

# DEBUGGING ##
# -----------------------------------------------------#
# Inform user that data loaded sucsessfully
print('Data loaded successfully')
print(raca_df.head())
print(raca_df['risk_types'].unique())
# -----------------------------------------------------#


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )



# Setup our Dropdown Listboxes to filter results based on our choices
# Note there is no checking currently of what level 3 categories
# belong to level 2 categories, whhich inb turn belong to level 1
# categories. - But i'm working on it.
# -----------------------------------------------------#

app.layout = html.Div([
    # Taxonomy Level 1 Dropdown List box
    dcc.Dropdown(
        id='risk_types',
        options=[{'label': k, 'value': k} for k in sorted(raca_df['risk_types'].unique())],
        value='Operational Risk'
    ),

    html.Hr(),
    # Taxonomy Level 2 Dropdown List Box
    dcc.Dropdown(id='risk'),

    html.Hr(),

    # Level 3 Dropdown List Box
    dcc.Dropdown(id='level3'),

    # Display the values selected from the dropdowns
    html.Hr(),
    html.Div(id='answer')
])

# Setup cascade to TL2 dropdown
@app.callback(
    Output('risk', 'options'),
    Input('risk_types', 'value'))
def set_tl2_options(selected_country):
    return [{'label': i, 'value': i} for i in sorted(raca_df['risk'].unique())]


@app.callback(
    Output('risk', 'value'),
    Input('risk', 'options'))
def set_tl2_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('level3', 'options'),
    Input('risk', 'value'))
def set_level3_options(selected_country):
    return [{'label': i, 'value': i} for i in sorted(raca_df['level3'].unique())]

@app.callback(
    Output('level3', 'value'),
    Input('level3', 'options'))
def set_level3_values(available_options):
    return available_options[0]['value']

# Get all the inputs and output them to a sentence
# This proves we can get values from the dropdowns
# so we should now be able to pull values to sort
# dataframes
@app.callback(
    Output('answer', 'children'),
    Input('risk_types', 'value'),
    Input('risk', 'value'),
    Input('level3', 'value')
)
def set_display_children(selected_country, selected_city, available_options):
    return 'Taxonomy Level 1 is {}, Taxonomy Level 2 is {} and level 3 is {}'.format(
        selected_country, selected_city,  available_options,
    )


if __name__ == '__main__':
    app.run_server(debug=True)
