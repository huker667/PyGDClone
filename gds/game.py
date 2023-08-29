from ursina import *

app = Ursina(development_mode = True)


player = Entity(
	model = 'quad',
	collider = 'box',
	texture = 'assets/Cube011.png',
	scale = (3, 3, 3),
    y = 0,
    x = -10
	)
pmode = 0
x = 0
y = 0
start_lvl = 0
endtrg = ""
bgtrgs = []
camera.orthographic = True
camera.fow = 18
diam = []
plates = []
gds = ''
level_file = ''
pause = 1
player_speeded = 0
def lvlload():
	global start_lvl
	global pmode
	global level_file
	global diam
	global gds
	global y
	global x
	global pause
	global player_speeded
	global plates
	global endtrg
	start_lvl = 0
	camera.x = 10
	camera.y = 6
	diam = []
	plates = []
	standartent = []
	level_file = open("level_editor.gdl", "r")
	lines = 0
	words = 0
	symbols = 0
	pause = 1
	for line in level_file:
	    lines += 1
	    words += len(line.split())
	    symbols += len(line.replace(' ', ''))
	level_file.close()
	lines = lines + 1
	level_file = open("level_editor.gdl", "r")
	for _ in range(lines):
		linelvl_file = level_file.readline()
		if linelvl_file.startswith('PlayerSpeed:'):
			linelvl_file = level_file.readline()
			player_speeded = float(linelvl_file.replace("\n", ""))

			linelvl_file = level_file.readline()
			pmode = float(linelvl_file.replace("\n", ""))
		elif linelvl_file.startswith('CreateStartAudio:'):
			linelvl_file = level_file.readline()
			audio_string = linelvl_file.replace("\n", "")
			linelvl_file = level_file.readline()
			Loop_bool = linelvl_file.replace("\n", "")
			if Loop_bool.startswith('True'):
				gds = Audio(audio_string, loop = True)
			elif Loop_bool.startswith('False'):
				gds = Audio(audio_string)
		elif linelvl_file.startswith('CreateObject:'):
			linelvl_file = level_file.readline()
			if linelvl_file.startswith('Spike'):
				linelvl_file = level_file.readline()
				print(linelvl_file)
				xed = float(linelvl_file.replace("\n",""))
				linelvl_file = level_file.readline()
				yed = float(linelvl_file.replace("\n",""))
				linelvl_file = level_file.readline()
				zrt = float(linelvl_file.replace("\n",""))
				new1 = Entity(
					model = 'quad',
					y = yed,
					texture = 'assets/RegularSpike01.png',
					x = xed,
					scale = (3, 3, 3),
					rotation_z = zrt)
		
				new2 = duplicate(
					new1, y = yed,
					x = xed, scale = 0.1, color = color.red, collider = 'mesh')
		
				diam.extend((new1, new2))
			elif linelvl_file.startswith("NoHB Platform"):
				linelvl_file = level_file.readline()
				xed = float(linelvl_file.replace("\n",""))
				linelvl_file = level_file.readline()
				yed = float(linelvl_file.replace("\n",""))
				e = Entity(
				model = 'cube',
				y = yed, x=xed,
				scale_x = 3,
				scale_y = 1.3,
				collider = 'cube',
				texture = 'assets/RegularPlatform01.png')
				plates.append(e)
			elif linelvl_file.startswith("Platform"):
				linelvl_file = level_file.readline()
				xed = float(linelvl_file.replace("\n",""))
				linelvl_file = level_file.readline()
				yed = float(linelvl_file.replace("\n",""))
				e = Entity(
					model = 'cube',
					y = yed, x=xed,
					scale_x = 3,
					scale_y = 1.3,
					collider = 'cube',
					texture = 'assets/RegularPlatform01.png')
				ehit1 = duplicate(
					e, y = yed,
					x = xed, scale_y = 0.01,scale_x = 2.5, color = color.red, collider = 'mesh')
				plates.extend((e, ehit1))
			elif linelvl_file.startswith("Block001"):
				linelvl_file = level_file.readline()
				xed = float(linelvl_file.replace("\n",""))
				linelvl_file = level_file.readline()
				yed = float(linelvl_file.replace("\n",""))
				eb = Entity(
				model = 'cube',
				y = yed, x=xed,
				scale_x = 3,
				scale_y = 3,
				collider = 'cube',
				texture = 'assets/block_1.png')
				ebhit1 = duplicate(
				eb, y = yed,
				x = xed, scale = 0.1, color = color.red, collider = 'mesh')
				plates.extend((eb, ebhit1))
			
			elif linelvl_file.startswith("Coin"):
				linelvl_file = level_file.readline()
				xed = float(linelvl_file.replace("\n",""))
				linelvl_file = level_file.readline()
				yed = float(linelvl_file.replace("\n",""))
				coin = Entity(
				model = 'cube',
				y = yed, x=xed,
				scale_x = 4,
				scale_y = 4,
				texture = 'assets/coin.png')
				plates.append(coin)
		elif linelvl_file.startswith('CreateTrigger:'):
			linelvl_file = level_file.readline()
			if linelvl_file.startswith("End"):
				linelvl_file = level_file.readline()
				xend = float(linelvl_file.replace("\n",""))
				linelvl_file = level_file.readline()
				yend = float("-" + linelvl_file.replace("\n",""))
				endtrg = Entity(
					model = 'cube',
					y = yend, x=xend,
					scale_x = 0.01,
					scale_y = 0.01,
					collider = 'cube')
				plates.append(endtrg)
	start_lvl = 1
	pause = 0
	player.y = 0
	ground = Entity(
	model = 'cube',
	color= color.blue	,
	y=-1.5, origin_y=.5,
	scale = (34000, 25, 1),
	collider='box',
	texture = 'assets/ground1.png'
	)
	ground.texture_scale = (2000,1)
	plates.append(ground)
	background = Entity(
	model = 'quad',
	texture = 'assets/bg.png',
	scale = 7500, z = 25, y = -3,
	color = color.red
	)
	background.texture_scale = (100,100)
	plates.append(background)
lvlload()


l_win = 0
player.y= 0
def update():
	global start_lvl
	if start_lvl == 1:
		global pmode
		global gds
		if pmode == 1:
			camera.y = player.y+6
			camera.x = 3
		if pmode == 0:
			camera.y = player.y+5
		global l_win
		global level_file
		global pause
		global xend
		global diam
		global plates
		global yend
		if player.y < 0:
			player.y = 0
	
		if pmode == 1:
			if held_keys['a']:
				for ob in diam:
					if pause == 0:
						ob.x += player_speeded * time.dt
				for ob in plates:
					if pause == 0:
						ob.x += player_speeded * time.dt
			elif held_keys['d']:
				for ob in diam:
					if pause == 0:
						ob.x -= player_speeded * time.dt
				for ob in plates:
					if pause == 0:
						ob.x -= player_speeded * time.dt
		else:
			for ob in diam:
				if pause == 0:
					ob.x -= player_speeded * time.dt

			for ob in plates:
				if pause == 0:
					ob.x -= player_speeded * time.dt
		if player.x > endtrg.x:
			if l_win == 0:
				print("Win!")
				l_win = 1
		if not player.intersects().hit:
			player.y -= 20*time.dt
		player.y = max(-5, player.y)
		t = player.intersects()
		if t.hit:
			for en in t.entities:
				if en.color == color.red:
					if pause == 0:
						gds.stop(destroy=True)
						Audio("assets/death.mp3")
						pause = 1
						level_file.close()
						
						for ob in diam:
							ob.enabled = False
						for ob in plates:
							ob.enabled = False

						player.y = 0
						start_lvl = 0
						lvlload()




#b = Button(text='hello world!', color=color.azure, icon='sword', scale=.25, text_origin=(-.5,0))
#b.on_click = application.quit # assign a function to the button.
#b.tooltip = Tooltip('exit')
def input(key):
	if player.rotation_z != 180 or 0:
		player.rotation_z = 0
	global pmode
	global pause
	if key == 'escape':
		if pause == 1:
			pause = 0
		else:
			pause = 1
	if pmode == 0:
		if pause == 0:
			if key == 'space':
				if player.intersects().hit:
					player.animate_y(
						player.y + 6,
						duration = 0.3,
						curve = curve.out_quart
						)
					player.animate_rotation_z(player.rotation_z + 180, duration = 0.4, curve = curve.out_quart)
	elif pmode == 1:
		if pause == 0:
			if key == 'space':
				if player.intersects().hit:
					player.animate_y(
						player.y + 6,
						duration = 0.3,
						curve = curve.out_quart
						)
					player.animate_rotation_z(player.rotation_z + 180, duration = 0.4, curve = curve.out_quart)
	





app.run()
