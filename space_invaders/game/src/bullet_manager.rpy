init python:
  class BulletManagerBuilder:
    """
    A class to help build a BulletManager object.
    """
    def __init__(self):
      self.bullet_speed = 0
      self.max_bullets = 0
      self.x_offset = 0
      self.y_offset = 0
      self.direction = "right"
      self.y_bounds_limit = 0
      self.bullet_color = "#000000"
  
  class BulletManager:
    """
    BulletManager handles the bullets shot from either player or by 
    an invader. 
    """
    def __init__(self, bullet_man_builder):
      self.bullets = []

      self.bullet_speed = bullet_man_builder.bullet_speed
      self.max_bullets = bullet_man_builder.max_bullets
      # Offset is used to tune where the bullet appears when
      # fired by an invader or player. This is so the bullet is centered 
      # on screen.
      self.x_offset = bullet_man_builder.x_offset
      self.y_offset = bullet_man_builder.y_offset
      self.direction = bullet_man_builder.direction
      # y_bounds_limit is used to calculate when to make bullet disappear
      self.y_bounds_limit = bullet_man_builder.y_bounds_limit
      self.bullet_color = bullet_man_builder.bullet_color

      self.last_time_shot = None
      self.time_between_shot = 0.3

    def shoot_bullet(self, ship, st):

      self.last_time_shot = st

      if len(self.bullets) >= self.max_bullets:
        return

      if ship is None:
        return

      bullet = BoxDisplayable(self.bullet_color, ship.width/10, ship.height)

      initial_x = ship.x + (ship.width/2) - self.x_offset
      initial_y = ship.y - self.y_offset

      bullet.set_pos(initial_x, initial_y)
      self.bullets.append(bullet)

    def has_time_elapsed_to_shoot(self, st):
      if self.last_time_shot is None:
        self.last_time_shot = st

      if st > self.last_time_shot + self.time_between_shot:
        return True
      else:
        return False

    def move_bullet(self, bullet, dtime):
      move_distance = self.bullet_speed * dtime * self.direction

      new_x = bullet.x
      new_y = bullet.y + move_distance
      bullet.set_pos(new_x, new_y)

    def bullet_out_bounds(self, bullet, i):
      if(self.y_bounds_limit < 500 and bullet.y < self.y_bounds_limit):
        del self.bullets[i]
        return

      if(self.y_bounds_limit > 500 and bullet.y > self.y_bounds_limit):
        del self.bullets[i]
        return

    def draw_bullets(self,draw_args,dtime):
      for i, bullet in enumerate(self.bullets):
        self.move_bullet(bullet,dtime)

        bullet.draw(draw_args)

        self.bullet_out_bounds(bullet, i)