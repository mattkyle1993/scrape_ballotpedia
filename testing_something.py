import pandas as pd
def return_states_list_and_stage_groups_urls(split_states=False):
    urls = pd.read_excel("BPStateLegislaturePages.xlsx",)
    urls.rename(columns={"House":"ballotpedia_url"},inplace=True)
    state_groups_urls = urls['ballotpedia_url'].tolist()
    # state_groups_urls = state_groups_urls[20:30]
    headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding': 'none',
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Connection': 'keep-alive',
                    'Referer': ''
                }
    states = [
        'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware',
        'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky',
        'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri',
        'montana', 'nebraska', 'nevada', 'new_hampshire', 'new_jersey', 'new_mexico', 'new_york',
        'north_carolina', 'north_dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode_island',
        'south_carolina', 'south_dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington',
        'west_virginia', 'wisconsin', 'wyoming'
    ]
    states = [' '.join([part.capitalize() for part in state.split('_')]) for state in states]
    under_states = [state.replace(" ","_") for state in states if state.count(" ") == 1]
    no_under_states = [state for state in states if state.count(" ") == 0]
    states = under_states + no_under_states

    if split_states == True:
        return under_states, no_under_states, state_groups_urls,headers
    if split_states == False:
        return states, state_groups_urls,headers

# list_ = ['U.S. Senate Alabama', 'U.S. Senate Alabama', 'U.S. Senate Alabama', 'U.S. Senate Alabama', 'U.S. Senate Alaska', 'U.S. Senate Alaska', 'U.S. Senate Alaska', 'U.S. Senate Alaska', 'U.S. Senate Arkansas', 'U.S. Senate Arkansas', 'U.S. Senate Arkansas', 'U.S. Senate Arkansas', 'U.S. Senate Florida', 'U.S. Senate Florida', 'U.S. Senate Florida',
#           'U.S. Senate Florida', 'U.S. Senate Idaho', 'U.S. Senate Idaho', 'U.S. Senate Idaho', 'U.S. Senate Idaho', 'U.S. Senate Indiana', 'U.S. Senate Indiana', 'U.S. Senate Indiana', 'U.S. Senate Indiana', 'U.S. Senate Indiana', 'U.S. Senate Indiana', 'U.S. Senate Kansas', 'U.S. Senate Kansas', 'U.S. Senate Kansas', 'U.S. Senate Kansas', 'U.S. Senate Kentucky', 'U.S. Senate Kentucky', 'U.S. Senate Kentucky', 'U.S. Senate Kentucky', 'U.S. Senate Louisiana', 'U.S. Senate Louisiana', 'U.S. Senate Louisiana', 'U.S. Senate Louisiana', 'U.S. Senate Maine', 'U.S. Senate Maine', 'U.S. Senate Mississippi', 'U.S. Senate Mississippi', 'U.S. Senate Missouri', 'U.S. Senate Missouri', 'U.S. Senate Missouri', 'U.S. Senate Missouri', 'U.S. Senate Montana', 'U.S. Senate Montana', 'U.S. Senate Nebraska', 'U.S. Senate Nebraska', 'U.S. Senate Nebraska', 'U.S. Senate Nebraska', 'U.S. Senate North Carolina', 'U.S. Senate North Carolina', 'U.S. Senate North Carolina', 'U.S. Senate North Carolina', 'U.S. Senate North Dakota', 'U.S. Senate North Dakota', 'U.S. Senate North Dakota', 'U.S. Senate North Dakota', 'U.S. Senate Ohio', 'U.S. Senate Ohio', 'U.S. Senate Oklahoma', 'U.S. Senate Oklahoma', 'U.S. Senate Oklahoma', 'U.S. Senate Oklahoma', 'U.S. Senate South Carolina', 'U.S. Senate South Carolina', 'U.S. Senate South Carolina', 'U.S. Senate South Carolina', 'U.S. Senate South Dakota', 'U.S. Senate South Dakota', 'U.S. Senate South Dakota', 'U.S. Senate South Dakota', 'U.S. Senate Tennessee', 'U.S. Senate Tennessee', 'U.S. Senate Tennessee', 'U.S. Senate Tennessee', 'U.S. Senate Texas', 'U.S. Senate Texas', 'U.S. Senate Texas', 'U.S. Senate Texas', 'U.S. Senate Utah', 'U.S. Senate Utah', 'U.S. Senate Utah', 'U.S. Senate Utah', 'U.S. Senate Wyoming', 'U.S. Senate Wyoming', 'U.S. House Alabama District 1', 'U.S. House Alabama District 1', 'U.S. House Alabama District 1', 'U.S. House Alabama District 2', 'U.S. House Alabama District 2', 'U.S. House Alabama District 3', 'U.S. House Alabama District 3', 'U.S. House Alabama District 3', 'U.S. House Alabama District 4', 'U.S. House Alabama District 4', 'U.S. House Alabama District 5', 'U.S. House Alabama District 5', 'U.S. House Alabama District 5', 'U.S. House Alabama District 6', 'U.S. House Alabama District 6', 'U.S. House Arizona District 1', 'U.S. House Arizona District 1', 'U.S. House Arizona District 2', 'U.S. House Arizona District 2', 'U.S. House Arizona District 2', 'U.S. House Arizona District 5', 'U.S. House Arizona District 5', 'U.S. House Arizona District 6', 'U.S. House Arizona District 6', 'U.S. House Arizona District 6', 'U.S. House Arizona District 8', 'U.S. House Arizona District 8', 'U.S. House Arizona District 8', 'U.S. House Arizona District 9', 'U.S. House Arizona District 9', 'U.S. House Arkansas District 1', 'U.S. House Arkansas District 1', 'U.S. House Arkansas District 1', 'U.S. House Arkansas District 2', 'U.S. House Arkansas District 2', 'U.S. House Arkansas District 3', 'U.S. House Arkansas District 3', 'U.S. House Arkansas District 3', 'U.S. House Arkansas District 4', 'U.S. House Arkansas District 4', 'U.S. House California District 1', 'U.S. House California District 1', 'U.S. House California District 1', 'U.S. House California District 3', 'U.S. House California District 3', 'U.S. House California District 3', 'U.S. House California District 5', 'U.S. House California District 5', 'U.S. House California District 5', 'U.S. House California District 13', 'U.S. House California District 13', 'U.S. House California District 13', 'U.S. House California District 22', 'U.S. House California District 22', 'U.S. House California District 23', 'U.S. House California District 23', 'U.S. House California District 23', 'U.S. House California District 27', 'U.S. House California District 27', 'U.S. House California District 27', 'U.S. House California District 40', 'U.S. House California District 40', 'U.S. House California District 41', 'U.S. House California District 41', 'U.S. House California District 41', 'U.S. House California District 45', 'U.S. House California District 45', 'U.S. House California District 45', 'U.S. House',
#         'California District 48', 'U.S. House California District 48', 'U.S. House Colorado District 3', 'U.S. House Colorado District 3', 'U.S. House Colorado District 3', 'U.S. House Colorado District 4', 'U.S.',
#         'House Colorado District 4', 'U.S. House Colorado District 5', 'U.S. House Colorado District 5', 'U.S. House Colorado District 5', 'U.S. House Florida District 1', 'U.S. House Florida District 1', 'U.S. House Florida District 1', 'U.S. House Florida District 2',
#           'U.S. House Florida District 2', 'U.S. House Florida District 3', 'U.S. House Florida District 3', 'U.S. House Florida District 3', 'U.S. House Florida District 4', 'U.S. House Florida District 4', 'U.S. House Florida District 5', 'U.S. House Florida District 5', 'U.S. House Florida District 5', 'U.S. House Florida District 6', 'U.S. House Florida', 
#         'District 6', 'U.S. House Florida District 7', 'U.S. House Florida District 7', 'U.S. House Florida District 7', 'U.S. House Florida District 8', 'U.S. House Florida District 8', 'U.S. House Florida District 11', 'U.S. House Florida District 11', 'U.S. House Florida District 11', 'U.S. House Florida District 12', 'U.S. House Florida District 12', 
#         'U.S. House Florida District 13', 'U.S. House Florida District 13', 'U.S. House Florida District 13', 'U.S. House Florida District 15.', 'U.S. House Florida District 15.', 'U.S. House Florida District 15.', 'U.S. House Florida District 16', 'U.S. House Florida District 16', 'U.S. House Florida District 17', 'U.S. House Florida District 17', 
#         'U.S. House Florida District 17', 'U.S. House Florida District 18', 'U.S. House Florida District 18', 'U.S. House Florida District 19', 'U.S. House Florida District 19', 'U.S. House Florida District 19', 'U.S. House Florida District 21', 'U.S. House Florida District 21', 'U.S. House Florida District 21', 'U.S. House Florida District 26', 
#         'U.S. House Florida District 26', 'U.S. House Florida District 27', 'U.S. House Florida District 27', 'U.S. House Florida District 27', 'U.S. House Florida District 28', 'U.S. House Florida District 28', 'U.S. House Georgia District 1', 'U.S. House Georgia District 1', 'U.S. House Georgia District 1', 'U.S. House Georgia District 3',
#           'U.S. House Georgia District 3', 'U.S. House Georgia District 3', 'U.S. House Georgia District 6', 'U.S. House Georgia District 6', 'U.S. House Georgia District 8', 'U.S. House Georgia District 8', 'U.S. House Georgia District 9', 'U.S. House Georgia District 9', 'U.S. House Georgia District 9', 'U.S. House Georgia District 10', 
#           'U.S. House Georgia District 10', 'U.S. House Georgia District 11', 'U.S. House Georgia District 11', 'U.S. House Georgia District 11', 'U.S. House Georgia District 12', 'U.S. House Georgia District 12', 'U.S. House Georgia District 12', 'U.S. House Georgia District 12', 'U.S. House Idaho District 1', 'U.S. House Idaho District 1',
#             'U.S. House Idaho District 2', 'U.S. House Idaho District 2', 'U.S. House Idaho District 2', 'U.S. House Illinois District 12', 'U.S. House Illinois District 12', 'U.S. House Illinois District 12', 'U.S. House Illinois District 15', 'U.S. House Illinois District 15', 'U.S. House Illinois District 16', 'U.S. House Illinois District 16',
#               'U.S. House Illinois District 16', 'U.S. House Indiana District 2', 'U.S. House Indiana District 2', 'U.S. House Indiana District 3', 'U.S. House Indiana District 3', 'U.S. House Indiana District 3', 'U.S. House Indiana District 4', 'U.S. House Indiana District 4', 'U.S. House Indiana District 5', 'U.S. House Indiana District 5',
#                 'U.S. House Indiana District 5', 'U.S. House Indiana District 6', 'U.S. House Indiana District 6', 'U.S. House Indiana District 8', 'U.S. House Indiana District 8', 'U.S. House Indiana District 9', 'U.S. House Indiana District 9', 'U.S. House Indiana District 9', 'U.S. House Indiana District 9', 'U.S. House Indiana District 9',
#                   'U.S. House Indiana District 9', 'U.S. House Indiana District 9', 'U.S. House Indiana District 9', 'U.S. House Indiana District 9', 'U.S. House Indiana District 9', 'U.S. House Indiana District 9', 'U.S. House Indiana District 9', 'U.S. House Indiana District 9', 'U.S. House Kansas District 1', 'U.S. House Kansas District 1', 'U.S. House Kansas District 2', 'U.S. House Kansas District 2', 'U.S. House Kansas District 2', 'U.S. House', 
#         'Kansas District 4', 'U.S. House Kansas District 4', 'U.S. House Kansas District 4', 'U.S. House Kentucky District 1', 'U.S. House Kentucky District 1', 'U.S. House Kentucky District 2', 'U.S. House Kentucky District 2', 'U.S. House Kentucky District 2', 'U.S. House Kentucky District 4', 
#         'U.S. House Kentucky District 4', 'U.S. House Kentucky District 4', 'U.S. House Kentucky District 5', 'U.S. House Kentucky District 5', 'U.S. House Kentucky District 6', 'U.S. House Kentucky District 6', 'U.S. House Kentucky District 6', 'U.S. House Louisiana District 1', 'U.S. House Louisiana District 1', 'U.S. House Louisiana District 3', 
#         'U.S. House Louisiana District 3', 'U.S. House Louisiana District 4', 'U.S. House Louisiana District 4', 'U.S. House Louisiana District 4', 'U.S. House Louisiana District 5', 'U.S. House Louisiana District 5', 'U.S. House Louisiana District 6', 'U.S. House Louisiana District 6', 'U.S. House Louisiana District 6', 'U.S. House Maryland District 1', 'U.S. House Maryland District 1', 'U.S.', 
#         'House Michigan District 1', 'U.S. House Michigan District 1', 'U.S. House Michigan District 1', 'U.S. House Michigan District 2', 'U.S. House Michigan District 2', 'U.S. House Michigan District 4', 'U.S.',
#         'House Michigan District 4', 'U.S. House Michigan District 5', 'U.S. House Michigan District 5', 'U.S. House Michigan District 5', 'U.S. House Michigan District 9', 'U.S. House Michigan District 9', 'U.S.',
#         'House Michigan District 9', 'U.S. House Michigan District 10', 'U.S. House Michigan District 10', 'U.S. House Minnesota District 1', 'U.S. House Minnesota District 1', 'U.S. House Minnesota District 6', 'U.S. House Minnesota District 6', 'U.S. House Minnesota District 6', 
#         'U.S. House Minnesota District 7', 'U.S. House Minnesota District 7', 'U.S. House Minnesota District 8', 'U.S. House Minnesota District 8', 'U.S. House Minnesota District 8', 'U.S. House Mississippi District 1', 'U.S. House Mississippi District 1', 'U.S. House Mississippi District 3', 
#         'U.S. House Mississippi District 3', 'U.S. House Mississippi District 4', 'U.S. House Mississippi District 4', 'U.S. House Mississippi District 4', 'U.S. House Missouri District 2', 'U.S. House Missouri District 2', 'U.S. House Missouri District 2', 'U.S. House Missouri District 3',
#           'U.S. House Missouri District 3', 'U.S. House Missouri District 4', 'U.S. House Missouri District 4', 'U.S. House Missouri District 4', 'U.S. House Missouri District 6', 'U.S. House Missouri District 6', 'U.S. House Missouri District 6', 'U.S. House Missouri District 7', 
#           'U.S. House Missouri District 7', 'U.S. House Missouri District 8', 'U.S. House Missouri District 8', 'U.S. House Missouri District 8', 'U.S. House Montana District 1', 'U.S. House Montana District 1', 'U.S. House Montana District 2', 'U.S. House Montana District 2', 'U.S. House Montana District 2', 'U.S. House', 
#         'Nebraska District 1', 'U.S. House Nebraska District 1', 'U.S. House Nebraska District 2', 'U.S. House Nebraska District 2', 'U.S. House Nebraska District 2', 'U.S. House Nebraska District 3', 'U.S. House',
#         'Nebraska District 3', 'U.S. House Nevada District 2', 'U.S. House Nevada District 2', 'U.S. House New Jersey District 2 Jeff', 'U.S. House New Jersey District 2 Jeff', 'U.S. House New Jersey District 4 Chris', 'U.S. House New Jersey District 4 Chris', 'U.S. House New Jersey District 7 Thomas',
#           'U.S. House New Jersey District 7 Thomas', 'U.S. House New Jersey District 7 Thomas', 'U.S. House New York District 1 Nicholas', 'U.S. House New York District 1 Nicholas', 'U.S. House New York District 2 Andrew', 'U.S. House New York District 2 Andrew', 'U.S. House New York District 2 Andrew', 'U.S. House New York District 4 Anthony', 
#           'U.S. House New York District 4 Anthony', 'U.S. House New York District 4 Anthony', 'U.S. House New York District 11 Nicole', 'U.S. House New York District 11 Nicole', 'U.S. House New',
#         'York District 17 Michael', 'U.S. House New York District 17 Michael', 'U.S. House New York District 19 Marcus', 'U.S. House New York District 19 Marcus', 'U.S. House New York District 21 Elise', 'U.S. House New York District 21 Elise', 
#         'U.S. House New York District 22 Brandon', 'U.S. House New York District 22 Brandon', 'U.S. House New York District 22 Brandon', 'U.S. House New York District 23 Nick', 'U.S. House New York District 23 Nick', 'U.S. House New York District 24 Claudia', 'U.S. House New York District 24 Claudia', 
#         'U.S. House New York District 24 Claudia', 'U.S. House North Carolina District 3', 
#         'Gregory', 'U.S. House North Carolina District 3 Gregory', 'U.S. House North Carolina District 3 Gregory', 'U.S. House North Carolina District 5 Virginia', 'U.S. House North Carolina District 5 Virginia', 
#         'U.S. House North Carolina District 5 Virginia', 'U.S. House North Carolina District 7 David', 'U.S. House North Carolina District 7 David', 'U.S. House North Carolina District 7 David', 'U.S. House North Carolina District 8 Dan', 'U.S. House North Carolina District 8 Dan', 
#         'U.S. House North Carolina District 9 Richard', 'U.S. House North Carolina District 9 Richard', 'U.S. House North Carolina District 9 Richard', 'U.S. House North Carolina District 10 Patrick', 'U.S. House North Carolina District 10 Patrick', 'U.S. House North Carolina District 11 Chuck', 
#         'U.S. House North Carolina District 11 Chuck', 'U.S. House North Carolina District 11 Chuck', 'U.S. House North Dakota At-large District Kelly', 'U.S. House North Dakota At-large District Kelly', 'U.S. House Ohio District 2', 'U.S. House Ohio District', 
#         '2', 'U.S. House Ohio District 4', 'U.S. House Ohio District 4', 'U.S. House Ohio District 5', 'U.S. House Ohio District 5', 'U.S. House Ohio District 5', 'U.S. House Ohio District 7', 'U.S. House Ohio District 7', 'U.S. House Ohio District 7', 'U.S. House Ohio District 8',
#           'U.S. House Ohio District 8', 'U.S. House Ohio District 10', 'U.S. House Ohio District 10', 'U.S. House Ohio District 12', 'U.S. House Ohio District 12', 'U.S. House Ohio District 14', 'U.S. House Ohio District 14', 'U.S. House Ohio District 15', 'U.S. House Ohio District 15', 'U.S. House Ohio District 15', 'U.S. House Oklahoma District 1',
#             'U.S. House Oklahoma District 1', 'U.S. House Oklahoma District 2', 'U.S. House Oklahoma District 2', 'U.S. House Oklahoma District 2', 'U.S. House Oklahoma District 3', 'U.S. House Oklahoma District 3', 'U.S. House Oklahoma District 4', 'U.S. House Oklahoma District 4', 'U.S. House Oklahoma District 4', 'U.S. House Oklahoma District 5', 
#             'U.S. House Oklahoma District 5', 'U.S. House Oregon District 2', 'U.S. House Oregon District 2', 'U.S. House Oregon District 5', 'U.S. House Oregon District 5', 'U.S. House Oregon District 5', 'U.S. House Pennsylvania District 1', 'U.S. House Pennsylvania District 1', 'U.S. House Pennsylvania District 1', 'U.S. House Pennsylvania District 9', 
#             'U.S. House Pennsylvania District 9', 'U.S. House Pennsylvania District 9', 'U.S. House Pennsylvania District 10', 'U.S. House Pennsylvania District 10', 'U.S. House Pennsylvania District 11', 'U.S. House Pennsylvania District 11', 'U.S. House Pennsylvania District 11', 'U.S. House Pennsylvania District 13', 'U.S. House Pennsylvania District 13', 
#             'U.S. House Pennsylvania District 13', 'U.S. House Pennsylvania District 14', 'U.S. House Pennsylvania District 14', 'U.S. House Pennsylvania District 15', 'U.S. House Pennsylvania District 15', 'U.S. House Pennsylvania District 15', 'U.S. House Pennsylvania District 16', 'U.S. House Pennsylvania District 16', 'U.S. House South Carolina District 1 Nancy',
#               'U.S. House South Carolina District 1 Nancy', 'U.S. House South Carolina District 2 Joe', 'U.S. House South Carolina District 2 Joe', 'U.S. House South Carolina District 2 Joe', 'U.S. House South Carolina District 3 Jeff', 'U.S. House South Carolina District 3 Jeff', 'U.S. House South Carolina District 4 William', 'U.S. House South Carolina District 4 William',
#                 'U.S. House South Carolina District 4 William', 'U.S. House South Carolina District 5 Ralph', 'U.S. House South Carolina District 5 Ralph', 'U.S. House South Carolina District 7 Russell', 'U.S. House South Carolina District 7 Russell', 'U.S. House South Dakota At-large District Dusty', 'U.S. House South Dakota At-large District Dusty', 
#                 'U.S. House South Dakota At-large District Dusty', 'U.S. House Tennessee District 1', 'U.S. House Tennessee District 1', 'U.S. House Tennessee District 2', 'U.S. House Tennessee District 2', 'U.S. House Tennessee District 2', 'U.S. House Tennessee District 3', 'U.S. House Tennessee District 3', 'U.S. House Tennessee District 4', 'U.S. House Tennessee District 4',
#                   'U.S. House Tennessee District 4', 'U.S. House Tennessee District 5', 'U.S. House Tennessee District 5', 'U.S. House Tennessee District 6', 'U.S. House Tennessee District 6', 'U.S. House Tennessee District 6', 'U.S. House Tennessee District 7', 'U.S. House Tennessee District 7', 'U.S. House Tennessee District 8', 'U.S. House Tennessee District 8',
#                     'U.S. House Tennessee District 8', 'U.S. House Texas District 1', 'U.S. House Texas District 1', 'U.S. House Texas District 1', 'U.S. House Texas District 2', 'U.S. House Texas District 2', 'U.S. House Texas District 3', 'U.S. House Texas District 3', 'U.S. House Texas District 3', 'U.S. House Texas District 4', 'U.S. House Texas District 4',
#                       'U.S. House Texas District 5', 'U.S. House Texas District 5', 'U.S. House Texas District 5', 'U.S. House Texas District 6', 'U.S. House Texas District 6', 'U.S. House Texas District 8', 'U.S. House Texas District 8', 'U.S. House Texas District 10', 'U.S. House Texas District 10', 'U.S. House Texas District 11', 'U.S. House Texas District 11',
#                         'U.S. House Texas District 11', 'U.S. House Texas District 12', 'U.S. House Texas District 12', 'U.S. House Texas District 13', 'U.S. House Texas District 13', 'U.S.', 
#         'House Texas District 13', 'U.S. House Texas District 14', 'U.S. House Texas District 14', 'U.S. House Texas District 15', 'U.S. House Texas District 15', 'U.S. House Texas District 15', 'U.S. House Texas',
#         'District 17', 'U.S. House Texas District 17', 'U.S. House Texas District 17', 'U.S. House Texas District 19', 'U.S. House Texas District 19', 'U.S. House Texas District 19', 'U.S. House Texas District 21', 'U.S. House Texas District 21', 'U.S. House Texas District 21', 'U.S. House Texas District 22', 'U.S. House Texas District 22', 'U.S. House Texas District 23', 
#         'U.S. House Texas District 23', 'U.S. House Texas District 23', 'U.S. House Texas District 24', 'U.S. House Texas District 24', 'U.S. House Texas District 25', 'U.S. House Texas District 25', 'U.S. House Texas District 25', 'U.S. House Texas District 26.', 'U.S. House Texas District 26.', 'U.S. House Texas District 27', 'U.S. House Texas District 27', 
#         'U.S. House Texas District 27', 'U.S. House Texas District 31', 'U.S. House Texas District 31', 
#         'U.S. House Texas District 31', 'U.S. House Texas District 36', 'U.S. House Texas District 36', 'U.S. House Texas District 38', 'U.S. House Texas District 38', 'U.S. House Utah District 1', 'U.S. House Utah District 1', 'U.S. House Utah District 1', 'U.S. House Utah District 2', 'U.S. House Utah District 2', 'U.S. House Utah District 3', 
#         'U.S. House Utah District 3', 'U.S. House Utah District 3', 'U.S. House Utah District 4', 'U.S. House Utah District 4', 'U.S. House Virginia District 1', 'U.S. House Virginia District 1', 'U.S. House Virginia District 1', 'US. House Virginia District 2', 'US. House Virginia District 2', 'U.S. House Virginia District 5', 'U.S. House Virginia District 5', 
#         'U.S. House Virginia District 5', 'U.S. House Virginia District 6', 'U.S. House Virginia District 6', 'U.S. House Virginia District 9', 'U.S. House Virginia District 9', 'U.S. House Virginia District 9', 'U.S. House Washington District 4', 'U.S. House Washington District 4', 'U.S. House Washington District 4', 'U.S. House', 
#         'West Virginia District 1 Carol', 'U.S. House West Virginia District 1 Carol', 'U.S. House West Virginia District 2 Alexander', 'U.S. House West Virginia District 2 Alexander', 'U.S. House West Virginia District 2 Alexander', 'U.S. House Wisconsin District 1', 'U.S. House Wisconsin District 1', 'U.S. House Wisconsin District 3', 
#         'U.S. House Wisconsin District 3', 'U.S. House Wisconsin District 5', 'U.S. House Wisconsin District 5', 'U.S. House Wisconsin District 6', 'U.S. House Wisconsin District 6', 'U.S. House Wisconsin District 6', 'U.S. House Wisconsin District 7', 'U.S. House Wisconsin District 7', 'U.S. House Wisconsin District 8', 'U.S. House Wisconsin District 8',
#           'U.S. House Wisconsin District 8', 'U.S. House Wyoming At-large District', 'U.S. House Wyoming At-large District', 'U.S. Senate Arizona', 'U.S. Senate Arizona', 'U.S. Senate Maine', 'U.S. Senate Maine', 'U.S. Senate Vermont', 'U.S. Senate Vermont', 'U.S. Senate Arizona', 'U.S. Senate Arizona', 'USS. Senate California', 'USS. Senate California',
#             'U.S. Senate California', 'U.S. Senate California', 'U.S. Senate Colorado', 'U.S. Senate Colorado', 'U.S. Senate Colorado', 'U.S. Senate Colorado', 'U.S. Senate Connecticut', 'U.S. Senate Connecticut', 'U.S. Senate Connecticut', 'U.S. Senate Connecticut', 'U.S. Senate Delaware', 'U.S. Senate Delaware', 'U.S. Senate Delaware', 'U.S. Senate Delaware', 
#             'U.S. Senate Georgia', 'U.S. Senate Georgia', 'U.S. Senate Georgia', 'U.S. Senate Georgia', 'U.S. Senate Hawaii', 'U.S. Senate Hawaii', 'U.S. Senate Hawaii', 'U.S. Senate Hawaii', 'USS. Senate Illinois', 'USS. Senate Illinois', 'USS. Senate Illinois', 'USS. Senate Illinois', 'USS. Senate Illinois', 'USS. Senate Illinois', 'U.S. Senate Maryland',
#               'U.S. Senate Maryland', 'U.S. Senate Maryland', 'U.S. Senate Maryland', 'U.S. Senate Massachusetts', 'U.S. Senate Massachusetts', 'U.S. Senate Massachusetts', 'U.S. Senate Massachusetts', 'U.S. Senate Michigan', 'U.S. Senate Michigan', 'U.S. Senate Michigan', 'U.S. Senate Michigan', 'U.S. Senate Minnesota', 'U.S. Senate Minnesota', 'U.S. Senate Minnesota',
#                 'U.S. Senate Minnesota', 'U.S. Senate Mississippi', 'U.S. Senate Mississippi', 'U.S. Senate Montana', 'U.S. Senate Montana', 'U.S. Senate Nevada', 'U.S. Senate Nevada', 'U.S. Senate Nevada', 'U.S. Senate Nevada', 'U.S. Senate New Hampshire', 'U.S. Senate New Hampshire', 'U.S. Senate New Hampshire', 'U.S. Senate New Hampshire', 'U.S. Senate New Jersey',
#                   'U.S. Senate New Jersey', 'U.S. Senate New Jersey', 'U.S. Senate New Jersey', 'U.S. Senate New Mexico', 'U.S. Senate New Mexico', 'U.S. Senate New Mexico', 'U.S. Senate New Mexico', 'U.S. Senate New York', 'U.S. Senate New York', 'U.S. Senate New York', 'U.S. Senate New York', 'U.S. Senate Ohio', 'U.S. Senate Ohio', 'U.S. Senate Oregon', 'U.S. Senate Oregon',
#                     'U.S. Senate Oregon', 'U.S. Senate Oregon', 'U.S. Senate Pennsylvania', 'U.S. Senate Pennsylvania', 'U.S. Senate Pennsylvania', 'U.S. Senate Pennsylvania', 'U.S. Senate Rhode Island', 'U.S. Senate Rhode Island', 'U.S. Senate Rhode Island', 'U.S. Senate Rhode Island', 'U.S. Senate Vermont', 'U.S. Senate Vermont', 'U.S. Senate Virginia', 'U.S. Senate Virginia',
#                       'U.S. Senate Virginia', 'U.S. Senate Virginia', 'U.S. Senate Washington', 'U.S. Senate Washington', 'U.S. Senate Washington', 'U.S. Senate Washington', 'US. Senate West Virginia', 'US. Senate West Virginia', 'U.S. Senate West Virginia', 'U.S. Senate West Virginia', 'U.S. Senate Wisconsin', 'U.S. Senate Wisconsin', 'U.S. Senate Wisconsin', 'U.S. Senate Wisconsin', 'U.S. Senate Wyoming', 'U.S. Senate Wyoming']

# under_states, no_under_states, _, _ = return_states_list_and_stage_groups_urls(split_states=True)
# all_states = []
# seen_state = []
# under_state_ct = 0
# for lal in list_:
#     for state in no_under_states:
#         state = state.strip()
#         if state not in all_states:
#             all_states.append(state)
#         if state in lal:
#             if state not in seen_state:
#                 seen_state.append(state)
#     for state in under_states:
#         state = state.replace("_"," ")
#         state = state.strip()
#         if state not in all_states:
#             all_states.append(state)
#         if state in lal:
#             print("under state here:",state)
#             under_state_ct+=1
#             if state not in seen_state:
#                 seen_state.append(state)

# # print("comparing lengths of seen and all 50 states:",((len(seen_state),len(all_states))))

# for state in all_states:
#     if state not in seen_state:
#         print(state)
# print("under_state_ct",under_state_ct)


"""
U.S. House Maryland District 2 Dutch Ruppersberger

U.S. House Maryland District 3 John Sarbanes

U.S. House Maryland District 4 Glenn Ivey

U.S. House Maryland District 5 Steny Hoyer

U.S. House Maryland District 6 David Trone

U.S. House Maryland District 7 Kweisi Mfume

U.S. House Maryland District 8 Jamie Raskin
"""

i = "U.S. House Maryland District 8 Jamie Raskin "

pass_by = False
failed = False
if pass_by == False:
    if "Indepen" in i:
        pass_by = True
        the_party = "Indepen"
if pass_by == False:
    if "Republi" in i:
        the_party = "Republi"
        pass_by = True
if pass_by == False:
    if "Republi" not in i:
        if "Indepen" not in i:
            the_party = "assume democratic"
            pass_by = True
text_list = i.split(" ")
under_states, no_under_states, _,_ = return_states_list_and_stage_groups_urls(split_states=True)
fin_party = ""
# house_len = 1
for state in no_under_states:
    state = state.strip()
    if state in i:
        house_len = 5
        if "House Maryland" in i:
            print((i,the_party," ".join(text_list[0:house_len])))
        pol_test = " ".join(text_list[0:house_len])
        if pol_test[-1].isnumeric() == True:
            house_len = 5
            break
        if pol_test[-1].isnumeric() == False:
            house_len = 6
            break
for state in under_states:
    state = state.replace("_"," ")
    # state = state.strip()
    if state in i:
        if "At-Large" in i:
            house_len = 7
        if "At-Large" not in i:
            house_len = 6
if house_len == 1:
    print("house len == 1:"," ".join(text_list))
if house_len != 1:
    fin_party = ""
    pol = " ".join(text_list[0:house_len])
    name = text_list[house_len:]
    if the_party in ["Indepen","Republi"]:
        name = " ".join(name)
        if the_party == "Indepen":
            fin_party = "Independent"
        if the_party == "Republi":
            fin_party = "Republican party"
    else:
        name = " ".join(name)
        fin_party = "Democratic Party"
if type(name) == type([]):
    failed = True
    print("darnit")
if failed == False:
    # if name not in check_list:
    #     print(name)
    legist_dict = {
        "legistlator":name,
        "political_office":pol,
        "party":fin_party
                    }
# print((name,fin_party,pol))
print(legist_dict)