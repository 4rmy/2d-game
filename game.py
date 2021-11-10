import os, pygame, numpy, time, colorama, noise
from chunk import Chunk
import win32gui, win32con

class Game():
    # Init class values
    def __init__(self, seed, errorLog=False):

        if errorLog == False:
            hide = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hide , win32con.SW_HIDE)
            self.debug = False
        else:
            self.debug = True

        try:
            command = 'clear'
            if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
                command = 'cls'
            os.system(command)
        except:
            self.log("CLEAR PROMT COMMAND FAILED", error=True)
        
        colorama.init()

        self.world = []
        self.ChunkList = []
        self.chunkOffset = 0
        self.seed = seed
        self.furthestGen = 0
        self.nearestGen = 0
        self.firstRender = 0
        self.tempCNum = 0
        self.camX = 0
        self.camY = 0
        self.speed = 5
        self.chunksRendered = 0

        self.log("    Game initialization    ")
        self.log("---=========Log=========---")
        self.log("")

    # Custom Timed Logging System
    def log(self, msg, error = False):
        msg = str(msg)

        curTime = time.localtime()

        # Format : [<hour>:<min>:<sec>] <message>
        if self.debug:
            if error == False:
                print(colorama.Fore.WHITE + "[" + str(curTime.tm_hour) + ":" + str(curTime.tm_min) + ":" + str(curTime.tm_sec) + "] " + colorama.Fore.CYAN + msg + colorama.Fore.WHITE)
            else:
                print(colorama.Fore.WHITE + "[" + str(curTime.tm_hour) + ":" + str(curTime.tm_min) + ":" + str(curTime.tm_sec) + "] " + colorama.Fore.RED + "ERROR: " + msg + colorama.Fore.WHITE)
                input("Press enter to continue...")
    
    # Render All Chunks (Can be optimized by not rendering chunks offscreen)
    def render(self, display, tilesize, w, h):
        # Loop world chunks
        for c in range(len(self.world)):
            # Loop through chunk map height
            for y in range(len(self.world[c].map)):
                # Loop through chunk map width
                for x in range(len(self.world[c].map[y])):
                    # Draw square based on color and tile size
                    pygame.draw.rect(display, self.world[c].map[y][x], ((x*tilesize) + (self.world[c].x * tilesize * len(self.world[c].map[y])) + self.camX, (y*tilesize) + (self.world[c].y * tilesize * len(self.world[c].map)) + self.camY, tilesize, tilesize))
        
    # Chunk Generation
    def genChunk(self, cx, cy, cw, ch, seed):
        # Create basic chunk
        self.chunk = Chunk(cx,cy,[[0 for i in range(cw)] for j in range(ch)])

        # Generate Map Values
        for y in range(len(self.chunk.map)):
            for x in range(len(self.chunk.map[y])):
                self.chunk.map[y][x] = noise.pnoise2(
                                                        (y + (cy * ch) + (100 * seed)) /100,
                                                        (x + (cx * cw) + (100 * seed)) /100,
                                                        octaves=6,
                                                        persistence=0.5,
                                                        lacunarity=2.0,
                                                        repeatx=99999999,
                                                        repeaty=99999999,
                                                        base=0)

        # Parse map values and set state of block
        # Color values
        water = (0, 82, 214)
        sand = (188, 219, 125)
        grass = (36, 163, 49)
        lowStone = (87, 87, 87)
        medStone = (130,130,130)
        hiStone = (166, 166, 166)
        Snow = (227, 227, 227)
        #loop through values and set position rgb

        for y in range(len(self.chunk.map)):
            for x in range(len(self.chunk.map[y])):
                if self.chunk.map[y][x] < 0.0000000005:
                    self.chunk.map[y][x] = water
                elif self.chunk.map[y][x] < 0.025:
                    self.chunk.map[y][x] = sand
                elif self.chunk.map[y][x] < 0.1:
                    self.chunk.map[y][x] = grass
                elif self.chunk.map[y][x] < 0.15:
                    self.chunk.map[y][x] = lowStone
                elif self.chunk.map[y][x] < 0.2:
                    self.chunk.map[y][x] = medStone
                elif self.chunk.map[y][x] < 0.3:
                    self.chunk.map[y][x] = hiStone
                else:
                    self.chunk.map[y][x] = Snow

        self.ChunkList.append(self.chunk)
        self.log("Generated new Chunk: Chunk(x: " + str(self.chunk.x) + ", y: " + str(self.chunk.y) + ")")
        self.chunk = {}
    
    # Try to generate a chunk if the view is not full of chunks
    def tryChunkGen(self):
        pass