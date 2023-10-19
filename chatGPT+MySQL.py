import os
import openai
import logging
import json
import pymysql
from io import StringIO
import csv
import logging

#Openai Key
api_key = '{INSERT API KEY HERE}'
openai_api_key = api_key
openai_model = "gpt-3.5-turbo"

#Configuration
#Table
EngPLFixtures_fact = 'EngPLFixtures_fact, fixture_id, int\nEngPLFixtures_fact, league_id, int\nEngPLFixtures_fact, status, nvarchar\nEngPLFixtures_fact, referee, nvarchar\nEngPLFixtures_fact, fixture_date, datetime\nEngPLFixtures_fact, season, int\nEngPLFixtures_fact, home_id, int\nEngPLFixtures_fact, home_name, nvarchar\nEngPLFixtures_fact, home_result, nvarchar\nEngPLFixtures_fact, away_id, int\nEngPLFixtures_fact, away_name, nvarchar\nEngPLFixtures_fact, away_result, nvarchar\nEngPLFixtures_fact, FT_home_goals, int\nEngPLFixtures_fact, FT_away_goals, int\nEngPLFixtures_fact, Ht_home_goals, int\nEngPLFixtures_fact,HT_away_goals, int\nEngPLFixtures_fact, date_added, datetime'
FixtureOdds_fact = 'FixtureOdds_fact, fixture_id, int\nFixtureOdds_fact, league_id, int\nFixtureOdds_fact, season, int\nFixtureOdds_fact, bookie_name, nvarchar\nFixtureOdds_fact, home0V1_5,decimal\nFixtureOdds_fact, home0V2_5, decimal\nFixtureOdds_fact, away0V1_5, decimal\nFixtureOdds_fact, away0V2_5, decimal\nFixtureOdds_fact, BTTS_yes, decimal\nFixtureOdds_fact, BTTS_no, decimal\nFixtureOdds_fact, date_added, datetime'
FixtureStats_fact = 'FixtureStats_fact,fixture_id,int\nFixtureStats_fact,team_id,int\nFixtureStats_fact,team_name,nvarchar\nFixtureStats_fact,shots_on_goal,int\nFixtureStats_fact,shots_off_goal,int\nFixtureStats_fact,total_shots,int\nFixtureStats_fact,blocked_shots,int\nFixtureStats_fact,shots_insidebox,int\nFixtureStats_fact,shots_outsidebox,int\nFixtureStats_fact,fouls,int\nFixtureStats_fact,corner_kicks,int\nFixtureStats_fact,offsides,int\nFixtureStats_fact,possession_percent,int\nFixtureStats_fact,yellow_cards,int\nFixtureStats_fact,red_cards,int\nFixtureStats_fact,GK_saves,int\nFixtureStats_fact,total_passes,int\nFixtureStats_fact,accurate_passes,int\nFixtureStats_fact,passes_percent,int\nFixtureStats_fact,date_added,datetime'
BettingMarket_dim = 'BettingMarket_dim, market_id, int\nBettingMarket_dim, market_name, nvarchar'
Bookmakers_dim = 'Bookmakers_dim, bookie_id, int\nBookmakers_dim,bookie_name,nvarchar'
FEMALE = 'FEMALE, gender, nvarchar\nFEMALE, id, int'
MALE = 'MALE, gender, nvarchar\nMALE, id, int'
ModelOdds_fact = 'ModelOdds_fact, fixture_id, int\nModelOdds_fact, fixture, nvarchar\nModelOdds_fact, bookie_name, nvarchar\nModelOdds_fact, home0V1_5, int\nModelOdds_fact, home0V2_5, int\nModelOdds_fact, away0V1_5, int\nModelOdds_fact, awaya0V2_5, int\nModelOdds_fact, BTTS_yes, int\nModelOdds_fact, BTTS_no, int\nModelOdds_fact, date_added, datetime'
Teams_dim = 'Teams_dim, team_id, int\n Teams_dim, team_name, nvarchar'



#Code to process the message asked in chatGPT
class ChatGPT:

    startMessageStack = [
        {"role": "system", "content": "You act as the middleman between USER and a DATABASE. Your main goal is to answer questions based on data in a mySQL Server database (SERVER). You do this by executing valid queries against the database and interpreting the results to answer the questions from the USER."},
        {"role": "user", "content": "From now you will only ever respond with JSON. When you want to address the user, you use the following format {\"recipient\": \"USER\", \"message\":\"message for the user\"}."},
        {"role": "assistant", "content": "{\"recipient\": \"USER\", \"message\":\"I understand.\"}."},
        {"role": "user", "content": "You can address the SQL Server by using the SERVER recipient. When calling the server, you must also specify an action. The action can be QUERY when you want to QUERY the database, or SCHEMA when you need SCHEMA information for a comma separated list of tables. The format you will use for requesting schema information is as follows {\"recipient\":\"SERVER\", \"action\":\"SCHEMA\", \"message\":\"EngPLFixtures_fact, FixtureODDs_fact\"}. The format you will use for executing a query is as follows: {\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"SELECT * FROM EngPLFixtures_fact;\"}"},
        # At some point the list of tables should become dynamic. Todo: Figure out how the flows can be dynamic, perhaps some sort of config.
        {"role": "user", "content": "THe following tables are available in the database: BettingMarket_dim, Bookmakers_dim, EngPLFixtures_fact, FEMALE, FixtureODDs_fact, FixtureStats_fact, Leagues_dim, MALE, ModelOdds_fact, Teams_dim. You will always first request the SCHEMA for a table before using the table in a QUERY."},
        {"role": "user", "content": "Let's start! What was the home result when Arsenal played home against Everton in 2021?"},
        {"role": "assistant", "content": "{\"recipient\":\"SERVER\", \"action\":\"SCHEMA\", \"message\":\"EngPLFixtures_fact\"}"},
        {"role": "user", "content": f"Table, Column, DataType\n{EngPLFixtures_fact}"},
        {"role": "assistant", "content": "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"SELECT home_result FROM EngPLFixtures_fact where home_name = 'Arsenal' and away_name = 'Everton' and season = 2021\"}"},
        {"role": "user", "content": "home_result\nW"},
        {"role": "assistant", "content": "{\"recipient\": \"USER\", \"message\":\"Arsenal W at home against Everton in 2021\"}."},
        {"role": "user", "content": "Great Thank you,next question: How many goals did Fulham score when they played Crystal Palace at home in 2018?"},
        {"role": "assistant", "content": "{\"recipient\":\"SERVER\", \"action\":\"SCHEMA\", \"message\":\"EngPLFixtures_fact\"}"},
        {"role": "user", "content": f"Table, Column, DataType\n{EngPLFixtures_fact}"},
        {"role": "assistant", "content": "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"SELECT FT_home_goals FROM EngPLFixtures_fact where home_name = 'Fulham' and away_name = 'Crystal Palace' and season = 2018\"}"},
        {"role": "user", "content": "FT_home_goals\n0"},
        {"role": "assistant", "content": "{\"recipient\": \"USER\", \"message\":\"Fulham scored 0 goals when they played Crystal Palace at home in 2018\"}."},
        {"role": "user", "content": "excellent, thank you! Now the next question. What were the odds for both teams to score (BTTS_yes) when Arsenal played Everton at home in 2021?"},
        {"role": "assistant", "content": "{\"recipient\":\"SERVER\", \"action\":\"SCHEMA\", \"message\":\"EngPLFixtures_fact, FixtureOdds_fact\"}"},
        {"role": "user", "content": f"Table, Column, DataType\n{EngPLFixtures_fact}\n{FixtureOdds_fact}"},
        {"role": "assistant", "content": "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"select FixtureOdds_fact.bookie_name,FixtureOdds_fact.BTTS_yes from EngPLFixtures_fact join FixtureOdds_fact on EngPLFixtures_fact.fixture_id = FixtureOdds_fact.fixture_id where EngPLFixtures_fact.home_name = 'Arsenal'and EngPLFixtures_fact.away_name = 'Everton';'\"}"},
        {"role": "user", "content": "EngPLFixtures_fact.home_name = 'Arsenal'\nEngPLFixtures_fact.away_name = 'Everton'\nFixtureOdds_fact.bookie_name = '888Sport' + 'Bet365' + 'Betway' + 'William Hill'\nFixtureOdds_fact.BTTS_yes = 1.79 + 1.80 + 1.85 + 1.85"},
        {"role": "assistant", "content": "{\"recipient\": \"USER\", \"message\":\"The Odds for both teams to score (BTTS) when Arsenl played Everton at home in 2021 where: 1.79 at 888Sport, 1.80 at Bet365, 1.85 at Betway and 1.85 at William Hill\"}."},
        {"role": "user", "content": "excellent, thank you! Now the next question. What were the Goals scored,shots on target and shots off-target for both teams when Manchester United played at home to Leicester in 2018?"},
        {"role": "assistant", "content": "{\"recipient\":\"SERVER\", \"action\":\"SCHEMA\", \"message\":\"EngPLFixtures_fact, FixtureStats_fact\"}"},
        {"role": "user", "content": f"Table, Column, DataType\n{EngPLFixtures_fact}\n{FixtureStats_fact}"},
        {"role": "assistant", "content": "{\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"select FixtureStats_fact.team_name,EngPLFixtures_fact.home_name,EngPLFixtures_fact.away_name,FixtureStats_fact.shots_on_goal,FixtureStats_fact.shots_off_goal,EngPLFixtures_fact.FT_home_goals,EngPLFixtures_fact.FT_away_goals FROM FixtureStats_fact join EngPLFixtures_fact on FixtureStats_fact.fixture_id = EngPLFixtures_fact.fixture_id where EngPLFixtures_fact.home_name = 'Manchester United' and EngPLFixtures_fact.away_name = 'Leicester' and EngPLFixtures_fact.season=2018;'\"}"},
        {"role": "user", "content": "FixtureStats_fact.team_name = 'Manchester United' + 'Leicester'\nEngPLFixtures_fact.home_name = 'Manchester United' + 'Manchester United'\nEngPLFixtures_fact.away_name = 'Leicester' + 'Leicester'\nFixtureStats_fact.shots_on_goal = 6 + 4\nFixtureStats_fact.shots_off_goal = 1 + 3\nFixtureStats_fact.FT_home_goals = 2 + 2\nFixtureStats_fact.FT_away_goals = 1 + 1"},
        {"role": "assistant", "content": "{\"recipient\": \"USER\", \"message\":\"The total Goals scored,total shots on target and total shots off-target for both teams are Manchester United = 2:6:1 while Leicester = 1:4:3\"}."}
        ]

    def __init__(self, api_key, model = "gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model
        self.messages = self.startMessageStack.copy()

    def message(self, message, sender):
        logging.debug(message)
        if (sender):
            message = json.dumps({'message':message, 'sender':sender})
        self.messages.append({"role": "user", "content": message})
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        response = completion.choices[0].message.content 
        logging.debug(response)
        self.messages.append({"role": "assistant", "content": response})
        return response

    def reset(self):
        self.messages = self.startMessageStack.copy()
        print('model was reset to intial state')

# Code to connect and query database
class mySQL_DB:

    def __init__(self):      '{Fill out connection details}'
        self.host = ""
        self.user=""
        self.password=""
        self.database=""
        self.connection = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)


    def connect(self):
        try:
            self.connection
            return True
        except Exception as e:
            return str(e)

    def close(self):
        self.connection.close()

    def execute_query(self, query):
        print(f'\033[94mExecuting Query:{query}\033[0m')
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                result = "0 rows returned"
                logging.debug(result)
                print(f'\033[96m{result}\033[0m')
                return result

            headers = [column[0] for column in cursor.description]
            output = StringIO()
            csv_writer = csv.writer(output)
            csv_writer.writerow(headers)
            csv_writer.writerows(result)
            result = output.getvalue()
            logging.debug(result)
            print(f'\033[96m{result}\033[0m')
            return result
        except Exception as e:
            print('Trying Query -------')
            return str(e)

    def process_table_string(self, input_str):
        items = input_str.split(',')
        items = [item.split('.')[-1] for item in items]
        formatted_str = "', '".join(items)
        result = f"'{formatted_str}'"
        return result

    def execute_schema(self, table_list):
        queryPart = self.process_table_string(table_list)
        return f"SELECT CONCAT(TABLE_SCHEMA, '.', TABLE_NAME, ', ', COLUMN_NAME, ', ', DATA_TYPE) AS 'Table, Column, DataType' FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ({queryPart})"

class Controller:

    def __init__(self):
        # initialise all the things
        self.SQL = mySQL_DB()
        self.SQL.connect()
        self.chatModel = ChatGPT(openai_api_key,openai_model)

    def run(self, message, sender):
        responseString = self.chatModel.message(message, sender)
        try:
            response = json.loads(responseString[:-1] if responseString.endswith('.') else responseString)
        except ValueError:
            return self.run("Please repeat that answer but use valid JSON only.", "SYSTEM")
        match response["recipient"]:
            case "USER": 
                return response["message"]
            case "SERVER":
                match response["action"]:
                    case "QUERY":
                        result = self.SQL.execute_query(response["message"])  #Using Execute function from mySQL_DB
                        return self.run(result, None)
                    case "SCHEMA":
                        result = self.SQL.execute_schema(response["message"])   #could be execute_schema
                        return self.run(result, None)
                    case _:
                        print('error invalid action')
                        print(response)
            case _:
                print('error, invalid recipient')
                print(response)


    def reset(self):
        self.chatModel.reset()

# Configure the logging settings
logging.basicConfig(filename='debug.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("Ask any question about the data. Enter 'q' to quit. Enter 'r' to reset ChatGPT.")
    controller = Controller()
    while True:
        user_input = input("Question: ")
        if user_input.lower() == 'q':
            break
        if user_input == "r":
            controller.chatModel.reset()
            continue
        try:
            result = controller.run(message=user_input, sender="USER")
            print(f"ChatGPT: {result}")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

if __name__ == "__main__":
    main()