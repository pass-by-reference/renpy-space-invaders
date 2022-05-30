init python:

  EXPLODING_IMAGE = "exploding.png"
  INVADER_IMAGE_ONE = "InvaderA1.png"
  INVADER_IMAGE_TWO = "InvaderB1.png"
  INVADER_IMAGE_THREE = "InvaderA2.png"
  INVADER_IMAGE_FOUR = "InvaderC1.png"
  INVADER_IMAGE_FIVE = "InvaderB2.png"
  INVADER_IMAGE_SIX = "InvaderC2.png"
  
  class InvaderManagerBuilder:
    
    class InvaderPositions:
      def __init__(self):
        self.initial_x = 0
        self.initial_y = 0

    class InvaderPadding:
      def __init__(self):
        self.x_padding = 0
        self.y_padding = 0

    class InvaderSize:
      def __init__(self):
        self.width = 0
        self.height = 0

    def __init__(self):
      self.rows = 0
      self.columns = 0

      self.exploding_time = 0
      self.speed = 0
      self.shoot_interval = 0

      self.invader_positions = self.InvaderPositions()
      self.invader_padding = self.InvaderPadding()
      self.invader_size = self.InvaderSize()

    def set_invader_positions(self, x, y):
      self.invader_positions.x = x
      self.invader_positions.y = y

    def set_invader_size(self,width,height):
      self.invader_size.width = width
      self.invader_size.height = height

    def set_invader_padding(self, x_padding, y_padding):
      self.invader_padding.x_padding = x_padding
      self.invader_padding.y_padding = y_padding
  
  class InvaderManager:
    """
    InvaderManager manages the invaders on screen
    1) Rendering/drawing of invaders
    2) Invader Movement And Position

    Invaders are stored in 1D array of InvaderRow
    InvaderRow is a inherited from list so in effect,
    the invaders can be used as a 2d array
    """
    
    class InvaderRow(list):
      def __init__(self, invaders):
        self.extend(invaders)
        self.direction = "right"

      def __getitem__(self, key):
        return list.__getitem__(self, key)

      def __setitem__(self, key, item):
        return list.__setitem__(self, key, item)

    def __init__(self, ivd_man_builder, wave):
      """
      Accepts a InvaderManagerBuilder
      """
      self.rows = ivd_man_builder.rows
      self.columns = ivd_man_builder.columns
      self.exploding_time = ivd_man_builder.exploding_time
      self.speed = ivd_man_builder.speed
      self.screen_width = SCREEN_WIDTH
      self.screen_height = SCREEN_HEIGHT
      self.shoot_interval = ivd_man_builder.shoot_interval

      self.initial_x = ivd_man_builder.invader_positions.x
      self.initial_y = ivd_man_builder.invader_positions.y

      self.x_padding = ivd_man_builder.invader_padding.x_padding
      self.y_padding = ivd_man_builder.invader_padding.y_padding

      self.invader_width = ivd_man_builder.invader_size.width
      self.invader_height = ivd_man_builder.invader_size.height

      self.destroyed = 0
      self.invaders = []

      # Every new instantiation of the invader 
      self.create_invaders()

    def create_invaders(self):
      for row in range(self.rows):
        row_of_invaders = []
        invader_img = self.__determine_invader_img(row)
        for column in range(self.columns):
          invader = Invader(invader_img,self.exploding_time, self.invader_width, self.invader_height)
          x, y = self.__get_grid_pos(row,column)

          invader.set_pos(x,y)
          row_of_invaders.append(invader)

        invader_rows = self.InvaderRow(row_of_invaders)
        self.invaders.append(invader_rows)
    
    def __get_grid_pos(self, row, column):
      new_initial_x = 0
      even_row_start = self.initial_x + self.x_padding/2

      if row % 2 == 0:
        new_initial_x = even_row_start
      else:
        new_initial_x = self.initial_x

      x = new_initial_x + column * self.x_padding
      y = self.initial_y + row * self.y_padding

      return x,y

    def __determine_invader_img(self, row):
      if row % 6 == 0:
        return INVADER_IMAGE_SIX
      elif row % 5 == 0:
        return INVADER_IMAGE_FIVE
      elif row % 4 == 0:
        return INVADER_IMAGE_FOUR
      elif row % 3 == 0:
        return INVADER_IMAGE_THREE
      elif row % 2 == 0:
        return INVADER_IMAGE_TWO
      else:
        return INVADER_IMAGE_ONE
    
    def draw_invaders(self, draw_args):
      invaders = list(chain.from_iterable(self.invaders))
      for invader in invaders:
        if invader.is_destroyed:
          continue

        invader.draw(draw_args)

    def remove_invaders(self, st):
      invaders = list(chain.from_iterable(self.invaders))
      for invader in invaders:
        can_remove = invader.should_remove(st)
        if not invader.is_destroyed and can_remove:
          invader.is_destroyed = True

    def move_invaders(self, dtime):
      for invader_row in self.invaders:
        self.__move_invader_row(invader_row, dtime)
    
    def __move_invader_row(self, invader_row, dtime):
      first = invader_row[0]
      last = invader_row[-1]

      if first.x < 0:
        invader_row.direction = "right"

      if last.x > self.screen_width - 300:
        invader_row.direction = "left"

      for invader in invader_row:
        self.__move_invader(invader_row.direction, invader, dtime)

    def __move_invader(self, direction, invader, dtime):

      direct_vector = 1 if direction == "right" else -1

      new_x = invader.x + dtime*self.speed*direct_vector
      new_y = invader.y

      invader.set_pos(new_x, new_y)

    def get_random_invader(self):
      front = self.__get_front_invaders()

      if len(front) == 0:
        return None

      # chose one random from the front
      index = random.randint(0, len(front)-1)
      front_invader = front[index]

      return front_invader

    def __get_front_invaders(self):
      row_index = len(self.invaders)-1

      front_invaders = []
      for i in range(self.columns):
        front_invaders.append(None)
      
      while row_index >= 0:
        row_invaders = self.invaders[row_index]

        for index, invader in enumerate(row_invaders):
          if( 
            not invader.is_exploding and
            front_invaders[index] is None
            ):
            front_invaders[index] = invader

        row_index -= 1

      for index, invader in enumerate(front_invaders):
        if invader is None:
          del front_invaders[index]

      return front_invaders