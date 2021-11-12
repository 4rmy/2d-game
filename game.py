import os, pygame, time, colorama, noise
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

        self.world = [[0 for x in range(4)] for y in range(4)]
        self.ChunkList = []
        self.chunkOffX = 0
        self.chunkOffY = 0
        self.seed = seed
        self.furthestGen = 0
        self.nearestGen = 0
        self.firstRender = 0
        self.tempCNum = 0
        self.camX = 0
        self.camY = 0
        self.speed = 5
        self.chunksRendered = 0
        self.chunkDir = "chunks\\"

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
        
        # Create Temp world
        tempMap = self.world

        # loop through chunk y values
        for cy in range(len(tempMap)):
            # loop through chunk x values
            for cx in range(len(tempMap[cy])):
                # store chunk into temp storage
                tempChunk = tempMap[cy][cx]
                # parse chunk heights
                tempChunk = tempChunk.split('\n')
                # remove extra line
                tempChunk = tempChunk[:-1]
                # loop through chunk height
                for y in range(len(tempChunk)):
                    # split height by tile
                    tempChunk[y] = tempChunk[y].split(',')
                    # loop through tiles in that height
                    for x in range(len(tempChunk[y])):
                        # create color values
                        water = (0, 82, 214)
                        sand = (188, 219, 125)
                        grass = (36, 163, 49)
                        lowStone = (87, 87, 87)
                        medStone = (130,130,130)
                        hiStone = (166, 166, 166)
                        Snow = (227, 227, 227)
                        # parse chunk values
                        if tempChunk[y][x] == "0":
                            color = water
                        elif tempChunk[y][x] == "1":
                            color = sand
                        elif tempChunk[y][x] == "2":
                            color = grass
                        elif tempChunk[y][x] == "3":
                            color = lowStone
                        elif tempChunk[y][x] == "4":
                            color = medStone
                        elif tempChunk[y][x] == "5":
                            color = hiStone
                        elif tempChunk[y][x] == "6":
                            color = Snow
                        # draw tile to the display
                        pygame.draw.rect(display, color, pygame.Rect(x * tilesize + (cx * tilesize * 50), y * tilesize + (cy * tilesize * 50), tilesize, tilesize))
                        
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
        water = "0"
        sand = "1"
        grass = "2"
        lowStone = "3"
        medStone = "4"
        hiStone = "5"
        Snow = "6"
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

        data = ""
        f = open(self.chunkDir + str(self.chunk.x) + "-" + str(self.chunk.y) + ".txt", "a")
        for y in range(len(self.chunk.map)):
            line = ""
            for x in range(len(self.chunk.map[y])):
                if x != 0:
                    line += "," + str(self.chunk.map[y][x])
                else:
                    line += str(self.chunk.map[y][x])

            data += line + "\n"
        f.write(data)
        f.close
        
        self.log("Generated new Chunk: Chunk(x: " + str(self.chunk.x) + ", y: " + str(self.chunk.y) + ")")
        self.chunk = {}
    
    # Try to generate a chunk if the view is not full of chunks
    def tryChunkGen(self):
        chunktest = True
        exist = False
        for y in range(4):
            for x in range(4):
                exist = False
                for file in os.listdir(self.chunkDir):
                    file = file.split(".txt")
                    file = file[0]
                    file = file.split("-")
                    if int(file[0]) == x + self.chunkOffX:
                        if int(file[1]) == y + self.chunkOffY:
                            exist = True
                            f = open(self.chunkDir + file[0] + "-" + file[1] + ".txt", "r")
                            self.world[y][x] = f.read()
                if exist == False:
                    chunktest = False
                    self.log("Chunk not found at x:" + str(x) + ", y:" + str(y))
                    self.genChunk(x + self.chunkOffX, y + self.chunkOffY, 50, 50, self.seed)
        return chunktest