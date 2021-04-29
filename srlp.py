# Sonic Rush Level Parser
# Converted from PHP to Python by heyjoeway
# Original description below:
# By Techokami
# Big thanks to JoseTB!
# MP file format
# 0x0000 - X dimension (little endian)
# 0x0002 - Y dimension (little endian)
# 0x0004 to EOF - Metatile ID (little endian)
# _a is the upper layer, _b is the lower layer

import ndspy.rom
import ndspy.narc
import ndspy.lz10
import libripper
from PIL import Image, ImageOps, ImageChops
import os
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path to the ROM file (any Rush game)")
parser.add_argument("stage", help="Stage ID (ex. first act of first zone would be \"z11\")")
parser.add_argument("--tiles", help="Path to output tiles")
parser.add_argument("--chunks", help="Path to output chunks")
parser.add_argument("--amap", help="Path to output map A (high map)")
parser.add_argument("--bmap", help="Path to output map B (low/default map)")
parser.add_argument("--map", help="Path to output composited map")
args = parser.parse_args()

# What shall we be ripping today?
rom = ndspy.rom.NintendoDSRom.fromFile(args.path)

# Next, the map data. Ex. z11 is the first act of the first zone.
stage = args.stage
stage_map_narc = ndspy.narc.NARC(
	rom.getFileByName("narc/" + stage + "_map.narc")
)
stage_raw_narc = None
try:
	stage_raw_narc = ndspy.narc.NARC(
		rom.getFileByName("narc/" + stage + "_raw.narc")
	)
except:
	pass

# Load the mapping data
stage_amap_data_lz10 = stage_map_narc.getFileByName(stage + "_a.mp")
stage_amap_data = ndspy.lz10.decompress(stage_amap_data_lz10)
stage_bmap_data_lz10 = stage_map_narc.getFileByName(stage + "_b.mp")
stage_bmap_data = ndspy.lz10.decompress(stage_bmap_data_lz10)

# Graphics data
if stage_raw_narc:
	stage_graphics_data_lz10 = stage_raw_narc.getFileByName(stage + ".ch")
	stage_metatile_data_lz10 = stage_raw_narc.getFileByName(stage + ".bk")
else:
	stage_graphics_data_lz10 = stage_map_narc.getFileByName(stage + ".ch")
	stage_metatile_data_lz10 = stage_map_narc.getFileByName(stage + ".bk")

stage_graphics_data = ndspy.lz10.decompress(stage_graphics_data_lz10)
stage_metatile_data = ndspy.lz10.decompress(stage_metatile_data_lz10)

# Palette data
stage_palette_data_lz10 = stage_map_narc.getFileByName(stage + ".pl")
stage_palette_data = ndspy.lz10.decompress(stage_palette_data_lz10)
stage_palette = libripper.make8BitGBAPalette(stage_palette_data)

# Build the 8x8 tile images
stage_tiles = libripper.make8bppTiles(
	stage_graphics_data,
	stage_palette
)

def generateMetatiles(stage_metatile_data, stage_tiles):
	# So, how many metatiles will we be building?
	stage_metatile_count = int(len(stage_metatile_data) / 128)
	stage_metatiles = []

	# Okay we got the tiles!  Let's start building the Map64.
	source_index = 0
	for j in range(stage_metatile_count):
		metatile = Image.new('RGBA', (64, 64))
		stage_metatiles.append(metatile)
		for y in range(8):
			for x in range(8):
				tileParams = libripper.getFWord(stage_metatile_data, source_index)
				source_index += 2

				# PPPP XYAA AAAA AAAA
				# 1111 0000 0000 0000 - 0x6000 - determine pallete
				tilepallete = math.floor((tileParams & 0xF000)/4096);
				# 0000 1000 0000 0000 - 0x0800 - determine X flip
				tileyflip = math.floor((tileParams & 0x800)/2048);
				# 0000 0100 0000 0000 - 0x0400 - determine Y flip
				tilexflip = math.floor((tileParams & 0x400)/1024);
				# 0000 0111 1111 1111 - 0x03FF - get tile ID
				tileID = tileParams & 0x03FF;
				tile = stage_tiles[tileID]
				
				if tileyflip:
					tile = ImageOps.flip(tile)

				if tilexflip:
					tile = ImageOps.mirror(tile)
				
				metatile.paste(tile, (x * 8, y * 8))

	return stage_metatiles

def generateMap(stage_map_data, stage_metatiles):
	# How big are the images going to be?
	stage_map_dimx = libripper.getFWord(stage_map_data,0)
	stage_map_dimy = libripper.getFWord(stage_map_data,2)

	stage_map_dims = (
		stage_map_dimx * 64,
		stage_map_dimy * 64
	)
	stage_map_img = Image.new('RGBA', stage_map_dims)

	source_index = 4
	for y in range(stage_map_dimy):
		for x in range(stage_map_dimx):
			map_currentTileIndex = libripper.getFWord(
				stage_map_data,
				source_index
			)
			source_index += 2

			map_currentTile = stage_metatiles[map_currentTileIndex]

			stage_map_img.paste(
				map_currentTile,
				(x * 64, y * 64)
			)

	return stage_map_img

if args.tiles:
	libripper.generateTilesheet(stage_tiles).save(args.tiles)

if args.chunks or args.amap or args.bmap or args.map:
	stage_metatiles = generateMetatiles(stage_metatile_data, stage_tiles)

	if args.chunks:
		libripper.generateTilesheet(stage_metatiles).save(args.chunks)

	stage_amap_img = None
	stage_bmap_img = None

	if args.amap or args.map:
		stage_amap_img = generateMap(stage_amap_data, stage_metatiles)
		if args.amap:
			stage_amap_img.save(args.amap)
	
	if args.bmap or args.map:
		stage_bmap_img = generateMap(stage_bmap_data, stage_metatiles)
		if args.bmap:
			stage_bmap_img.save(args.bmap)

	if args.map:
		stage_map_img = stage_bmap_img.copy()
		stage_map_img.paste(stage_amap_img, (0,0), stage_amap_img)
		stage_map_img.save(args.map)