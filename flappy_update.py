
# MAY-DAY
# A GAME MADE BY AMOGH, ANAND AND AMMAR

import pygame, sys, random 

# def draw_floor():
# 	screen.blit(floor_surface,(floor_x_pos,900))
# 	screen.blit(floor_surface,(floor_x_pos + 576,900))

def create_building():
	random_building_pos = random.choice(building_height)
	bottom_building = building_surface.get_rect(midtop = (700,random_building_pos))
	top_building = building_surface.get_rect(midbottom = (700,random_building_pos - 300))
	return bottom_building,top_building

def move_buildings(buildings):
	for building in buildings:
		building.centerx -= 5
	visible_buildings = [building for building in buildings if building.right > -50]
	return visible_buildings

def draw_buildings(buildings):
	for building in buildings:
		if building.bottom >= 1024:
			screen.blit(building_surface,building)
		else:
			flip_building = pygame.transform.flip(building_surface,False,True)
			screen.blit(flip_building,building)

def check_collision(buildings):
	global can_score
	for building in buildings:
		if plane_rect.colliderect(building):
			death_sound.play()
			can_score = True
			return False

	if plane_rect.top <= -100 or plane_rect.bottom >= 900:
		can_score = True
		return False

	return True

def rotate_plane(plane):
	new_plane = pygame.transform.rotozoom(plane,-plane_movement * 3,1)
	return new_plane

def plane_animation():
	new_plane = plane_frames[plane_index]
	new_plane_rect = new_plane.get_rect(center = (100,plane_rect.centery))
	return new_plane,new_plane_rect

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

def building_score_check():
	global score, can_score 
	
	if building_list:
		for building in building_list:
			if 95 < building.centerx < 105 and can_score:
				score += 1
				score_sound.play()
				can_score = False
			if building.centerx < 0:
				can_score = True

#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 2, buffer = 1024)
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

# Game Variables
gravity = 0.4
plane_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# floor_surface = pygame.image.load('assets/base.png').convert()
# floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

plane_fire1 = pygame.transform.scale2x(pygame.image.load('assets/plane-fire1.png').convert_alpha())
plane_fire2 = pygame.transform.scale2x(pygame.image.load('assets/plane-fire2.png').convert_alpha())
plane_fire3 = pygame.transform.scale2x(pygame.image.load('assets/plane-fire3.png').convert_alpha())
plane_frames = [plane_fire1,plane_fire2,plane_fire3]
plane_index = 0
plane_surface = plane_frames[plane_index]
plane_rect = plane_surface.get_rect(center = (100,512))

planeFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(planeFLAP,200)

# plane_surface = pygame.image.load('assets/blueplane-fire2.png').convert_alpha()
# plane_surface = pygame.transform.scale2x(plane_surface)
# plane_rect = plane_surface.get_rect(center = (100,512))

building_surface = pygame.image.load('assets/building.png')
building_surface = pygame.transform.scale2x(building_surface)
building_list = []
SPAWNbuilding = pygame.USEREVENT
pygame.time.set_timer(SPAWNbuilding,1200)
building_height = [400,600,800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT,100)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				plane_movement = 0
				plane_movement -= 12
				flap_sound.play()
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				building_list.clear()
				plane_rect.center = (100,512)
				plane_movement = 0
				score = 0

		if event.type == SPAWNbuilding:
			building_list.extend(create_building())

		if event.type == planeFLAP:
			if plane_index < 2:
				plane_index += 1
			else:
				plane_index = 0

			plane_surface,plane_rect = plane_animation()

	screen.blit(bg_surface,(0,0))

	if game_active:
		# plane
		plane_movement += gravity
		rotated_plane = rotate_plane(plane_surface)
		plane_rect.centery += plane_movement
		screen.blit(rotated_plane,plane_rect)
		game_active = check_collision(building_list)

		# buildings
		building_list = move_buildings(building_list)
		draw_buildings(building_list)
		
		# Score
		building_score_check()
		score_display('main_game')
	else:
		screen.blit(game_over_surface,game_over_rect)
		high_score = update_score(score,high_score)
		score_display('game_over')


	# Floor
	floor_x_pos -= 1
	# draw_floor()
	if floor_x_pos <= -576:
		floor_x_pos = 0
	

	pygame.display.update()
	clock.tick(120)
