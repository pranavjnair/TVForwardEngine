from VarietyScraper import run_variety_scraper
from typing import Dict
from configparser import ConfigParser
import psycopg2
import psycopg2.extras as psql_extras
import pandas as pd
from typing import Dict


def load_connection_info(
        ini_filename: str
) -> Dict[str, str]:
    parser = ConfigParser()
    parser.read(ini_filename)
    # Create a dictionary of the variables stored under the "postgresql" section of the .ini
    conn_info = {param[0]: param[1] for param in parser.items("postgresql")}
    return conn_info

def insert_data(
        query: str,
        conn: psycopg2.extensions.connection,
        cur: psycopg2.extensions.cursor,
        df: pd.DataFrame,
        page_size: int
) -> None:
    data_tuples = [tuple(row.to_numpy()) for index, row in df.iterrows()]

    try:
        psql_extras.execute_values(
            cur, query, data_tuples, page_size=page_size)
        print("Query:", cur.query)

    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        print("Query:", cur.query)
        conn.rollback()
        cur.close()

    else:
        conn.commit()


if __name__ == "__main__":
    # host, database, user, password
    connection = psycopg2.connect(dbname="postgres", user="", password="")
    cursor = connection.cursor()

    # Insert data into the variety table
    house_df = pd.DataFrame({
        "title": ["‘The Walking Dead’ Series Finale", "Top Entertainment Franchises", "Len Goodman to Exit ‘Dancing With the Stars’"],
        "link": ["https://variety.com/2022/tv/reviews/the-walking-dead-series-finale-review-closure-anticlimactic-1235438189/","https://variety.com/2022/tv/news/walking-dead-series-finale-commercials-tv-advertising-characters-1235438320/","https://variety.com/2022/tv/news/yellowstone-recap-season-5-episode-3-1235436302/"],
        "date": ["2022-11-20","2022-11-20","2022-11-20"]
    })
    insert_query = "INSERT INTO variety(title, link, date) VALUES %s"
    insert_data(insert_query, connection, cursor, house_df, 100)

    # Close all connections to the database
    connection.close()
    cursor.close()
