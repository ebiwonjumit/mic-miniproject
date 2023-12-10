"""
This is where the implementation of the plugin code goes.
The othelloHighlightMoves-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('othelloHighlightMoves')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class othelloHighlightMoves(PluginBase):
  def main(self):
    active_node = self.active_node
    core = self.core
    logger = self.logger
    self.namespace = None
    META = self.META
    logger.debug('path: {0}'.format(core.get_path(active_node)))
    logger.info('name: {0}'.format(core.get_attribute(active_node, 'name')))
    logger.warn('pos : {0}'.format(core.get_registry(active_node, 'position')))
    logger.error('guid: {0}'.format(core.get_guid(active_node)))
    nodesList = core.load_sub_tree(active_node)
    nodes = {}
    states=[]
    
    current_game_state_path = core.get_pointer_path(active_node,'currentGameState')
    self.current_game_state = core.load_by_path(self.root_node,current_game_state_path)
    
    for node in nodesList:
      nodes[core.get_path(node)] = node

      
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
    self.states = states   
    #logger.info(states)
    #self.undo_move()
    #self.countPieces()
    self.highlightTiles()
    #self.computerMove()
    
  def computerCreateState(self,tile_to_play,tiles_to_flip):
    core = self.core
    META = self.META
    logger = self.logger
    current_node = self.active_node
    tile_row = core.get_attribute(tile_to_play,'row')
    tile_column = core.get_attribute(tile_to_play,'column')
    # Make new Game State
    new_game_state = core.copy_node(self.current_game_state,current_node)
    #point to previous state
    core.set_pointer(new_game_state,'previousGameState',self.current_game_state)
    #GameFolder points to the newly created state
    core.set_pointer(current_node,'currentGameState',new_game_state)
    current_name = core.get_attribute(self.current_game_state,'name')
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
    
    for path in children_new_state:
      node = core.load_by_path(self.root_node, path)
      if(core.is_instance_of(node,META['Player'])):
        current_node_color = core.get_attribute(node,'color')
        if(current_node_color == opposite_color[current_player_color]):
          core.set_pointer(new_game_state,'currentPlayer',node)
          
      #Create Piece
      if(core.is_instance_of(node,META['Board'])):
        tile_paths = core.get_children_paths(node)
        for tile_p in tile_paths:
          tile_node = core.load_by_path(self.root_node,tile_p)
          if(core.is_instance_of(tile_node,META['Tile'])):
            tile_node_row = core.get_attribute(tile_node, 'row')
            tile_node_column = core.get_attribute(tile_node,'column')
            if(tile_node_row == tile_row and tile_node_column == tile_column):
              created_piece = core.create_node({'parent':tile_node,'base':META['Piece']})
              core.set_attribute(created_piece, "color", opposite_color[current_player_color])
              core.set_pointer(new_game_state,'currentMove',created_piece)
            elif(tile_node_row, tile_node_column) in tiles_to_flip:
              current_piece_path = core.get_children_paths(tile_node)[0]
              current_piece = core.load_by_path(self.root_node,current_piece_path)
              core.set_attribute(current_piece,"color", opposite_color[current_player_color])
    
    self.util.save(self.root_node,self.commit_hash, self.branch_name)
    
    
  def computerMove(self):
    from random import randrange
    valid_tile_nodes,valid_tiles_to_flip = self.highlightTiles()
    rand_index = randrange(len(valid_tile_nodes))
    self.computerCreateState(valid_tile_nodes[rand_index],valid_tiles_to_flip[rand_index])
    
  def isValidMove(self, tile):
    self.is_tile_valid = False
    self.valid_tiles_to_flip =[]
    possible_next_moves = {"black":"white","white":"black"}
    directions = [(0,0),(0,1),(1,0),(1,1),(1,0),(0,1),(-1,-1),(-1,0),(0,-1),(-1,1),(1,-1)]
    logger = self.logger
    core = self.core
    current_node = self.active_node
    board = core.get_parent(current_node)
    game_state = core.get_parent(board)
    
    current_move_path = core.get_pointer_path(self.current_game_state,"currentMove")
    current_move = core.load_by_path(self.root_node,current_move_path)
    current_move_color = core.get_attribute(current_move,'color')
    self.next_move_color = possible_next_moves[current_move_color]
    state_path = self.current_game_state["nodePath"]
    
    
    for state in self.states:
      if state_path == state["path"]:
        board_ref = state["board"]
        column = core.get_attribute(tile,'column')
        row = core.get_attribute(tile,'row')
        if board_ref[row][column]['color'] == None:
          for direction in directions:
            tiles_to_flip =[]
            rows = len(board_ref)
            columns = len(board_ref[0])
            
            if 0 <= row + direction[0] < rows and 0 <= column + direction[1] < columns and board_ref[row+direction[0]][column+direction[1]] is not None:
              if board_ref[row+direction[0]][column+direction[1]]['color'] == current_move_color:
                tiles_to_flip = [(row + direction[0], column+ direction[1])]
                multiplier = 2
                while(row + (direction[0]*multiplier) > 0 and row + (direction[0]*multiplier) < 8) and (column + (direction[1]*multiplier) >0 and column + (direction[1]*multiplier)<8):
                  if board_ref[row + direction[0]*multiplier][column + (direction[1]*multiplier)]['color'] == self.next_move_color:
                    end_position = (row+direction[0]*multiplier, column +(direction[1]*multiplier))
                    for position in tiles_to_flip:
                      self.valid_tiles_to_flip.append(position)
                    self.is_tile_valid = True
                  tiles_to_flip.append((row+direction[0]*multiplier, column +(direction[1]*multiplier)))
                  multiplier += 1
    return self.is_tile_valid,self.valid_tiles_to_flip
    
  def highlightTiles(self):
    core = self.core
    logger = self.logger
    self.namespace = None
    META = self.META
    valid_tiles_to_play=[]
    valid_tiles_to_flip=[]
    valid_tile_nodes=[]
    
    #Children of the Game State
    children_game_state = core.get_children_paths(self.current_game_state)
    for path in children_game_state:
      node = core.load_by_path(self.root_node, path)
      if(core.is_instance_of(node,META['Board'])):
        tile_paths = core.get_children_paths(node)
        for tile_path in tile_paths:
          tile_node = core.load_by_path(self.root_node,tile_path)
          if(core.is_instance_of(tile_node,META['Tile'])):
            valid_tile,tiles_to_flip = self.isValidMove(tile_node)
            if valid_tile == True:
              tile_column = core.get_attribute(tile_node,'column')
              tile_row = core.get_attribute(tile_node,'row')
              valid_tiles_to_play.append([tile_row,tile_column])
              valid_tile_nodes.append(tile_node)
              valid_tiles_to_flip.append(tiles_to_flip)
    #logger.info(valid_tiles_to_play)                                   
    return valid_tile_nodes,valid_tiles_to_flip
    
    
  #Undo moves
  def undo_move(self):
    logger = self.logger
    core = self.core
    previous_game_state_path = core.get_pointer_path(self.current_game_state,'previousGameState')
    previous_game_state = core.load_by_path(self.root_node,previous_game_state_path)
    core.set_pointer(self.active_node,'currentGameState',previous_game_state)
    core.delete_node(self.current_game_state)
    self.util.save(self.root_node,self.commit_hash,self.branch_name)
    
  def countPieces(self):
    black_pieces = 0
    white_pieces = 0
    current_node=self.active_node 
    core = self.core
    logger = self.logger
    self.namespace = None
    META = self.META

    #Children of the Game State
    children_game_state = core.get_children_paths(self.current_game_state)
    
    for path in children_game_state:
      node = core.load_by_path(self.root_node, path)
      if(self.core.is_instance_of(node,META['Board'])):
        for tile_path in core.get_children_paths(node):
          tile = core.load_by_path(self.root_node,tile_path)
          piece_paths = core.get_children_paths(tile)
          if len(piece_paths) > 0:
            for piece_path in piece_paths:
              piece = core.load_by_path(self.root_node,piece_path)
              color_of_piece = core.get_attribute(piece,'color')
              if color_of_piece == 'black':
                black_pieces += 1
              if color_of_piece == 'white':
                white_pieces += 1
    logger.info('black pieces: {0}'.format(black_pieces))
    logger.info('white pieces: {0}'.format(white_pieces))
    return black_pieces,white_pieces
           

      
   

