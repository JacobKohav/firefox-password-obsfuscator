from IPython.display import display
import pandas as pd
import numpy as np
from tabulate import tabulate
from datetime import datetime
from datetime import date
import sys

# Modify display options for native Pandas display
pd.set_option('display.max_columns', 5)
pd.options.display.max_rows = 5
pd.set_option("expand_frame_repr", False)
pd.set_option("max_colwidth", 40)
pd.set_option("colheader_justify", "center")
# pd.set_option("large_repr", "truncate")

# No warning on new column
pd.options.mode.chained_assignment = None  # default='warn'

def import_credentials (credentials_file_str, credentials_df):
    print ("\nParsing credentials file...")

    open_credentials = open(credentials_file_str)
    credentials_df = pd.read_csv(credentials_file_str)
    credentials_df.reset_index(inplace=True) # Add indices
    return (credentials_df)

def reformat_credentials (credentials_df):
    print ("Reformatting...")

    # --Remove uncessesary columns--
    # Reformat via columns droppping
    # credentials_df = credentials_df.drop (columns=['httpRealm', 'guid', 'timeCreated', 'timeLastUsed', 'timePasswordChanged'])
    # Reformat via columns selection
    credentials_df = credentials_df [['url', 'username', 'password']]

    # --Add resource name column; remove irrelevant URL data
    # Remove "http(s)://"
    credentials_df['resource'] = credentials_df['url'].str.replace(r"http[a-z]*://", '', regex=True)
    # Remove "www."
    credentials_df['resource'] = credentials_df['resource'].str.replace(r"www.", '', regex=True)
    # Remove ".com", ".org", etc.
    credentials_df['resource'] = credentials_df['resource'].str.replace(r"\.[a-z]{2,3}$", '', regex=True)
    # Remove miscellaneous additions
    credentials_df['resource'] = credentials_df['resource'].str.replace(r"account[s]*.", '', regex=True)
    credentials_df['resource'] = credentials_df['resource'].str.replace(r"my.", '', regex=True)
    credentials_df['resource'] = credentials_df['resource'].str.replace(r"sso.", '', regex=True)
    credentials_df['resource'] = credentials_df['resource'].str.replace(r"signin.", '', regex=True)
    credentials_df['resource'] = credentials_df['resource'].str.replace(r"digital.", '', regex=True)
    credentials_df['resource'] = credentials_df['resource'].str.replace(r"shop.", '', regex=True)
    credentials_df['resource'] = credentials_df['resource'].str.replace(r"login[-us]*.", '', regex=True)

    # Capitalize resource name
    # credentials_df['resource'] = credentials_df['resource'].str.capitalize()
    credentials_df['resource'] = credentials_df['resource'].str.title()

    # Reoder/rename columns
    credentials_df = credentials_df [['resource', 'url', 'username', 'password']]
    credentials_df = credentials_df.set_axis(['resource', 'domain', 'username', 'password'], axis=1)

    # Alphabetize by resource name
    credentials_df = credentials_df.sort_values('resource')
    
    return (credentials_df)

def obsfuscate_username (credentials_df, names):
    print ("Obsfuscating usernames...")

    credentials_df['username'] = credentials_df['username'].str.replace(r"([a-z]{2})[a-z, .]*([a-z]{2})([@][a-z]{2})[a-z]*([a-z])", r'\1.. ..\2\3..\4', regex=True)
    credentials_df['username'] = credentials_df['username'].str.replace(r"([a-z]{1})[a-z, .]*([a-z]{1}[0-9]{1})[0-9]*([0-9]{1}[@][a-z]{2})[a-z]*([a-z])", r'\1..\2..\3..\4', regex=True)

    return (credentials_df)

def obsfuscate_credentials (credentials_df):
    print ("Obsfuscating credentials...")

    # Letter characters
    credentials_df['password'] = credentials_df['password'].str.replace(r"([A-Z,a-z]{3})[A-Z,a-z]{3}([A-Z,a-z]{1})[A-Z,a-z]*([A-Z,a-z]{2})", r'\1...\2...\3', regex=True) # 9 letters
    credentials_df['password'] = credentials_df['password'].str.replace(r"([A-Z,a-z]{3})[A-Z,a-z]{2}([A-Z,a-z]{1})[A-Z,a-z]*([A-Z,a-z]{2})", r'\1...\2...\3', regex=True) # 8 letters
    credentials_df['password'] = credentials_df['password'].str.replace(r"([A-Z,a-z]{3})[A-Z,a-z]{1}([A-Z,a-z]{1})[A-Z,a-z]*([A-Z,a-z]{2})", r'\1...\2...\3', regex=True) # 7 letters
    credentials_df['password'] = credentials_df['password'].str.replace(r"([A-Z,a-z]{2})[A-Z,a-z]{1,2}[A-Z,a-z]*([A-Z,a-z]{2})", r'\1...  ...\2', regex=True) # 5 - 6 letters

    # Numerical characters
    credentials_df['password'] = credentials_df['password'].str.replace(r"([0-9]{1})[0-9]{1,3}([0-9]{1})", r'\1..\2', regex=True) # 5 - 6 letters

    return (credentials_df)

def export_credentials (credentials_df):
    print ("Exporting to .csv...")

    #TODO add 
    identifier = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
    credentials_df.to_csv(f'creds_obfuscated_{identifier}.csv', index=True)  

    print (f"Exported `creds_obfuscated_{identifier}.csv`\n")

def testingfunction():
    import re
    # repl = lambda m: m.group(0)[::-1]

    inp = '653433,78'
    inp2 = 'Jampura_8036'
    # ser = pd.Series(['foo 123', 'bar baz', np.nan])
    print ("\nOriginal: " )
    display(inp2)

    # ser = ser.str.replace(r'[a-z]+', repl, regex=True)
    out = re.sub(r'([0-9]{6}),([0-9]{2})', r'\1.\2', inp)
    out2 = re.sub(r'([A-Z][a-z])', r'\1___', inp2)
    out2 = inp2.replace(r'([A-Z][a-z])', '')

    # [A-Z][a-z]*[!, ?][0-9]*

    print ("\nChanged: ")
    # return (ser)
    return (out2)

# def main(credentials_file_str):
def main(): 
    args = sys.argv[1:]

    # Request name to obfuscaste optimally
    # name_first = input ("What is your FIRST name? ")
    # name_last = input ("What is your LAST name? ")

    credentials_df = pd.DataFrame()
    credentials_df = import_credentials (args[0], credentials_df)
    credentials_df = reformat_credentials (credentials_df)
    # credentials_df = obsfuscate_username (credentials_df, [name_first, name_last])
    credentials_df = obsfuscate_username (credentials_df, [None, None])
    credentials_df = obsfuscate_credentials (credentials_df)

    # Print table (use Tabulate library for formatting)
    print("\n", tabulate(credentials_df, showindex=True, tablefmt = "github", headers=credentials_df.columns), "\n")
    # display (credentials_df)

    export_credentials (credentials_df)

# main("passwords.csv")
main()
