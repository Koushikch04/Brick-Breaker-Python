import numpy as np
import pyglet
import imageio

output = "S20210010048_Assignment2_BouncingBallAnimation.gif"
elapsed_time = 0.0
outputFrames = []
text = "Bouncing Ball Animation"
count = 0


class S20210010048Assignment2(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self, resizable=False)
        self.falling = True
        self.coefficientOfRestitution = 1
        self.ballSprite = None
        self.createDrawableObjects()
        self.adjustWindowSize()

    def createDrawableObjects(self):
        ballImage = pyglet.image.load('S20210010048_bouncing_ball.png')
        ballImage.anchor_x = ballImage.width // 2
        ballImage.anchor_y = ballImage.height // 2
        self.ballSprite = pyglet.sprite.Sprite(ballImage)
        self.ballSprite.position = (self.ballSprite.width / 4, self.ballSprite.height * (11 / 4), 0)

    def adjustWindowSize(self):
        w = self.ballSprite.width * 3
        h = self.ballSprite.height * 3
        self.width = w
        self.height = h

    def on_reset(self):
        self.ballSprite.position = (self.ballSprite.width / 4, self.ballSprite.height * (11 / 4), 0)

    def moveObjects(self, t):
        if self.falling:
            self.ballSprite.y -= 5
            self.ballSprite.rotation += self.coefficientOfRestitution * 5
        if self.ballSprite.y <= self.coefficientOfRestitution * (self.ballSprite.height // 5):
            self.falling = False
            self.coefficientOfRestitution *= 6 / 7
        if not self.falling:
            self.ballSprite.y += 5
            self.ballSprite.rotation += self.coefficientOfRestitution * 3
        if not self.falling and self.ballSprite.y >= (
                self.ballSprite.height * (11 / 4) * self.coefficientOfRestitution):
            self.falling = True
        if self.ballSprite.x >= self.width:
            self.falling = False
            self.coefficientOfRestitution = 1
            self.on_reset()
        self.ballSprite.x += 0.5

        # Saving animation frames
        global elapsed_time
        elapsed_time += t
        if elapsed_time >= 3 / 20:
            color_buffer = pyglet.image.get_buffer_manager().get_color_buffer()
            image_data = color_buffer.get_image_data()
            data = np.frombuffer(image_data.get_data('RGBA', color_buffer.width * 4), dtype=np.uint8)
            frame = data.reshape((image_data.height, image_data.width, 4))
            frame = np.flipud(frame)
            outputFrames.append(frame)
            elapsed_time = 0.0

    def on_draw(self):
        self.clear()
        self.ballSprite.draw()
        label = pyglet.text.Label(text, font_name='Cooper', font_size=15, x=35, y=self.width - 20)
        global count
        count += 1
        label.draw()
        print(count)


window = S20210010048Assignment2()
pyglet.gl.glClearColor(0.5, 0.5, 0.5, 1)
# called once every specifed time in seconds
pyglet.clock.schedule_interval(window.moveObjects, 0.50 / 20)
pyglet.app.run()
# saving the animation frames into a GIF file
imageio.mimsave(output, outputFrames)
