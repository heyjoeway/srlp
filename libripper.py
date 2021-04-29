# Level ripping library
# Converted from PHP to Python by heyjoeway
# Compiled by Techokami
# Use this for creating PHP scripts that work with Genesis graphics!
# Released under BSD license

from PIL import Image
import numpy as np
import math

#FUNCTIONS

#Read a 16-bit WORD from the file
def getWord(source, index):
	return (source[index] << 8) + source[index+1]


#Read a 16-bit WORD from the file with flipped endians
def getFWord(source, index):
	return source[index] + (source[index+1] << 8)


#Generate a 16-color Genesis/MD pallete
def makeGenPalette(source, source_index, gd, keeptrans=False):
	result = []
	for i in range(16):
		color = source[source_index]
		source_index += 1
		color2 = source[source_index]
		source_index += 1
		# Genesis pallete entries are words - 0B GR
		red = 17 * (color2 % 16)
		green = 17 * floor(color2 / 16)
		blue = 17 * (color % 16)
		if not keeptrans and (i == 0):
			result[i] = imagecolorallocate( gd, 255, 0, 255 )
		else:
			result[i] = imagecolorallocate( gd, red, green, blue )

	return result

#Generate a 16-color GBA pallete
def makeGBAPalette(source, source_index = 0, transparent = True):
	source_index = 0
	result = []
	for i in range(16):
		color = getFWord(source, source_index)
		source_index += 2
		# GBA pallete entries are words - 0bbb bbgg gggr rrrr
		# This function was written by Justin Aquadero (Retriever II)
		blue = ((color>>10)&31) << 3
		blue += blue >>5
		green = ((color>>5)&31) << 3
		green += green >>5
		red = ((color)&31) << 3
		red += red >>5
		# The above function was written by Justin Aquadero (Retriever II)
		result.append((red, green, blue, 0 if transparent and (i == 0) else 256))


	return result

#Generate a 256-color GBA pallete
def make8BitGBAPalette(source, source_index = 0, transparent = True):
	result = []
	for i in range(256):
		color = getFWord(source, source_index)
		source_index += 2

		# GBA pallete entries are words - 0bbb bbgg gggr rrrr
		# This function was written by Justin Aquadero (Retriever II)
		blue = ((color>>10)&31) << 3
		blue += blue >>5
		green = ((color>>5)&31) << 3
		green += green >>5
		red = ((color)&31) << 3
		red += red >>5
		# The above function was written by Justin Aquadero (Retriever II)
		result.append((red, green, blue, 0 if transparent and (i == 0) else 256))
	
	return result

#Build a set of 8x8 tiles (4bpp)
def make8x8Tiles(source, gd, pal, tileAddr, bigendian = True):
	source_index = tileAddr
	for i in range(256):
		for j in range(32):
			for y in range(8):
				for x in range(0,8,2):
					byte = source[source_index]
					source_index += 1
					# Split a byte into nybbles
					if bigendian:
						leftpixel = floor(byte / 16)
						rightpixel = (byte % 16)
					else:
						rightpixel = floor(byte / 16)
						leftpixel = (byte % 16)

					#Paint the two pixels
					# imagesetpixel(gd, x + (j * 8), y + (i * 8), pal[leftpixel]);
					# imagesetpixel(gd, x + 1 + (j * 8), y + (i * 8), pal[rightpixel]);

	return gd

#Build a set of 8x8 tiles (8bpp)
def make8bppTiles(source, pal, tileAddr = 0, rows = 48, cols = 32):
	source_index = tileAddr
	tiles = []
	while source_index < len(source):
		tile = Image.new('RGBA', (8,8))
		tiles.append(tile)
		for y in range(8):
			for x in range(8):		
				byte = source[source_index]
				source_index += 1
				tile.putpixel((x,y), pal[byte])
	
	return tiles

def generateTilesheet(tiles, width=32):
	mode = tiles[0].mode

	tile_width = tiles[0].width
	tile_height = tiles[0].height

	height = math.ceil(len(tiles) / width)
	img = Image.new(mode, (width * tile_width, height * tile_height))
	for i in range(len(tiles)):
		tile = tiles[i]
		col = i % width
		row = int(i / width)
		img.paste(tile, (col * tile_width, row * tile_height))

	return img