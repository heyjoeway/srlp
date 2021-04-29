import argparse
import srlp
import os

stages_rush = [
	"z11", "z12", "z13",
	"z21", "z22", "z23",
	"z31", "z32", "z33",
	"z41", "z42", "z43",
	"z51", "z52", "z53",
	"z61", "z62", "z63",
	"z71", "z72", "z73",
	"z81", "z82",
	"z91", "z92", 
	"zf3"
]

stages_ra = [
	"z11", "z12", "z1t", "z1boss",
	"z21", "z22", "z2boss",
	"z31", "z32", "z3boss",
	"z41", "z42", "z4boss",
	"z51", "z52", "z5boss",
	"z61", "z62", "z6boss",
	"z71", "z72", "z7boss",
	"z8boss", 
	"z91"
]

stages_ra_weird = [ "z92", "z93", "z94" ]

stages_colors = [
	"rz11", "rz12", "rz13",
	"rz21", "rz22", "rz23",
	"rz31", "rz32", "rz33",
	"rz41", "rz42", "rz43",
	"rz51", "rz52", "rz53",
	"rz61", "rz62", "rz63",
	"zt1", "zt2", "zt3", "zt4", "zt5", "zt6", "zt7",
	"z11", "z12", "z1boss",
	"z21", "z22", "z2boss",
	"z31", "z32", "z3boss",
	"z41", "z42", "z4boss",
	"z51", "z52", "z5boss",
	"z61", "z62", "z6boss",
	"z71", "z7boss"
]

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--rush", help="Path to Rush ROM file")
	parser.add_argument("--ra", help="Path to Rush Adventure ROM file")
	parser.add_argument("--colors", help="Path to Colors ROM file")
	args = parser.parse_args()

	if args.rush:
		for stage_id in stages_rush:
			stage_path = "./output/Rush/" + stage_id + "/"
			try:
				os.makedirs(stage_path)
				srlp.extract({
					"path": args.rush,
					"stage": stage_id,
					"tiles": stage_path + "tiles.png",
					"chunks": stage_path + "chunks.png",
					"amap": stage_path + "amap.png",
					"bmap": stage_path + "bmap.png",
					"map": stage_path + "map.png"
				})
			except:
				pass

	if args.ra:
		for stage_id in stages_ra:
			stage_path = "./output/RushAdventure/" + stage_id + "/"
			try:
				os.makedirs(stage_path)
				srlp.extract({
					"path": args.ra,
					"stage": stage_id,
					"tiles": stage_path + "tiles.png",
					"chunks": stage_path + "chunks.png",
					"amap": stage_path + "amap.png",
					"bmap": stage_path + "bmap.png",
					"map": stage_path + "map.png"
				})
			except:
				pass

		for stage_id in stages_ra_weird:
			stage_path = "./output/RushAdventure/" + stage_id + "/"
			try:
				os.makedirs(stage_path)
				srlp.extract({
					"path": args.ra,
					"stageRaw": "z91",
					"stage": stage_id,
					"tiles": stage_path + "tiles.png",
					"chunks": stage_path + "chunks.png",
					"amap": stage_path + "amap.png",
					"bmap": stage_path + "bmap.png",
					"map": stage_path + "map.png"
				})
			except:
				pass

	if args.colors:
		for stage_id in stages_colors:
			stage_path = "./output/Colors/" + stage_id + "/"
			try:
				os.makedirs(stage_path)
				srlp.extract({
					"path": args.colors,
					"stage": stage_id,
					"tiles": stage_path + "tiles.png",
					"chunks": stage_path + "chunks.png",
					"amap": stage_path + "amap.png",
					"bmap": stage_path + "bmap.png",
					"map": stage_path + "map.png"
				})
			except:
				pass