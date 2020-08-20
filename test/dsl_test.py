import sys
import sdl2
import sdl2.ext

sdl2.ext.init()

window = sdl2.ext.Window("Hello World!", size=(640, 480))
window.show()

processor = sdl2.ext.TestEventProcessor()
processor.run(window)

sdl2.ext.quit()
