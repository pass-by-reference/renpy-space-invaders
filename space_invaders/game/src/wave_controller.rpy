init python:

  INITIAL_ROW = 1
  INITIAL_COLUMN = 0
  MAX_ROW = 5
  MAX_COLUMN = 5

  INITIAL_SPEED = 10
  MAX_SPEED = 100

  INITIAL_SHOOT_INTERVAL = 1
  MAX_SHOOT_INVERVAL = 10

  class WaveController:
    """
    Controls the waves.
    """

    class WaveScaling:
      """ 
      Sets the attributes in InvaderManager according to wave number
      """
      def __init__(self):
        pass

      def get_rows(self, wave):
        # Add a row every 3 waves after wave 3
        if(wave > 3):
          increment = int((wave-3)/3)
          return min(INITIAL_ROW + increment, MAX_ROW)

        return 1

      def get_columns(self,wave):
        # Add a column every wave between wave 1 and 4
        return min(INITIAL_COLUMN + wave, MAX_COLUMN)

      def get_speed(self,wave):
        return min(INITIAL_SPEED + wave*5, MAX_SPEED)

      def get_shoot_interval(self,wave):
        # Increase every two waves
        increment = int(wave/2)
        return min(INITIAL_SHOOT_INTERVAL+increment, MAX_SHOOT_INVERVAL)

    def __init__(self, time_between_waves):
      self.invader_manager = None
      self.timer = Timer(time_between_waves)

      self.in_wave_transition = False
      self.wave = 1
      self.ws = self.WaveScaling()

    def is_wave_completed(self):
      if(
        self.invader_manager.destroyed == 
        self.invader_manager.rows * self.invader_manager.columns
      ):
        return True

      return False

    def get_new_manager(self):
      wave = self.wave
      ivd_man_builder = InvaderManagerBuilder()

      ivd_man_builder.rows = self.ws.get_rows(wave)
      ivd_man_builder.columns = self.ws.get_columns(wave)

      ivd_man_builder.exploding_time = 0.2
      ivd_man_builder.speed = self.ws.get_speed(wave)
      ivd_man_builder.shoot_interval = self.ws.get_shoot_interval(wave)

      ivd_man_builder.set_invader_positions(x=100,y=150)
      ivd_man_builder.set_invader_size(width=48,height=32)
      ivd_man_builder.set_invader_padding(x_padding=200,y_padding=100)

      self.invader_manager = InvaderManager(ivd_man_builder, self.wave)
      return self.invader_manager
