#import os
import layoutinfo

def generateDatafiles(all_rooms, all_doors, offset, layout, out_dir, layout_string):
	txt_string = ""
	txt_base = layoutinfo.txt[layout]
	#these were +offset
	x_offset, y_offset = txt_base[0] + offset[0], txt_base[1] + offset[1]
	ellipse = txt_base[2]
	txt_string += "X_OFFSET\n%i\nY_OFFSET\n%i\nVERTICAL\n0\n%s\n"%(x_offset, y_offset, ellipse)
	for i, room in enumerate(all_rooms):
		txt_string += "ROOM\n%i\n%i\n%i\n%i\n%i\n"%(i, room.coords[0], room.coords[1], room.dimensions[0], room.dimensions[1])
	for door in all_doors:
		roomB_i = -1 if door.roomB is None else all_rooms.index(door.roomB)
		txt_string += "DOOR\n%i\n%i\n%i\n%i\n%i\n"%(door.position[0], door.position[1], all_rooms.index(door.roomA), roomB_i, door.vertical)

	with open("%s/%s.txt"%(out_dir, layout_string), "w+") as f:
		f.write(txt_string)

	floor_offset = layoutinfo.floor_offset[layout]
	with open("data_originals/%s.xml"%layout, "r") as f_in:
		xml_string = ""
		for line in f_in:
			is_relevant = 0
			if line[:4] == "<img":
				is_relevant = 1
			elif line[:7] == "\t<floor":
				is_relevant = 2
			if is_relevant > 0:
				sign = [0, -1, 1][is_relevant]
				new_line = ""
				lis = line.split(" ")
				for arg in lis:
					new_arg = arg
					yay = arg.split("=")
					if len(yay) == 2:
						if yay[0] == "x":
							tmp = yay[1].split("/")
							old_x = int(tmp[0][1:-1])
							X_diff = x_offset - txt_base[3]
							new_x = old_x + sign * (X_diff * 35)
							if is_relevant == 2:
								new_x += floor_offset[0]
							new_arg = 'x="%s"'%str(new_x)
							if len(tmp) > 1:
								new_arg += "/" + tmp[1]
						elif yay[0] == "y":
							tmp = yay[1].split("/")
							old_y = int(tmp[0][1:-1])
							Y_diff = y_offset - txt_base[4]
							new_y = old_y + sign * (Y_diff * 35)
							if is_relevant == 2:
								new_y += floor_offset[1]
							new_arg = 'y="%s"'%str(new_y)
							if len(tmp) > 1:
								new_arg += "/" + tmp[1]
					new_line += new_arg + " "
				xml_string += new_line
			else:
				xml_string += line
	with open("%s/%s.xml"%(out_dir, layout_string), "w+") as f_out:
		f_out.write(xml_string)


