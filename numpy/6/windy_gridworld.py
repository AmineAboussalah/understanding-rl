import numpy as np

INIT_POS = (3, 0)
#INIT_POS = (3, 0)
GOAL_POS = (3, 7)
#GOAL_POS = (3, 4)
WIND_ARR = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
#WIND_ARR = [0, 1, 2, 1, 0]
GRID_SHAPE = (7, 10)
#GRID_SHAPE = (5, 5)
R_STEP = -1
KEY_ACTION_DICT = {
  'a': (-1, 0),
  'z': (-1, 1),
  'e': (-1, -1),
  'q': (0, -1),
  's': (0, 0),
  'd': (0, 1),
  'w': (1, -1),
  'x': (1, 0),
  'c': (1, 1),
}
POS_CHAR_DICT = {
  GOAL_POS: 'G',
  INIT_POS: 'S',
}
AGENT_KEY = 'A'

class Position:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  def in_bounds(self, index, axis):
    return max(0, min(index, GRID_SHAPE[axis] - 1))
  
  def get_wind(self, stoch):
    return WIND_ARR[self.y] + stoch * np.random.randint(-1, 2)

  def update_pos(self, wind, action):
    dx, dy = action
    self.x = self.in_bounds(self.x + dx - wind, 0)
    self.y = self.in_bounds(self.y + dy, 1)
  
  def __eq__(self, other_pos):
    return self.x == other_pos.x and self.y == other_pos.y

  def __add__(self, other_pos):
    return Position(self.x + other_pos.x, self.y + other_pos.y)

  def __hash__(self):
    return hash((self.x, self.y))

  def __str__(self):
    return f"({self.x}, {self.y})"

class WindyGridworld:
  def __init__(self, diags=False, stay=False, stoch=False):
    self.diags = diags
    self.stay = stay
    self.stoch = stoch
    self.get_moves()
    self.get_states()
    self.get_keys()

  def get_moves(self):
    self.moves = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if (abs(x) + abs(y)) == 1]
    if self.diags:
      self.moves += [(x, y) for x in [-1, 1] for y in [-1, 1] if x + y == 0]
    if self.stay:
      self.moves += [(0, 0)]

  def get_states(self):
    self.states = [Position(x, y) for x in range(GRID_SHAPE[0]) for y in range(GRID_SHAPE[1])]

  def step(self, action):
    self.state.update_pos(self.state.get_wind(self.stoch), action)
    return self.state, R_STEP, self.state == Position(*GOAL_POS), {}

  def reset(self):
    self.state = Position(*INIT_POS)
    return self.state

  def get_keys(self):
    self.keys = KEY_ACTION_DICT.keys()

  def step_via_key(self, key):
    return self.step(KEY_ACTION_DICT[key])

  def __str__(self):
    x_ag, y_ag = self.state.x, self.state.y
    s = ''
    for wind in WIND_ARR:
      s += str(wind)
    s += '\n'
    for x in range(GRID_SHAPE[0]):
      for y in range(GRID_SHAPE[1]):
        if (x, y) in POS_CHAR_DICT.keys():
          s += POS_CHAR_DICT[(x, y)]
        elif (x, y) == (x_ag, y_ag):
          s += AGENT_KEY
        else:
          s += '.'
      s += '\n'
    return s
