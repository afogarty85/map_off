# Map Off
# Made with Love for Hannah
# v 0.2 - Work in Progress; 21 NOV 19

## todo:
# class helper function
# adding a capital city marker would be a nice addition
# need better shapefiles

import pandas as pd
import numpy as np


class Maps():
    ''' This class builds the maps.  '''

    def __init__(self):
        ''' The constructor initializes a couple of string containers for
        filter and win/lose conditions checks.  '''
        self.dataset_selection = ''
        self.check_map = ''

    def load_data(self):
        ''' This method allows the user to load the playing area: U.S. States or the World. '''
        user_input = input('Please select the data set: U.S. States or the World. Please enter: States or World ').title()

        if user_input == 'World':
            self.df = pd.read_csv('https://raw.githubusercontent.com/afogarty85/map_off/master/world.csv', low_memory=False)
            # fix shapeid so its numeric
            self.df['shapeid'] = pd.to_numeric(self.df['shapeid'])
            self.df['shapeid'] = self.df['shapeid'].astype(float).astype(int)
            print("The World dataset is loaded")
            self.dataset_selection += 'World'

        if user_input == 'States':
            self.df = pd.read_csv('https://raw.githubusercontent.com/afogarty85/map_off/master/states.csv', low_memory=False)
            # fix shapeid so its numeric
            self.df['shapeid'] = pd.to_numeric(self.df['shapeid'])
            self.df['shapeid'] = self.df['shapeid'].astype(float).astype(int)
            print("The States dataset is loaded")
            self.dataset_selection += 'States'
            self.filtered_df = self.df
            self.random_choice_list = list(self.filtered_df['shapeid'].unique())
            self.random_shape_selection = np.random.choice(self.random_choice_list, 1)
            self.current_map = self.filtered_df[self.filtered_df.shapeid == self.random_shape_selection[0]]
            self.current_map.reset_index(inplace=True)
            self.check_map = self.current_map['SOVEREIGNT'][0]

        if user_input not in ['World', 'States']:
            raise Exception('Please enter World or States')

    def select_map(self):
        ''' This method lets the user select the continent to play on. '''

        continents = ['Europe', 'Africa', 'Asia', 'South America', 'Oceania', 'Antarctica']
        user_input = input('To choose the playing area, please enter World or a continent like Europe, Africa, South America, Oceania, Asia. ').title()

        if user_input not in continents: # check user input
            raise Exception('Please enter the correct continent') # raise exception in case they make a mistake

        # filter dataframe by continent
        if any(continent in user_input for continent in continents):
            self.filtered_df = self.df[self.df.CONTINENT == user_input]
            self.random_choice_list = list(self.filtered_df['shapeid'].unique())
            self.random_shape_selection = np.random.choice(self.random_choice_list, 1)
            self.current_map = self.filtered_df[self.filtered_df.shapeid == self.random_shape_selection[0]]
            self.current_map.reset_index(inplace=True)
            self.check_map = self.current_map['SOVEREIGNT'][0]


class MapDraw():
    ''' This class draws the map in ASCII for command prompt usage.    '''

    def __init__(self, Maps):
        '''  method description  '''
        self.Maps = Maps

    def draw_map(self):
        dataframe = self.Maps.current_map
        HEIGHT = 20
        WIDTH = 50
        MARKER = '*'
        FILL_CHARACTER = ' '

        coordinate_container = []
        for i in range(dataframe.shape[0]):
            coordinate_container.append([dataframe['x'][i], (dataframe['y'][i])])

        xmin = dataframe['x'].min()
        xmax = dataframe['x'].max()
        kx = (WIDTH - 1)  / (xmax - xmin)

        ymin = dataframe['y'].min()
        ymax = dataframe['y'].max()
        ky = (HEIGHT - 1) / (ymax - ymin)

        acoords = [(round((c[0] - xmin) * kx),
                    round((c[1] - ymin) * ky)) for c in coordinate_container]

        for y in range(HEIGHT, -1, -1):
            chars = []
            for x in range(WIDTH):
                if (x, y) in acoords:
                    chars.append(MARKER)
                else:
                    chars.append(FILL_CHARACTER)
            print(''.join(chars))


class Scoreboard():
    '''
    This class keeps track of the scores.   '''

    def __init__(self):
        '''  method description  '''
        self.total_players = 0
        self.score = []
        self.player1 = ''
        self.player2 = ''
        self.player1_guess = ''
        self.player2_guess = ''
        self.local_score_p1 = 0
        self.local_score_p2 = 0

    def numberize(self):
        ''' This method gets the number of players '''
        user_input = int(input('Please enter the number of players playing: '))
        self.total_players += user_input
        if user_input > 2:
            raise Exception("The current build only allows for 1 or 2 players")

    def player_names(self):
        ''' This method gets player names from the users. '''
        if self.total_players == 1:
            user_input = input("Please enter your name: ").title()
            self.player1 += user_input

        else:
            user_input = input("Please enter Player 1's name: ").title()
            self.player1 += user_input
            user_input = input("Please enter Player 2's name: ").title()
            self.player2 += user_input

    def init_scoreboard(self):
        ''' This method builds the scoreboard. '''
        if self.total_players == 1:
            self.score.append(0)
        else:
            self.score.append(0)
            self.score.append(0)

class Check_Answers():
    ''' This class checks the answers and awards points to the Scoreboard.
    I'm not sure why self.Maps.check_map functions correctly while
    self.Scoreboard.player1_guess does not; currently working however.
    '''

    def __init__(self, Maps1, Scoreboard1):
        ''' The constructor requires the Maps and Scoreboard class. '''
        self.Maps = Maps1
        self.Scoreboard = Scoreboard1

    def retrieve_answers(self):
        ''' This method asks the user to guess the right answer. '''
        if self.Scoreboard.total_players == 1:
            user_input = input("Please enter the country's name: ").title()
            self.Scoreboard.player1_guess = user_input

        elif self.Scoreboard.total_players == 2:
            user_input = input(f"{self.Scoreboard.player1}, please enter the country's name: ").title()
            self.Scoreboard.player1_guess = user_input
            user_input = input(f"{self.Scoreboard.player2}, please enter the country's name: ").title()
            self.Scoreboard.player2_guess = user_input

    def award_points(self):
        ''' Given answers yielded above, this method awards points based on
        the correct answer. '''

        if self.Scoreboard.total_players == 1 and self.Scoreboard.player1_guess == self.Maps.check_map:
            self.Scoreboard.score[0] += 1
            print("You guessed correctly!")
            print('The current score is: ', self.Scoreboard.score)

        if self.Scoreboard.total_players == 1 and self.Scoreboard.player1_guess != self.Maps.check_map:
            print("You guessed incorrectly!", 'The correct answer is: ', self.Maps.check_map)

        if self.Scoreboard.total_players == 2 and self.Scoreboard.player1_guess == self.Maps.check_map:
            self.Scoreboard.score[0] += 1
            self.Scoreboard.local_score_p1 = 1

            if self.Scoreboard.total_players == 2 and self.Scoreboard.player2_guess == self.Maps.check_map:
                self.Scoreboard.score[1] += 1
                self.Scoreboard.local_score_p2 = 1

            print(f"{self.Scoreboard.player1} was awarded", self.Scoreboard.local_score_p1, 'points', '\n',
            f"{self.Scoreboard.player2} was awarded", self.Scoreboard.local_score_p2, 'points', '\n',
            'The current score is', self.Scoreboard.score)

        if self.Scoreboard.total_players == 2 and self.Scoreboard.player1_guess != self.Maps.check_map:
            print(f"{self.Scoreboard.player1} guessed incorrectly", 'The correct answer is: ', self.Maps.check_map)

        if self.Scoreboard.total_players == 2 and self.Scoreboard.player2_guess != self.Maps.check_map:
            print(f"{self.Scoreboard.player2} guessed incorrectly", 'The correct answer is: ', self.Maps.check_map)


class Control():
    '''
    This class controls the game.
    '''
    def __init__(self):
        '''  Nothing to initialize in the constructor here. '''
        pass

    def run_game(self):
        '''
        This method executes the game and maintains it in a loop.
         '''
        while True:
            maps1 = Maps()
            maps1.load_data()
            if maps1.dataset_selection == 'World':
                maps1.select_map()
            else:
                pass
            score1 = Scoreboard()
            score1.numberize()
            score1.init_scoreboard()
            score1.score
            score1.player_names()
            score1.player1
            score1.player2

            draw1 = MapDraw(maps1)
            draw1.draw_map()

            check1 = Check_Answers(maps1, score1)
            check1.retrieve_answers()
            score1.player1_guess
            score1.player2_guess
            check1.award_points()
            while True:
                while True:
                    maps1 = Maps()
                    maps1.load_data()
                    if maps1.dataset_selection == 'World':
                        maps1.select_map()
                    else:
                        pass

                    draw1 = MapDraw(maps1)
                    draw1.draw_map()

                    check1 = Check_Answers(maps1, score1)
                    check1.retrieve_answers()
                    score1.player1_guess
                    score1.player2_guess
                    check1.award_points()
                    break

####
control1 = Control()
control1.run_game()

#### Debugging
#maps1 = Maps()
#maps1.load_data()
#maps1.select_map()
#maps1.check_map
#maps1.dataset_selection
#maps1.dataset_selection == 'World'


#score1 = Scoreboard()
#score1.numberize()
#score1.total_players

#score1.init_scoreboard()
#score1.score
#score1.player_names()
#score1.player1
#score1.player2

#draw1 = MapDraw(maps1)
#draw1.draw_map()

#score1.retrieve_answers()
#score1.player1_guess
#score1.player2_guess
#score1.award_points()
#score1.score
