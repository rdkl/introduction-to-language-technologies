#-*- coding: utf-8 -*-

from collections import namedtuple
import openpyxl
import transliterate

Player = namedtuple('Player', ("number", "name", "position"), verbose = False);

wb = openpyxl.load_workbook('hockey.xlsx')
ws = wb[wb.get_sheet_names()[0]]

players = {"home-team" : {},
           "guest-team" : {}}

# First line is a name of team.
home_team_players_start = 4
home_team_players_end = 26

guest_team_players_start = 28
guest_team_players_end = 50

# If failed here, change previous variables.
assert(ws["A" + str(home_team_players_start)].value == "home-team")
assert(ws["A" + str(guest_team_players_start)].value == "guest-team")


for i in xrange(home_team_players_start + 1, home_team_players_end + 1):
    player_number = ws["B" + str(i)].value
    player_name = ws["C" + str(i)].value
    player_position = ws["D" + str(i)].value
    player_name = transliterate.translit(player_name, "ru", reversed=True)
    players["home-team"][player_number] = Player(player_number, player_name, 
                                                 player_position)

for i in xrange(guest_team_players_start + 1, guest_team_players_end + 1):
    player_number = ws["B" + str(i)].value
    player_name = ws["C" + str(i)].value
    player_position = ws["D" + str(i)].value
    player_name = transliterate.translit(player_name, "ru", reversed=True)
    players["guest-team"][player_number] = Player(player_number, player_name, 
                                                 player_position)
    

periods = [[52, 76],
           [77, 98],
           [99, 120],
           [121, 121],
           [123, 133],
           ]
important_event_results = ['scored', 'score']
important_event_actions = ['injury']   

teams = {ws["E2"].value : "home-team",
         ws["F2"].value : "guest-team"}

reverse_teams = {"home-team" : ws["E2"].value,
                 "guest-team": ws["F2"].value}

for period in periods:
    first_period_start = period[0]
    first_perion_end = period[1] 
    for i in xrange(first_period_start + 1, first_perion_end + 1):
        event_number = ws["A" + str(i)].value
        event_time = ws["B" + str(i)].value
        event_action = ws["C" + str(i)].value
        event_team = ws["D" + str(i)].value
        event_player_number = ws["E" + str(i)].value
        event_place = ws["F" + str(i)].value
        event_result = ws["J" + str(i)].value
        
        
        
        if event_team != None:
            team = teams[event_team]
        
        if event_action in important_event_actions:
            print players[team][event_player_number].name, event_action, 
            print event_team
        
        if event_result in important_event_results:
            print players[team][event_player_number].name, event_result, 
            print event_team,
            
            if event_place != None:                
                print "from", event_place
            else:
                print 
                
                
last_row = ws.get_highest_row()
home_score = ws["B" + str(last_row - 1)].value
guest_score = ws["B" + str(last_row)].value

if guest_score == home_score:
    print "Result of the match is draw"
if guest_score > home_score:
    print reverse_teams["guest-team"], " beat ", reverse_teams["home-team"],
    print " with score ", guest_score, ":", home_score 
    
    
from py4j.java_gateway import launch_gateway, java_import
gateway = launch_gateway(jarpath="simplenlg-v4.4.2.jar")
jvm = gateway.jvm
java_import(jvm, 'simplenlg.framework.*')
# os.system("java -jar simplenlg-v4.4.2.jar")