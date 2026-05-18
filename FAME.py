from random import randint, sample
from copy import deepcopy
import json

#Parameters used by the program
NB_PLAYERS = 128
NB_MAPS = 16
TEAM_SIZE = 4
NB_TEAMS = NB_PLAYERS // TEAM_SIZE

#Class representing a player
class Player :
    
    def __init__(self, name, seed, map_seeds, timezone) :
        self.name = name
        self.seed = seed
        self.map_seeds = map_seeds
        self.timezone = timezone

#Class representing a team (stores the list of players)
#Team.metric is the metric used by the balancing algorithm ; the metric is always positive and a metric of 0.0 is a perfectly balanced team (higher metric => less balanced)
#Team.metric can be any function with the team as its only argument satisfying the above conditions
class Team :
    
    def __init__(self, players) :
        self.players = players

    def sort_players(self) :
        self.players = sorted(self.players, key = lambda player : player.seed)

    #This metric uses two values in equal proportions
    #Sum of the squares of the differences between the sum of seeds and the mean seeding value
    #Square of the difference between the sum of seeds on every map and the mean seeding value
    def team_seed_and_mean_distance(self) :
        distance = 0
        mean = NB_PLAYERS * (NB_PLAYERS - 1) / 2 / NB_TEAMS
        seed_total = 0
        for i in range(NB_MAPS) :
            seed_total_map = 0
            for player in self.players :
                seed_total_map += player.map_seeds[i]
            distance += (seed_total_map - mean) ** 2
            seed_total += seed_total_map
        distance += (seed_total - mean * NB_MAPS) ** 2 * NB_MAPS
        return distance
    
    metric = team_seed_and_mean_distance

#Parses the qualifier results file into data usable by this prgram
def open_qualifiers_file() :
    players = []
    with open("qualifiers.json", encoding = 'utf-8') as file :
        data = json.load(file)
        for player in data["Players"] :
            name = player["Name"]
            seed = player["Seed"]
            map_seeds = player["Map seeds"]
            timezone = player["Time zone"]
            players.append(Player(name, seed, map_seeds, timezone))
    return players

#Create teams based off player seedings
def create_teams(players) :
    teams = [[] for i in range(NB_TEAMS)]
    for i in range(TEAM_SIZE) :
        for j in range(NB_TEAMS) :
            index = j if i%2 == 0 else NB_TEAMS - j - 1
            teams[index].append(players[NB_TEAMS * i + j])
    return [Team(teams[i]) for i in range(NB_TEAMS)]
    

#Swap players to reduce the metric of all teams until no swap can be performed
def balance_teams(teams) :
    
    #Check the player swap that reduces both metrics the most ; returns True if a swap was performed
    def check_swap(team_1, team_2) :
        
        #Swaps the players at indices on both teams
        def swap(team_1, team_2, index_1, index_2) :
            
            team_1.players[index_1], team_2.players[index_2] = team_2.players[index_2], team_1.players[index_1]

            
        nb_players = len(team_1.players)
        distance = team_1.metric() + team_2.metric()
        index_1 = -1
        index_2 = -1
        for i in range(nb_players) :
            for j in range(nb_players) :
                swap(team_1, team_2, i, j)
                new_distance = team_1.metric() + team_2.metric()
                if distance > new_distance :
                    distance = new_distance
                    index_1 = i
                    index_2 = j
                swap(team_1, team_2, i, j)
        if index_1 != -1 :
            swap(team_1, team_2, index_1, index_2)
            team_1.sort_players()
            team_2.sort_players()
            return True
        return False

    swap = True
    while swap :
        swap = False
        for i in range(NB_TEAMS - 1) :
            for j in range(i + 1, NB_TEAMS) :
                swap = swap or check_swap(teams[i], teams[j])

#Print players and metrics of all teams
def print_team_metrics(teams) :
    
    for team in teams :
        print([player.name for player in team.players], [player.seed for player in team.players], round(team.metric(),2))
    print("Metric total: " + str(round(sum(team.metric() for team in teams),2)))

#=========================================Main program=========================================
players = open_qualifiers_file()
teams = create_teams(players)
balance_teams(teams)
print("====Team balance====")
print_team_metrics(teams)
