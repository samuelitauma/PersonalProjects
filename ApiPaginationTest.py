import json
import requests
import csv

#Setting/Creating a class as this will be easier to read
class Players:

    #This is the function which will store all the important data/variables
    def __init__(self):
        #URL and headers to access the API data
        self.url = "https://api-football-v1.p.rapidapi.com/v3/players?league=39&season=2020"
        self.headers = {
            "X-RapidAPI-Key": "{INSERT API KEY HERE}",
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        
        #Creating a list to hold all player info
        self.all_players_data = []  
        
        #Using TRY / EXCEPTION method to test the API
        try:
            response = requests.get(self.url,headers=self.headers) #Format replaces season with its actual variable
            #print(self.url, headers=self.headers)
        except Exception as e:
            print(e)
            print('Error with collecting first URL')
        else:
            if response.status_code == 200:
                self.data = response.json()
            # This is where you collect your data from (First Page) and store it in all_players_data
                #self.all_players_data += self.data['response']
              
    
    # Getting Data from other pages
    def Paging(self):
        #Getting page Intergers
        current_page = self.data['paging']['current']
        total_pages = self.data['paging']['total']
        
        #Creating a formula cyclethrough the pages and collect data from every page
        while current_page < total_pages:
            # Checking pages until current page = total page
            current_page += 1
            next_url = self.url+ f"&page={current_page}"
            print(next_url)
            #Using TRY / EXCEPTION again as this is a new url
            try:
                response = requests.get(next_url, headers=self.headers) #Next Url = New/Next pages specific url
            except Exception as e:
                print(e)
                print('Error with getting data from other pages')
            else:
                if response.status_code == 200:
                    self.data = response.json()
                    # Putting all the data into the list for it to be processed below
                    self.all_players_data += self.data['response']
        
        print('Paging Completed')
        #Code to start Saving() function
        #self.SavingASjson()
        
    
    def SavingASjson(self):
        with open('lambdaTEST2.json', mode='w') as f:
            
            f.write('{' + '\n')
            try:    
                for asd in self.all_players_data:
                    n = asd['player']['name']
                    t = asd['statistics'][0]['team']['name']
                    

                    f.write( '  ' + '"Player"' + ':' + '"' + n + '"'+ ',' + '"Team"' + ':' + '"'+ t + '"' + ',' + '\n' )
            except Exception as e:
                print(e)
                print('ERROR SAVING')
            else:
                f.write('}')
                print('json file saved')
            
            
            
    
    #Function to collect + proccess + save as a CSV file
    def Saving(self):
        
        #Opening a CSV file and writing in content
        with open("PLAYERS IN EPL " + season + '.csv', mode='a', newline='') as f:
            
            writer = csv.writer(f)
            try:
                #Testing to see if there is content already in side
                if f.tell() == 0:
                    #Writing headers
                    #writer.writerow(['Player Name', 'Team Name', 'Position', 'Nationality', 'Appearences'])
                
                    #Collecting all of the data and sorting it to assigned variable
                    for player_data in self.all_players_data:
                        player_name = player_data['player']['name']
                        team_name = player_data['statistics'][0]['team']['name']
                        #position = player_data['statistics'][0]['games']['position']
                        #nationality = player_data['player']['nationality']
                        #appearences = player_data['statistics'][0]['games']['appearences']
                        #Writing the content
                        #writer.writerow([player_name, team_name, position, nationality, appearences])
                        writer.writerow([player_name, team_name])
            except Exception as e:
                #Checking for errors
                print(e)
                print('Error saving as a csv file')
            else:
                print('File Saved')

    def Select_one_page(self):
        #Getting page Intergers
        print('trying to select one page')
        select_page = 4
        
        next_url = self.url+ f"&page={select_page}"
        print(next_url)
        #Using TRY / EXCEPTION again as this is a new url
        try:
            response = requests.get(next_url, headers=self.headers) #Next Url = New/Next pages specific url
        except Exception as e:
            print(e)
            print('Error with getting data from other pages')
        else:  
            if response.status_code == 200:
                self.data = response.json()
                # Putting all the data into the list for it to be processed below
                self.all_players_data += self.data['response']
            
        for asd in self.all_players_data:
            n = asd['player']['name']
            t = asd['statistics'][0]['team']['name']

            print(n + ' , ' + t)


CODE = Players()
#CODE.Paging()
CODE.Select_one_page()





