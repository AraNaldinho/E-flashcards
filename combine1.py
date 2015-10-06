import os,pyglet
animals = os.listdir('animals')
sound = os.listdir('sound')
images = []
for name in animals:
    filename,extension = os.path.splitext(name)
    images.append(filename)
print images
soundlist = []
for name in sound:
    filename,extension = os.path.splitext(name)
    soundlist.append(filename)
print soundlist

for img in images:
    for snd in soundlist:
        if img == snd:
            animal = 'sound/'+snd+'.mp3'
            music = pyglet.media.load(animal)
            music.play()
            def exiter(dt):
                pyglet.app.exit()
            pyglet.clock.schedule_once(exiter,music.duration)
            pyglet.app.run()
            