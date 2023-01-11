# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Thief, platformer video game                    #
#                              Developer: Carbon               				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.engine import *

# Game: #

game = Game()

# Resolution: #

resolution = Resolution(game)

# Resoltuion Selection: #

while(resolution.resolution_status):

    resolution.update_background()

    if(resolution.resolution_a.render()):
        resolution.set_resolution(1280, 720)
        break

    if(resolution.resolution_b.render()):
        resolution.set_resolution(1920, 1080)
        break

    resolution.update_window()

# Sounds: #

sounds = Sounds(game)

# Game Window: #

game.start_window(sounds)

# Game Icon: #

game.set_game_icon('assets/Player/Move/0.png')

# Assets Manager: #

assets_manager = AssetsManager(game)

# User Interface: #

ui = UserInterface(game, assets_manager)

# World: #

world = World(game, assets_manager)

# Menu: #

menu = Menu(game, world, assets_manager)

# Editor: #

editor = Editor(game, world, assets_manager, menu)

# Particles: #

particles = Particles(game)

# Loading Tiles: #

world.load_tiles()
editor.load_tiles()

# Fade In:

start_fade = Fade(game, 1, ((0, 0, 0)))

# Game Loop: #

while(game.engine_running):
	game.set_background((63, 56, 81))
	if(game.menu_on):
		menu.handle_menu()
		start_fade.reset()
	else:
		if(game.editor_status):
			editor.generate_editor_world()
			editor.draw_world()
			editor.draw_grid()
			editor.draw_user_interface()
			editor.draw_information()
			editor.handle_buttons()
			if(start_fade.fade()):
				editor.handle_editor()
		else:
			menu.check_for_arrest()
			game.draw_game_sprites(world, ui)
			particles.draw_particles()
			game.update_game_sprites(world, particles)
			if(start_fade.fade()):
				game.start_game()

	game.update_display(60)