import os

import pandas as pd

from cultheld.configuration.configuration import configuration_venues

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

def main():
    df_venues = []
    for config in configuration_venues:
        df = config.function()
        df = ouput_venue(df, config.ID)
        df_venues.append(df)
    
    output_df = pd.concat(df_venues, ignore_index=True)
    output_df = output_df[['venue', 'type', 'start_date_time', 'title', 'price', 'ticket_url']].reset_index()

    output_df.to_csv(ROOT_DIR + '/../output/combined_venues.csv', encoding='utf-8')


def ouput_venue(df, ID):
    df = df[['start_date_time', 'title', 'price', 'ticket_url']].reset_index()

    for config in configuration_venues:
        if config.ID == ID:
            df['type'] = config.type
            df['venue'] = config.venue
            df.to_csv(config.output_folder, encoding='utf-8')

    return df


main()
