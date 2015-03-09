#-*- coding: utf-8 -*-

from collections import namedtuple
import openpyxl
from transliterate import translit
import random

#-----------------------------------------------------------------------------
# On the DATE HOME_TEAM welcomed GUEST_TEAM on the ice of CITY's ARENA.
# HOME_TEAM met GUEST_TEAM on ARENA rink in CITY on DATE. 
def generate_intro(date, home_team_name, guest_team_name, arena_name, city):
    selector = random.randint(0, 1)
    result = ""
    if selector == 0:
        result += "On " + date + " " + home_team_name + " welcomed " 
        result += guest_team_name + " on the ice of " + arena_name + " in " + city
        result += "."
    if selector == 1:
        result += home_team_name + " met " + guest_team_name + " on "
        result += arena_name + " rink in " + city + " on " + date + "."
    return result 

#-----------------------------------------------------------------------------
def add_ending(number):
    if type(number) == int:
        return add_ending(str(number))
    
    if type(number) == str:
        if number == '11':
            return "11th"
        if number == '12':
            return "12th"
        last_digit = int(number[-1])
        if last_digit == 1:
            return number + "st"
        if last_digit == 2:
            return number +  "nd"
        if last_digit == 3:
            return number +  "rd"
        return number +  "th"        

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    # Load data.
    home_team = "home-team"
    guest_team = "guest-team"
    
    is_first_goal_scored = False 
    
    Player = namedtuple('Player', 
                        ("number", "name", "position"), 
                        verbose = False);
    
    wb = openpyxl.load_workbook('hockey.xlsx')
    ws = wb[wb.get_sheet_names()[0]]
    
    teams = {ws["E2"].value : home_team,
             ws["F2"].value : guest_team}
    
    team_names = {home_team : ws["E2"].value,
                     guest_team: ws["F2"].value}
    
    # Generate intro section.
    match_date = ws["A2"].value
    intro = generate_intro(str(match_date.strftime("%B")) + " " + \
                           str(match_date.strftime("%d")), 
                           team_names[home_team], 
                           team_names[guest_team], 
                           translit(ws["B2"].value, "ru", reversed=True), 
                           translit(ws["C2"].value, "ru", reversed=True))
    print intro
    # End of intro section.
    
    players = {home_team : {},
               guest_team : {}}
    
    # First line is a name of team.
    home_team_players_start = 4
    home_team_players_end = 26
    
    guest_team_players_start = 28
    guest_team_players_end = 50
    
    # If failed here, change previous variables.
    assert(ws["A" + str(home_team_players_start)].value == home_team)
    assert(ws["A" + str(guest_team_players_start)].value == guest_team)
    
    
    for i in xrange(home_team_players_start + 1, home_team_players_end + 1):
        player_number = ws["B" + str(i)].value
        player_name = ws["C" + str(i)].value
        player_position = ws["D" + str(i)].value
        player_name = translit(player_name, "ru", reversed=True)
        players[home_team][player_number] = Player(player_number, player_name, 
                                                     player_position)
    
    for i in xrange(guest_team_players_start + 1, guest_team_players_end + 1):
        player_number = ws["B" + str(i)].value
        player_name = ws["C" + str(i)].value
        player_position = ws["D" + str(i)].value
        player_name = translit(player_name, "ru", reversed=True)
        players[guest_team][player_number] = Player(player_number, player_name, 
                                                     player_position)
        
    
    periods = [[52, 76],
               [77, 98],
               [99, 120],
               [121, 121],
               [123, 133],
               ]
    goal_events = ['scored', 'score']
    important_event_actions = ['injury']   
    
    
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
            
            if event_action in goal_events:
                if is_first_goal_scored is False:
                    # First goal event.
                    is_first_goal_scored = True
                    pass
                else:
                    # Common goal event.
                    pass                
                continue
            
            if event_team != None:
                team = teams[event_team]
            
            if event_action in important_event_actions:
                print players[team][event_player_number].name, event_action, 
                print event_team
            
            if event_result in goal_events:
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
        print team_names[guest_team], " beat ", team_names[home_team],
        print " with score ", guest_score, ":", home_score 
    