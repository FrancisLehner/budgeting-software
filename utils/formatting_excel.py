import pandas as pd
from datetime import datetime as dt
import os
import re

from dotenv import load_dotenv

load_dotenv()
directory = os.getenv('directory')
os.chdir(directory)

def convert_to_csv(dataframe):    
    old_df = pd.read_excel(dataframe)
    old_df.to_csv('Budget_Test.csv', index=False)

    new_df = pd.read_csv('Budget_Test.csv')
    return new_df


def format_old_dataframe(dataframe):
    new_df = convert_to_csv(dataframe)

    new_df = new_df.reset_index(drop=True)

    #Removing Unnecessary Rows and Columns
    new_df = new_df.dropna(how='all', axis=1)
    new_df = new_df.dropna(thresh = len(new_df.columns) - 2, axis=0, ignore_index=True)

    columns_to_drop = new_df.columns[new_df.columns.str.contains(r'Unnamed: \d+$', regex=True)]
    new_df = new_df.drop(columns=columns_to_drop)
    new_df = new_df.drop(columns='Price Rupiah')
    new_df = new_df.drop(columns='Price AED')

    # Format Dates
    for i, date in enumerate(new_df['Date']):
        date = date.replace('/', '-')
        date = dt.strptime(date, '%Y-%m-%d').date()
        date = date.strftime('%d-%m-%Y')
        date = new_df.at[i, 'Date']

    # Adding new columns
    new_df.insert(2, 'Description', 'None', False)
    new_df.insert(3, 'Category', 'None', False)


    # Sorting Purchase Names into Description and Category
    categories = ['Shopping', 'Leisure', 'Food', 'Groceries', 'Transport', 'ATM', 'Fashion']
    description_list_words = []
    category_list_words = []
    
    for purchase in new_df['Purchase']:
        purchase = str(purchase)
        description = re.findall(r'\(([^)]+)\)', purchase)
        if description:
            description_list_words.append(description[0])
            category_found = False
            for category in categories:
                if category in purchase:
                    category_list_words.append(category)
                    category_found = True
                    break
            if not category_found:
                if 'Gojek' in purchase:
                    category_list_words.append('Transport')
                elif 'ATM' in purchase:
                    category_list_words.append('ATM')
                elif 'Food' in purchase:
                    category_list_words.append('Food')
                else:
                    category_list_words.append('Other')

        else:
            if 'Gojek' in purchase:
                description_list_words.append('None')
                category_list_words.append('Transport')
            elif 'ATM' in purchase:
                description_list_words.append('None')
                category_list_words.append('ATM')
            elif 'Food' in purchase:
                description_list_words.append('None')
                category_list_words.append('Food')
            else:
                description_list_words.append('None')
                category_list_words.append('Other')


    new_df['Description'] = description_list_words
    new_df['Category'] = category_list_words

    new_df.to_csv('Budget_Test_F.csv', index=False)
    print(new_df)

format_old_dataframe('Budget_Test.xlsx')

