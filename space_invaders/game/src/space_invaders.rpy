init python:
  import pygame
  import random
  from itertools import chain

  SHIP_IMAGE = "Ship.png"

  SCREEN_WIDTH = 1920
  SCREEN_HEIGHT = 1080

  class Invader(GameDisplayable):
    def __init__(self, src, time, width, height):
      super(Invader,self).__init__(width,height)

      self.is_destroyed = False
      self.is_exploding = False
      self.exploding_timer = Timer(time)

      self.color = color
      self.display = Image(src, xsize=width, ysize=height)

    def has_collided(self, bullet):
      if(
        bullet.x >= self.x and
        bullet.x <= self.x + self.width and
        bullet.y >= self.y and
        bullet.y <= self.y + self.height
      ):
        return True
      
      return False

    def should_remove(self, st):
      if self.exploding_timer.start:
        elapsed, time_left = self.exploding_timer.has_time_elapsed(st)

        return elapsed
      else:
        return False

    def switch_exploding(self,st):
      self.display = Image(EXPLODING_IMAGE, xsize=40, ysize=30)
      self.is_exploding = True
      self.exploding_timer.start_time(st)
  
  class SpaceInvaders(renpy.Displayable):

    class DrawArguments:
      def __init__(self,render, shown_timebase, animation_timebase):
        self.render = render
        self.shown_timebase = shown_timebase
        self.animation_timebase = animation_timebase

    def __init__(self, **kwargs):
      super(SpaceInvaders, self).__init__(kwargs)

      self.window_width = SCREEN_WIDTH
      self.window_height = SCREEN_HEIGHT

      self.player_ship = ImageDisplayable(SHIP_IMAGE, 60,32)
      self.time_display = TextDisplayable("",300,40)
      self.score_display = TextDisplayable("",200,40)
      self.wave_display = TextDisplayable("", 500, 30)
      self.delta_time = DeltaTime()

      self.bullet_speed = 500
      self.player_lost = False
      self.score = 0

      self.player_bullets_manager = self.create_player_bullet_manager()
      self.invader_bullets_manager = self.create_invader_bullet_manager()

      self.wave_controller = WaveController(time_between_waves=5)
      self.invader_manager = None # Insantiation handled in wave controller

      # Create ship and invaders and set their positions
      self.set_player_ship_initial_pos()

      self.score_display.set_pos(self.window_width-500, 50)
      self.time_display.set_pos(self.window_width-300, 50)
      self.wave_display.set_pos((self.window_width/2)-(self.wave_display.width/4),self.window_height/3)

    def create_player_bullet_manager(self):
      bullet_builder = BulletManagerBuilder()

      bullet_builder.bullet_speed = self.bullet_speed
      bullet_builder.max_bullets = 2
      bullet_builder.x_offset = 0
      bullet_builder.y_offset = 20
      bullet_builder.direction = -1
      bullet_builder.y_bounds_limit = 50
      bullet_builder.bullet_color = "#ffffff"

      return BulletManager(bullet_builder)

    def create_invader_bullet_manager(self):
      bullet_builder = BulletManagerBuilder()

      bullet_builder.bullet_speed = self.bullet_speed
      bullet_builder.max_bullets = 5
      bullet_builder.x_offset = 0
      bullet_builder.y_offset = -10
      bullet_builder.direction = 1
      bullet_builder.y_bounds_limit = self.window_height
      bullet_builder.bullet_color = "#ff0000"

      return BulletManager(bullet_builder)

    def set_player_ship_initial_pos(self):
      x = (self.window_width-self.player_ship.width)/2
      y = self.window_height - 100

      self.player_ship.set_pos(x,y)

    def bullet_collision_invader(self,st):
      invaders = list(chain.from_iterable(self.invader_manager.invaders))
      bullets = self.player_bullets_manager.bullets

      for invader in invaders:
        for bullet_index, bullet in enumerate(bullets):
          if(
            not invader.is_destroyed and
            not invader.is_exploding and
            invader.has_collided(bullet)):

              self.invader_manager.destroyed += 1
              del bullets[bullet_index]
              invader.switch_exploding(st)

    def handle_invader_shoot(self, st):
      if self.invader_bullets_manager.has_time_elapsed_to_shoot(st):
        invader = self.invader_manager.get_random_invader()

        if invader is not None:
          self.invader_bullets_manager.shoot_bullet(invader, st)
      else:
        return

    def bullet_collision_player(self):
      bullets = self.invader_bullets_manager.bullets

      for bullet in bullets:
        if self.player_ship.has_collided(bullet):
          renpy.timeout(0)
          self.player_lost = True

    def get_score(self):
      return self.score + self.invader_manager.destroyed
    
    def draw_wave_message(self, draw_args, st):

      wave_number = self.wave_controller.wave
      elapsed, time_left = self.wave_controller.timer.has_time_elapsed(st)

      if(
        self.wave_controller.in_wave_transition and
        elapsed is False
      ):
        time_left = str(round(time_left,2))
        self.wave_display.draw(
          draw_args, 
          "Wave " + str(wave_number+1) + " in " + time_left
        )
    
    def wave_driver(self, st):
      wc = self.wave_controller

      if self.invader_manager is None:
        self.invader_manager = wc.get_new_manager()

      if(
        wc.is_wave_completed() and 
        wc.in_wave_transition is False
      ):
        wc.in_wave_transition = True
        wc.timer.start_time(st)

      has_elapsed, time_left = wc.timer.has_time_elapsed(st)
      if(
        wc.in_wave_transition and
        has_elapsed
      ):
        wc.wave += 1
        wc.in_wave_transition = False

        self.score += self.invader_manager.destroyed
        self.invader_manager = wc.get_new_manager()
    
    def render(self, width,height,st,at):
      self.delta_time.set_delta_time(st)  
      render = renpy.Render(self.window_width, self.window_height)

      draw_args = self.DrawArguments(render,st,at)

      self.wave_driver(st)
      self.handle_invader_shoot(st)

      self.player_ship.draw(draw_args)
      self.player_bullets_manager.draw_bullets(draw_args, self.delta_time.dtime)
      self.invader_bullets_manager.draw_bullets(draw_args, self.delta_time.dtime)

      self.invader_manager.move_invaders(self.delta_time.dtime)
      self.invader_manager.draw_invaders(draw_args)
      self.invader_manager.remove_invaders(st)

      self.bullet_collision_invader(st)
      self.bullet_collision_player()

      self.time_display.draw(draw_args, "Time: " + str(round(st,2)))
      self.score_display.draw(draw_args, "Score: " + str(self.get_score()))
      self.draw_wave_message(draw_args, st)
      renpy.redraw(self,0)

      return render 

    def event(self,ev,x,y,st):

      if(self.player_lost):
        return False, {
          "score": self.get_score(),
          "time": round(st,2),
          "wave": self.wave_controller.wave
        }
      
      if(ev.type == pygame.MOUSEBUTTONDOWN):
        self.player_bullets_manager.shoot_bullet(self.player_ship, st)
      
      self.player_ship.set_pos(x, self.player_ship.y)

      raise renpy.IgnoreEvent()