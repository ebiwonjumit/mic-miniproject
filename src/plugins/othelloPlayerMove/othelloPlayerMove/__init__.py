"""
This is where the implementation of the plugin code goes.
The othelloPlayerMove-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('othelloPlayerMove')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class othelloPlayerMove(PluginBase):
  def main(self):
    active_node = self.active_node
    core = self.core
    logger = self.logger
    self.namespace = None
    global_counter = core.set_attribute(core.get_parent(core.get_parent(core.get_parent(active_node))),'global_counter',0)
    META = self.META
    logger.debug('path: {0}'.format(core.get_path(active_node)))
    logger.info('name: {0}'.format(core.get_attribute(active_node, 'name')))
    logger.warn('pos : {0}'.format(core.get_registry(active_node, 'position')))
    logger.error('guid: {0}'.format(core.get_guid(active_node)))
    nodesList = core.load_sub_tree(core.get_parent(core.get_parent(core.get_parent(active_node))))
    nodes = {}
    states=[]
    
    for node in nodesList:
      nodes[core.get_path(node)] = node
      self.nodes = nodes
      
    for path in nodes:
      node = nodes[path]
      game_state={}
      
      if (core.is_instance_of(node, META['GameState'])):
        game_state['name'] = core.get_attribute(node, 'name')
        game_state['path'] = path
        states.append(game_state)
        
        #currentPlayer Path
        currentPlayer_path = core.get_pointer_path(node,'currentPlayer')
        player = nodes[currentPlayer_path]
        game_state['currentPlayer'] = core.get_attribute(player, 'currentPlayer')
        
        #currentPlayer Color
        currentPlayer_color = core.get_attribute(player, 'color')
        #logger.info(currentPlayer_color)
        
        #currentPlayer Move
        currentPlayer_move = core.get_pointer_path(node, 'currentMove')
        curr = nodes[currentPlayer_move]
        currentMove = {}
        currentMove['color'] = core.get_attribute(curr, 'color')
        currentMove['row'] = core.get_attribute(curr, 'row')
        currentMove['column']= core.get_attribute(curr, 'column')
        game_state['currentPlayerMove'] = currentMove
        
        rows = 8
        columns = 8
        board = [[0 for _ in range(columns)] for _ in range(rows)]
        game_state['board'] = board
        
      if (core.is_instance_of(node, META['Tile'])):
        for game_state in states:
          if game_state["path"][:4] == path[:4]:
            row = core.get_attribute(node, 'row')
            column = core.get_attribute(node, 'column')
            children = core.get_children_paths(node)
            flips = []
            childColor = None
            childPath = None
            if len(children) > 0:
              childPath = children[0]
              childColor = core.get_attribute(nodes[childPath], 'color')
              for ePaths in nodes:
                eNode = nodes[ePaths]
                if(core.is_instance_of(eNode, META['mightFlip'])):
                  srcTile = core.get_parent(nodes[core.get_pointer_path(eNode,'src')])
                  dstTile = core.get_parent(nodes[core.get_pointer_path(eNode,'dst')])
                  dstInfo = {'column': core.get_attribute(dstTile,'column'),'row': core.get_attribute(dstTile,'row')}
                  if node == srcTile:
                    flips.append(dstInfo)
                    
            game_state["board"][row][column] = {"color":childColor, 'flips':flips} 
        
   # logger.info(states)
    self.states = states
    #logger.info("Valid Move: {}".format(self.isValidMove()))
    self.isValidMove()
    self.makeNewState()
    
  def isValidMove(self):
    self.is_tile_valid = False
    self.valid_tiles_to_flip =[]
    possible_next_moves = {"black":"white","white":"black"}
    directions = [(0,0),(0,1),(1,0),(1,1),(1,0),(0,1),(-1,-1),(-1,0),(0,-1),(-1,1),(1,-1)]
    logger = self.logger
    core = self.core
    current_node = self.active_node
    board = core.get_parent(current_node)
    game_state = core.get_parent(board)
    current_move = self.nodes[core.get_pointer_path(game_state,"currentMove")]
    current_move_color = core.get_attribute(current_move,'color')
    next_move_color = possible_next_moves[current_move_color]
    state_path = game_state["nodePath"]
    for state in self.states:
      if state_path == state["path"]:
        board_ref = state["board"]
        column = core.get_attribute(current_node,'column')
        row = core.get_attribute(current_node,'row')
        if board_ref[row][column]['color'] == None:
          for direction in directions:
            tiles_to_flip =[]
            if board_ref[row+direction[0]][column+direction[1]]['color'] == current_move_color:
              tiles_to_flip = [(row + direction[0], column+ direction[1])]
              multiplier = 2
              while(row + (direction[0]*multiplier) > 0 and row + (direction[0]*multiplier) < 8) and (column + (direction[1]*multiplier) >0 and column + (direction[1]*multiplier)<8):
                if board_ref[row + direction[0]*multiplier][column + (direction[1]*multiplier)]['color'] == next_move_color:
                  end_position = (row+direction[0]*multiplier, column +(direction[1]*multiplier))
                  for position in tiles_to_flip:
                    self.valid_tiles_to_flip.append(position)
       
                  self.is_tile_valid = True
                tiles_to_flip.append((row+direction[0]*multiplier, column +(direction[1]*multiplier)))
                multiplier += 1
    return
    
    
  def makeNewState(self):
    if not self.is_tile_valid:
      self.logger.error('THIS IS NOT A VALID MOVE')
      self.create_message(self.active_node, 'THIS IS NOT A VALID MOVE')
      return
    
    logger = self.logger
    core = self.core
    current_node = self.active_node
    META = self.META
    board = core.get_parent(current_node)
    
    
    # Make new Game State
    game_state = core.get_parent(board)
    game_folder = core.get_parent(game_state)
    self.row = core.get_attribute(current_node, 'row')
    self.column = core.get_attribute(current_node, 'column')
    new_game_state = core.copy_node(game_state,game_folder)
    #point to previous state
    core.set_pointer(new_game_state,'previousGameState',game_state)
    #GameFolder points to the newly created state
    core.set_pointer(game_folder,'currentGameState',new_game_state)
    current_name = core.get_attribute(game_state,'name')
    original_name = 'OthelloGame'
    new_number = 0
    if '_' in current_name:
      new_number = int(current_name[-1:])+1
      base_name = current_name[:-2]
    else:
      base_name = original_name
      new_number = 1
    new_name = f"{base_name}_{new_number}"
    core.set_attribute(new_game_state, "name", new_name)
    
    #Children of new Game State
    children_new_state = core.get_children_paths(new_game_state)
    
    
    #Switch Player
    opposite_color = {"black":"white","white":"black"}
    current_player_path = core.get_pointer_path(new_game_state,'currentPlayer')
    current_player = core.load_by_path(self.root_node, current_player_path)
    current_player_color = core.get_attribute(current_player, 'color')
    logger.info(current_player_color)
    
    for path in children_new_state:
      node = core.load_by_path(self.root_node, path)
      if(core.is_instance_of(node,META['Player'])):
        current_node_color = core.get_attribute(node,'color')
        if(current_node_color == opposite_color[current_player_color]):
          logger.info(current_node_color)
          core.set_pointer(new_game_state,'currentPlayer',node)
          
      #Create Piece
      if(core.is_instance_of(node,META['Board'])):
        tile_paths = core.get_children_paths(node)
        for tile_p in tile_paths:
          tile_node = core.load_by_path(self.root_node,tile_p)
          if(core.is_instance_of(tile_node,META['Tile'])):
            tile_node_row = core.get_attribute(tile_node, 'row')
            tile_node_column = core.get_attribute(tile_node,'column')
            if(tile_node_row == self.row and tile_node_column == self.column):
              created_piece = core.create_node({'parent':tile_node,'base':META['Piece']})
              core.set_attribute(created_piece, "color", opposite_color[current_player_color])
              core.set_pointer(new_game_state,'currentMove',created_piece)
            elif(tile_node_row, tile_node_column) in self.valid_tiles_to_flip:
              current_piece_path = core.get_children_paths(tile_node)[0]
              current_piece = core.load_by_path(self.root_node,current_piece_path)
              core.set_attribute(current_piece,"color", opposite_color[current_player_color])
    
     
    self.util.save(self.root_node,self.commit_hash, self.branch_name)

    
      

      


      
   


