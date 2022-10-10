from .helper2 import *
import numpy as np

class Agent:

    def __init__(self):
        '''
        Place any initialization code for your agent here (if any)
        ''' 
        self.pending_actions = []
        self.pending_actions_bombs = []
        self.bombs_places=[]
        self.bombs_ticks=[]
        self.actions_taken= []        
        self.treasure=[]
        self.nextposition = ()      

    def next_move(self, game_state, player_state):

        
        player_ammo = player_state.ammo
        player_location = player_state.location
        enemy_location = game_state.opponents(1)[0]
        ammo = get_ammo(game_state)
        trs = get_treasure(game_state)
        action = ''
        tick_number = game_state.tick_number
        bombs = game_state.bombs
        self.pending_actions = []

        print()
        print(f"tick: {game_state.tick_number}")
        print(player_location)
        print(enemy_location)
        print()
        print(f"actions taken : {self.actions_taken}")
        print(f"next position : {self.nextposition}")
        

        if tick_number == 0:
            self.nextposition = player_location
        
        else:
            if self.actions_taken:
                self.nextposition = nmove(self.actions_taken.pop() , self.nextposition )
                if self.nextposition != player_location:
                    
                    return ""
            
        X,Y = player_location
        print(f"actions taken : {self.actions_taken}")
        print(f"next position : {self.nextposition}")
        print(f"bombs places {self.bombs_places}")
        print(f"bombs ticks {self.bombs_ticks}")

        for i in range(len(self.bombs_places)):
            if len(self.bombs_places) > i :
                if tick_number > self.bombs_ticks[i] + 35:
                    self.bombs_ticks.remove(self.bombs_ticks[i])
                    self.bombs_places.remove(self.bombs_places[i])

        
        for i in bombs:
            if i not in self.bombs_places:
                self.bombs_places.append(i)
                self.bombs_ticks.append(tick_number)

        game_map = print_map(self, game_state)
        
        game_map = get_unsafe_places(self.bombs_places,game_map,game_state)
        print(str(self.pending_actions)+ "  pending actions")
        print(str(self.pending_actions_bombs)+ "  pending actions under escaping bombs") 
        
        

        if bombs:
            if game_map[Y][X] != 0:

                if len(self.pending_actions_bombs) > 0:
                    
                    print(str(self.pending_actions_bombs)+ "  pending actions under escaping bomb")
                    action = self.pending_actions_bombs.pop()
                    print(f"Action under escaping bomb: {action}")
                
                else:                    
                    pos = safe_place(game_state, player_location ,game_map)

                    if pos:
                        for i in pos:
                            path = astar_b(game_state, player_location, i,game_map)
                            if path:
                                
                                print(f"target : {i}")
                                print(f"player location : {player_location}")
                                actions = get_path_actions(path)
                                for i in actions:
                                    self.pending_actions_bombs.append(i)
                                
                                print(str(self.pending_actions_bombs)+ "  pending actions under escaping bomb")
                                action = self.pending_actions_bombs.pop()
                                print(f"Action under escaping bomb: {action}")
                                if action != "":
                                    break
                                

                if action != '' and not game_state.is_occupied(nextPosition(action,player_location)):
                    self.actions_taken.append(action)
                    return action
                elif action != '':
                    self.pending_actions_bombs.append(action)
                    
                

        togo = anyoption(player_location, game_map, game_state)
        print(togo)
        if togo :

            print("Player has safe positions to go")
            print(togo)

            if ammo :     

                    for i in ammo:
                
                        print("Player searching for ammo path")

                        path = astar(game_state, player_location, i)

                        if path:
                            actions = get_path_actions(path)
                            for i in actions:
                                self.pending_actions.append(i)
                            print(str(self.pending_actions)+ "  pending actions under ammo ")
                            action = self.pending_actions.pop()
                            break
                        
                        

            elif trs :                  
                    for i in trs:

                        path = astar(game_state, player_location, i)
                        if path:
                            actions = get_path_actions(path)
                            for i in actions:
                                self.pending_actions.append(i)
                            print(str(self.pending_actions)+ "  pending actions under")
                            action = self.pending_actions.pop()
                            break

            f_pos = nmove(action, player_location)

            if f_pos in togo:
                    print(f"Action under taking ammo/treasure: {action}")
                    self.actions_taken.append(action)
                    return action
            elif action != '':
                self.pending_actions.append(action)
            

            action = ''

            if player_ammo >0 :              

                print("Player is going towards enemy")
                if isnearenemy(enemy_location,player_location) and game_state.tick_number == tick_number:
                    action = 'p'
                    print(f"Action under reaching enemy: {action}")
                    return action             
                
                else:
                    print("********************************")
                    tar = enemy_nearplaces(enemy_location,player_location,game_state)
                    if tar:
                        for i in tar:
                            path = astar(game_state,player_location,i)
                            if path:
                                actions = get_path_actions(path)
                                for i in actions:
                                    self.pending_actions.append(i)
                                
                                print(str(self.pending_actions)+ "  pending actions under reaching enemy ")

                                action = self.pending_actions.pop()
                                break
    

                f_pos = nextPosition(action,player_location)
                

                if f_pos in togo:
                    print(f"Action under reaching enemy: {action}")
                    self.actions_taken.append(action)
                    return action

                elif action != '':
                    self.pending_actions.append(action)

                                                                                                                                                                                  
            self.actions_taken.append('')
            return ''  

        else:
            self.actions_taken.append('')
            return ''
