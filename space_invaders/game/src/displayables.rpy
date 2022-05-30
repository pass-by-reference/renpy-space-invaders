init python:
  class GameDisplayable:
    def __init__(self, width, height):
      self.display = None
      self.width = width
      self.height = height

      self.x = 0
      self.y = 0

    def set_pos(self, x, y):
      self.x = x
      self.y = y

    def draw(self, draw_args):
      render = draw_args.render
      st = draw_args.shown_timebase
      at = draw_args.animation_timebase

      if(self.display != None):
        child_render = renpy.render(self.display,self.width,self.height,st,at)
        render.blit(child_render, (self.x, self.y))
      else:
        print("No displayable")

  class BoxDisplayable(GameDisplayable):
    def __init__(self, color, width, height):
      super(BoxDisplayable,self).__init__(width,height)

      self.color = color
      self.display = Solid(color, xsize=width,ysize=height)

  class TextDisplayable(GameDisplayable):

    def __init__(self, text, width, height):
      super(TextDisplayable, self).__init__(width, height)

      self.text = text
      self.display = Text(text)

    def draw(self, draw_args, text):

      render = draw_args.render
      st = draw_args.shown_timebase
      at = draw_args.animation_timebase
      
      if isinstance(text,float):
        text = round(text, 2)

      if(self.text != text):
        self.text = str(text)
        self.display = Text(str(text))

      child_render = renpy.render(self.display,self.width,self.height,st,at)
      render.blit(child_render, (self.x, self.y))

  class ImageDisplayable(GameDisplayable):

    def __init__(self, src, width,height):
      super(ImageDisplayable,self).__init__(width, height)
      self.display = Image(src, xsize=width, ysize=height)

    def has_collided(self, obj):
      if(
        obj.x >= self.x and
        obj.x <= self.x + self.width and
        obj.y >= self.y and
        obj.y <= self.y + self.height
      ):
        return True
      
      return False