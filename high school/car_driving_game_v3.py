# Car Driving Game
#   Play as a car, dodge oncoming vehicles. An accurate and exciting driving simulator for all ages. Created for the
#   AS91637 NCEA Level 3 internal assessment

# Created by Samuel Kolston
# Created on: 10/03/18
# Last edited: 16/04/18

# For incremental development updates see version control and related notes
# LDA = local data attribute

# Final bug fixes and to do list
#   -print out VCS log B


# Import tkinter and random builtin functions, using the "tk" mode for window creation
from tkinter import *
import tkinter as tk
import random


# MenuScreen Class: creates the main menu for the game, with start, instructions and exit buttons.
class MenuScreen:

    # Constants
    BT_WIDTH = 28  # Consistent button size (px)
    MENU_SEP_HEIGHT = 5  # Vertical button separation height (px)
    TITLE_FONT_SIZE = 30  # Consistent title size (px)
    OPTIONS_SCALE_WIDTH = 300  # Width of the scales for choosing the sizes of the cars (px)
    OPTIONS_CANVAS_WIDTH = 220  # Width of the canvas for displaying the sizes of the cars (px)
    OPTIONS_REFRESH_RATE = 100  # The rate, in ms, that the example cars refresh their size to match the scales

    def __init__(self, root):

        # Create LDA for main window
        self.root = root

        # Create menu buttons
        self.menu_frame = tk.Frame(self.root, width=Gui.WINDOW_WIDTH, height=Gui.WINDOW_HEIGHT,
                                   bg=Gui.WINDOW_COLOUR)
        self.menu_title = tk.Label(self.menu_frame, text="Car Driving Game", font=MenuScreen.TITLE_FONT_SIZE,
                                   bg=Gui.WINDOW_COLOUR)
        self.start_bt = tk.Button(self.menu_frame, width=MenuScreen.BT_WIDTH, text="START",
                                  command=self.start_game)
        self.instructions_bt = tk.Button(self.menu_frame, width=MenuScreen.BT_WIDTH, text="INSTRUCTIONS",
                                         command=self.instructions_menu)
        self.options_bt = tk.Button(self.menu_frame, width=MenuScreen.BT_WIDTH, text="OPTIONS",
                                    command=self.options_menu)
        # The exit button has no local function, and goes straight to the builtin exit function
        self.exit_bt = tk.Button(self.menu_frame, width=MenuScreen.BT_WIDTH, text="EXIT", command=exit)

        # Pack menu frame, grid buttons and menu title within the frame
        # I have used pack for the menu frame as it is simple and I want the frame to cover the whole window anyway
        self.menu_frame.pack()
        # I have used grid for the buttons as they are easy to organize and I want them on the same vertical plane
        self.menu_title.grid(row=0, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)  # Constant use for consistency
        self.start_bt.grid(row=1, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)
        self.instructions_bt.grid(row=2, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)
        self.options_bt.grid(row=3, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)
        self.exit_bt.grid(row=4, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)

        # Create instructions frame, label, and return button for instructions sub menu
        self.instructions_frame = tk.Frame(self.root, width=Gui.WINDOW_WIDTH, height=Gui.WINDOW_HEIGHT,
                                           bg=Gui.WINDOW_COLOUR)
        self.instructions_title = tk.Label(self.instructions_frame, text="Instructions",
                                           font=MenuScreen.TITLE_FONT_SIZE, bg=Gui.WINDOW_COLOUR)
        self.instructions_label = tk.Label(self.instructions_frame,
                                           text="Welcome to the Car Driving Game!\nAn exciting and realistic car "
                                                "driving simulator.\nDodge the oncoming cars with the Left and Right "
                                                "arrow keys.\nTry and survive for as long as you can!\n\n Created by: "
                                                "Samuel Kolston - 111546\nCreated on: 10/03/18\nLast edited: 16/04/18",
                                           bg=Gui.WINDOW_COLOUR)
        self.instructions_menu_bt = tk.Button(self.instructions_frame, width=MenuScreen.BT_WIDTH,
                                              text="MAIN MENU", command=self.hide_submenu)

        # Create options frame, label, slider and return button for options sub menu
        self.options_frame = tk.Frame(self.root, width=Gui.WINDOW_WIDTH, height=Gui.WINDOW_HEIGHT,
                                      bg=Gui.WINDOW_COLOUR)
        self.options_title = tk.Label(self.options_frame, text="Options", font=MenuScreen.TITLE_FONT_SIZE,
                                      bg=Gui.WINDOW_COLOUR)
        self.options_label = tk.Label(self.options_frame, text="Drag the slider to set the size of the games cars.\n"
                                                               "Be careful! The size of the cars will change gameplay "
                                                               "dramatically:\nThe larger the cars, the harder they "
                                                               "are to dodge or move.\n\nThe top slider controls the "
                                                               "size of your car\nThe bottom slider controls the size "
                                                               "of the enemy car\nThe leftmost car is your car, which "
                                                               "you will control.\nThe rightmost car is an example of "
                                                               "an enemy car\n",
                                      bg=Gui.WINDOW_COLOUR)
        self.options_menu_bt = tk.Button(self.options_frame, width=MenuScreen.BT_WIDTH, text="MAIN MENU",
                                         command=self.hide_submenu)

        # Scales for choosing size of cars, using constants for size from respective car classes
        self.player_size_scale = tk.Scale(self.options_frame, from_=PlayerCar.MIN_PLAYER_SIZE,
                                          to_=PlayerCar.MAX_PLAYER_SIZE,
                                          orient=HORIZONTAL, bg=Gui.WINDOW_COLOUR,
                                          length=MenuScreen.OPTIONS_SCALE_WIDTH)
        self.enemy_size_scale = tk.Scale(self.options_frame, from_=EnemyCar.MIN_ENEMY_SIZE, to_=EnemyCar.MAX_ENEMY_SIZE,
                                         orient=HORIZONTAL, bg=Gui.WINDOW_COLOUR, length=MenuScreen.OPTIONS_SCALE_WIDTH)
        self.player_size_scale.set(PlayerCar.DEFAULT_PLAYER_SIZE)
        self.enemy_size_scale.set(EnemyCar.DEFAULT_ENEMY_SIZE)

        # Determine the height of the test canvas by finding the highest maximum size for each car, then choosing that
        #   value plus 1 so that the whole of the cars can be seen
        self.options_canvas_size = 0
        if PlayerCar.MAX_PLAYER_SIZE >= EnemyCar.MAX_ENEMY_SIZE:
            self.options_canvas_size = PlayerCar.MAX_PLAYER_SIZE + 1
        else:
            self.options_canvas_size = EnemyCar.MAX_ENEMY_SIZE + 1
        # Create canvas for the example cars (also create the cars themselves)
        #   I have not used a constant for the border thickness as the menu is not aesthetically pleasing, and more
        #   difficult to understand, to the user
        self.options_canvas = Canvas(self.options_frame, width=MenuScreen.OPTIONS_CANVAS_WIDTH,
                                     height=self.options_canvas_size, bg=Gui.WINDOW_COLOUR, highlightthickness=0)
        self.example_player = self.options_canvas.create_rectangle(0, self.player_size_scale.get(),
                                                                   self.player_size_scale.get(), 0,
                                                                   fill=PlayerCar.PLAYER_COLOUR,
                                                                   outline=PlayerCar.PLAYER_OUTLINE_COLOUR)
        self.example_enemy = self.options_canvas.create_rectangle(int(MenuScreen.OPTIONS_CANVAS_WIDTH / 2),
                                                                  self.player_size_scale.get(),
                                                                  int(MenuScreen.OPTIONS_CANVAS_WIDTH / 2) +
                                                                  self.player_size_scale.get(), 0,
                                                                  fill=EnemyCar.ENEMY_COLOURS[0])

        # Boolean to see whether the game has started or not, this will be used to decrease redundant processes
        self.game_started = False

    # Function for changing some basic options for gameplay i.e. player car size
    def options_menu(self):
        self.menu_frame.pack_forget()  # Remove menu frame from screen, remembering its position

        self.options_frame.pack()  # Place options frame on screen
        # Place all other widgets in the options frame using grid, for same reasoning as main menu, in order of row
        self.options_title.grid(row=1, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)
        self.options_label.grid(row=2, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)
        self.player_size_scale.grid(row=3, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)
        self.options_canvas.grid(row=4, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)
        self.enemy_size_scale.grid(row=5, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)
        self.options_menu_bt.grid(row=6, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)

        self.options_slider_movement()

    def options_slider_movement(self):
        if not self.game_started:
            self.options_canvas.coords(self.example_player, 0, self.player_size_scale.get(),
                                       self.player_size_scale.get(), 0)
            self.options_canvas.coords(self.example_enemy, int(MenuScreen.OPTIONS_CANVAS_WIDTH / 2), 0,
                                       self.enemy_size_scale.get() + int(MenuScreen.OPTIONS_CANVAS_WIDTH / 2),
                                       self.enemy_size_scale.get())
            self.root.after(MenuScreen.OPTIONS_REFRESH_RATE, self.options_slider_movement)

    # Function for displaying instructions sub menu
    def instructions_menu(self):
        # Pack forget has been used as it remembers the location of widgets, only temporarily removing them
        self.menu_frame.pack_forget()

        # Packing the instructions frame, and gridding buttons just as with menu frame and buttons
        self.instructions_frame.pack()
        self.instructions_title.grid(row=1, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)
        self.instructions_label.grid(row=2, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)
        self.instructions_menu_bt.grid(row=3, column=0, pady=MenuScreen.MENU_SEP_HEIGHT)

    # Function for hiding instructions and/or highscore sub menu
    # I have named in hide_submenu rather than hide_instructions or something, as well as making it a separate function,
    #   because if I wanted to add another sub menu later it would be easy to add another pack forget here
    def hide_submenu(self):
        self.instructions_frame.pack_forget()
        self.options_frame.pack_forget()
        self.menu_frame.pack()

    # Function for closing menu and starting the main game (GameScreen)
    def start_game(self):
        # Remove menu screen from window. this will still be stored in memory so that it can be recalled easily later.
        #   while this memory takes up some resources even when the user has no need for it, the amount is negligible
        #   and will make it easy for the user to restart or close their game once they have finished playing
        self.menu_frame.pack_forget()

        # Set the game to started, so that the scale stops refreshing
        self.game_started = True

        # Create game screen object
        # I have passed through self, or this instance of the menu, so that I can re pack the menuscreen at any time
        GameScreen(self.root, self, self.player_size_scale.get(), self.enemy_size_scale.get())


# GameScreen Class: creates the canvas that holds everything in the actual "game" part of the program. this class also
#   handles keypresses and the collision of the player car
class GameScreen:

    # Constants
    GAME_SPEED = 16  # The "refresh rate" of the game, in ms (the higher, the slower). 16 is recommended
    GAME_BACKGROUND = "grey"  # The colour of the "road"
    DEBUGGING = False  # This boolean enables printing of window/widget information for debugging
    SCORE_LOCATION = [10, 10]  # The x and y co ordinates for the score counter
    BORDER_WIDTH = 10  # Width of the border that will surround the game canvas
    CAR_GEN_SPEED = 550  # The interval at which cars are created

    def __init__(self, root, menuscreen, player_size, enemy_size):

        # Create LDA for main window, main menu, player and enemy car size
        self.root = root
        self.menuscreen = menuscreen
        self.player_size = player_size
        self.enemy_size = enemy_size

        # None type for repeating enemy cars, this will eventually be turned into a tkinter function to stop the
        #   creation of enemy cars, see: create_enemy_cars()
        self.repeat_create_cars = None

        # Create the number of cars to generate
        self.max_enemy_cars = int(Gui.WINDOW_HEIGHT / EnemyCar.DEFAULT_ENEMY_SIZE)

        # Create list for movement and integer for player score
        self.movement_list = [0]
        self.player_score = 0

        # Create game canvas and score counter
        self.game_canvas = Canvas(self.root, height=Gui.WINDOW_HEIGHT, width=Gui.WINDOW_WIDTH,
                                  bg=GameScreen.GAME_BACKGROUND, highlightthickness=GameScreen.BORDER_WIDTH)
        self.score_counter = tk.Label(self.game_canvas, text=self.player_score, bg=GameScreen.GAME_BACKGROUND,
                                      fg="white", font=("Comic Sans", 16))

        # Place the score counter on the canvas, pack the canvas, place focus on the canvas
        self.score_counter.place(x=GameScreen.SCORE_LOCATION[0], y=GameScreen.SCORE_LOCATION[1])
        self.game_canvas.pack()  # Have used pack as it fills up whole screen and should originate at 0, 0
        self.game_canvas.focus_set()

        # List to store enemy cars
        self.car_list = []

        # Create player car object
        self.player = PlayerCar(self.root, self.game_canvas, self.movement_list, self.player_size, self.menuscreen)

        # Bind keypress/release events to corresponding functions
        self.root.bind_all("<KeyPress>", self.on_keypress)
        self.root.bind_all("<KeyRelease>", self.on_keyrelease)

        # Call the functions for increasing score every second, handling collisions with cars and creating enemy cars
        self.calculate_score()
        self.collision_check()
        self.create_enemy_cars()

    # Function for creating enemy cars, appending them to a list
    def create_enemy_cars(self):
        if len(self.car_list) < self.max_enemy_cars:

            # A list has been used so that the cars can be addressed without naming them individually
            self.car_list.append(EnemyCar(self.root, self.game_canvas, self.enemy_size, self.menuscreen))

        else:
            # Cancelling the window.after functionality so that when the maximum number of enemy cars is created, the
            #   loop does not either, increasing efficiency
            self.root.after_cancel(self.repeat_create_cars)
            return  # This ensures that the function is not repeated

        self.repeat_create_cars = self.root.after(GameScreen.CAR_GEN_SPEED, self.create_enemy_cars)

    # Function for checking collisions i.e. enemy car with bottom of screen, player car with enemy car
    def collision_check(self):

        # If the game has not ended
        if self.menuscreen.game_started:

            for i in range(len(self.car_list)):

                # If the enemy car overlaps with the player car, end the game
                if self.car_list[i].enemy_car in self.game_canvas.find_overlapping(
                       *self.game_canvas.coords(self.player.player_car)):
                    self.return_to_menu()
                    # I have used break here as it quits the loop before it is called again, saving an index error.
                    break

            # Prints some game and canvas information for lag debugging
            if GameScreen.DEBUGGING:
                print(self.game_canvas.find_withtag("all"))  # Print all items on canvas
                print("len car list: {}".format(len(self.car_list)))  # Prints length of car list
                print("reference count: {}".format(sys.getrefcount(EnemyCar)))  # Prints refs to EnemyCar object

            # Restart this function every (x)ms
            self.root.after(GameScreen.GAME_SPEED, self.collision_check)

    # Function for changing (increasing) score of the player
    def calculate_score(self):

        # Every 10th of a second, increase the player score by 0.1. I have not used constants here as I always intend
        #   for the score to be calculated with seconds surviving, with tenths of seconds for added accuracy and
        #   differentiation across close, varying scores.
        if self.menuscreen.game_started:  # Only runs when the game is being played
            self.player_score += 0.1
            self.score_counter.config(text="{:.1f}".format(self.player_score))  # Displaying the change to the user
            self.root.after(100, self.calculate_score)  # No constant, for reasoning above

    # Function for handling keypress events, will move the car left and/or right and/or exit/restart the game
    #   (returning to main menu)
    def on_keypress(self, event):
        if self.menuscreen.game_started:  # Only checks for inputs when the game is being played
            if event.keysym == "Left":
                if -PlayerCar.PLAYER_SPEED not in self.movement_list:
                    self.movement_list.append(-PlayerCar.PLAYER_SPEED)
            elif event.keysym == "Right":
                if PlayerCar.PLAYER_SPEED not in self.movement_list:
                    self.movement_list.append(PlayerCar.PLAYER_SPEED)
            elif event.keysym == "Escape":
                self.return_to_menu()
        else:
            return  # Stops the continuation of this function

    # Function for handing keyrelease events, will stop moving the car once left or right key is released
    def on_keyrelease(self, event):
        if self.menuscreen.game_started:  # Only checks for inputs when the game is being played
            if event.keysym == "Left":
                self.movement_list.remove(-PlayerCar.PLAYER_SPEED)
            elif event.keysym == "Right":
                self.movement_list.remove(PlayerCar.PLAYER_SPEED)
        else:
            return  # Stops the continuation of this function

    # Function for returning the user to the main menu, either by choice or by losing the game
    def return_to_menu(self):
        # This will delete all objects on the canvas, 'unpack' the game canvas, and re-pack the main menu
        #   essentially. This will increase efficiency as opposed to creating a new menu screen as I am not
        #   re creating unnecessary objects
        self.menuscreen.game_started = False
        self.game_canvas.delete("all")
        self.game_canvas.pack_forget()
        self.car_list = []
        self.menuscreen.menu_frame.pack()


# PlayerCar Class: creates the main player car, which can be controlled through key presses in the Gui class. The move()
#   function is controlled by the Gui class, which moves the rectangle that is the player car
class PlayerCar:

    # Constants
    PLAYER_SPEED = 10  # Maximum horizontal speed of car (px per movement)
    # Default ize of car rectangle (px, width/height). the car will always be a square, so only one value is needed here
    #   I have chosen to make player car (and enemy car) to always be even squares as it ensures that lots of space is
    #   given on the screen for movement, makes more sense (more car-like, kind of), and is more aesthetically pleasing.
    #   while this constant is not referenced in this class itself, I still believe it makes more logical sense to be
    #   located here as it is exclusively part of the player car object. This value will be the default of the scale in
    #   the options menu
    DEFAULT_PLAYER_SIZE = 50  # Size of player car square (px, width/height)
    MIN_PLAYER_SIZE = 1  # Minimum size of player car square (px, width/height) THIS SHOULD NOT GO BELOW 1, WILL BREAK
    MAX_PLAYER_SIZE = 100  # Maximum size of player car square (px, width/height)
    PLAYER_COLOUR = "green"  # Fill colour for player car rectangle
    PLAYER_OUTLINE_COLOUR = "black"  # Outline colour for player car rectangle

    def __init__(self, root, canvas, movement_list, player_size, menuscreen):

        # Create LDA for main window, canvas, movement list, player size and menuscreen instance
        self.root = root
        self.game_canvas = canvas
        self.movement_list = movement_list
        self.player_size = player_size
        self.menuscreen = menuscreen

        # None type for player move function, this will soon be changed into a tkinter canvas function
        self.repeat_player_movement = None

        # Create movement variable and origin points for the player car rectangle
        # These calculations with constants mean that the car will always spawn in the centre of the screen, no matter
        #   it's size, increasing consistency for the user. the car will also spawn just slightly (5px) above the
        #   border, so that the entirety of the car can be viewed by the user, increasing usability
        self.x1 = (Gui.WINDOW_WIDTH / 2) - 0.5 * self.player_size
        self.y1 = (Gui.WINDOW_HEIGHT - self.player_size) - (GameScreen.BORDER_WIDTH + 5)
        self.x2 = self.x1 + self.player_size
        self.y2 = self.y1 + self.player_size

        # Create player car object
        self.player_car = self.game_canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline=
                                                            PlayerCar.PLAYER_OUTLINE_COLOUR,
                                                            fill=PlayerCar.PLAYER_COLOUR)

        # Begin movement of the car
        self.move()

    # Function for controlling car movement
    # I have placed this function here, as opposed to placing it inside of the GameScreen with the enemy car collision
    #   function, as I believe that this move function is isolated to the player car, whereas the enemy car collision
    #   involves the main menu, the enemy car and the player car
    def move(self):
        if self.menuscreen.game_started:
            # If the player collides with the left of the screen, move it to the right to avoid going off the screen
            if self.player_car in self.game_canvas.find_overlapping(-10, 0, GameScreen.BORDER_WIDTH, Gui.WINDOW_HEIGHT):
                self.game_canvas.move(self.player_car, PlayerCar.PLAYER_SPEED, 0)

            # If the player collides with the right of the screen, move it to the left to avoid going off the screen
            elif self.player_car in self.game_canvas.find_overlapping(Gui.WINDOW_WIDTH - GameScreen.BORDER_WIDTH, 0,
                                                                      Gui.WINDOW_WIDTH + 10, Gui.WINDOW_HEIGHT):
                self.game_canvas.move(self.player_car, -PlayerCar.PLAYER_SPEED, 0)

            # If the player makes no collision
            else:
                # If no collision, move the car using the sum of the movement list, which has been manipulated with
                #   keypresses under gamescreen
                self.game_canvas.move(self.player_car, sum(self.movement_list), 0)

            # Restart the move function after (x)ms
            self.root.after(GameScreen.GAME_SPEED, self.move)

        else:
            self.repeat_player_movement = self.root.after_cancel(self.move)
            return


# EnemyCar Class: creates the enemy cars, which move vertically down the screen automatically.
class EnemyCar:

    # Constants
    ENEMY_SPEED = 3  # Maximum vertical speed enemy of car (px per movement)
    DEFAULT_ENEMY_SIZE = 50  # Size of enemy car square (px, width/height)
    MIN_ENEMY_SIZE = 1  # Minimum size of enemy car square (px, width/height) THIS SHOULD NOT GO BELOW 1, WILL BREAK
    MAX_ENEMY_SIZE = 100  # Maximum size of enemy car square (px, width/height)

    # List of all possible car colours, each car randomly selects a colour during creation
    # CAR_COLOURS = ["#686e77", "#58595b", "#8b8d91", "#b1bacc", "#3e4551", "#737d8e", "#5d5d5e", "#aaaab5"]
    # CAR_COLOURS = ["red", "yellow", "orange", "blue", "purple"]
    ENEMY_COLOURS = ["black"]  # Enemy car rectangle fill colour

    # The car outline colour is a single colour to avoid confusion from the player, as it is too visually confusing when
    #   the outline is constantly changing. this also means that as the car fill colour changes, the player can still
    #   always tell that the rectangles with (x) colour are always going to be enemy cars
    ENEMY_OUTLINE_COLOUR = "black"  # Enemy car rectangle outline colour

    def __init__(self, root, canvas, enemy_size, menuscreen):

        # Create LDA for main window, game canvas, enemy size and menuscreen instance
        self.root = root
        self.game_canvas = canvas
        self.enemy_size = enemy_size
        self.menuscreen = menuscreen

        # None type for repeating the move function, this will soon be changed into a tkinter canvas function
        self.repeat_enemy_movement = None

        # Create local variable, using constants, for the end point for the enemy cars
        self.car_exit_points = [0, Gui.WINDOW_HEIGHT + self.enemy_size, Gui.WINDOW_WIDTH, Gui.WINDOW_HEIGHT +
                                self.enemy_size + GameScreen.BORDER_WIDTH]

        # Create x1, x2 and y2 origin points for the creation of the enemy car rectangle. the x2 and y2 origin points
        #   are equal to their 1 alternatives, so that only 1 integer is needed to set the origin point of the enemy
        #   cars, and their sizes are an always constant size (determined using constants and scale under menuscreen)
        self.x1 = random.randint(0, Gui.WINDOW_WIDTH - self.enemy_size)
        self.y1 = -self.enemy_size
        self.x2 = self.x1 + self.enemy_size
        self.y2 = self.y1 + self.enemy_size

        # Get a random colour from the list for the car
        self.car_colour = EnemyCar.ENEMY_COLOURS[random.randint(0, len(EnemyCar.ENEMY_COLOURS) - 1)]

        # Create enemy car object
        self.enemy_car = self.game_canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                                           outline=EnemyCar.ENEMY_OUTLINE_COLOUR, fill=self.car_colour)

        # Begin movement of the car
        self.move()

    # Function for movement of the car
    def move(self):
        if self.menuscreen.game_started:
            # If the enemy car is just outside of the viewable screen of the player (handled by constants, meaning that
            #   these values will change automatically if the screen resolution is changed)

            if self.enemy_car in self.game_canvas.find_overlapping(*self.car_exit_points):
                # Save the current x position, and move the car to a random location between -current x position, and
                #   the width of the gui minus the same integer
                old_x = self.game_canvas.coords(self.enemy_car)[0]
                self.game_canvas.move(self.enemy_car, random.randint(-old_x, (Gui.WINDOW_WIDTH - old_x) -
                                      self.enemy_size), (-Gui.WINDOW_HEIGHT - self.enemy_size))
            else:
                self.game_canvas.move(self.enemy_car, 0, EnemyCar.ENEMY_SPEED)

            # Restart loop
            self.repeat_enemy_movement = self.root.after(GameScreen.GAME_SPEED, self.move)

        else:
            self.repeat_enemy_movement = self.root.after_cancel(self.move)
            return


# Gui Class: this is essentially the main class. creates the root window which makes up the graphical side of the
#   program.
class Gui:

    # Constants
    # Window sizing. the changing of these constants will also change many other values throughout the program so that
    #   the gameplay is the same no matter the resolution of the player
    # IT IS ADVISED THAT THE WINDOW IS NO SMALLER THAN 500 BY 500 PIXELS, AS THE GAME WILL BE UNPLAYABLE OTHERWISE
    WINDOW_WIDTH = 800  # Width of the window (in px)
    WINDOW_HEIGHT = 600  # Height of the window (in px)

    WINDOW_X_ORIGIN = 0  # Origin point of the window (x axis)
    WINDOW_Y_ORIGIN = 0  # Origin point of the window (y axis)

    WINDOW_COLOUR = "#ff7802"  # Background colour of the window. this will also apply to the menu widgets

    def __init__(self):
        # Create root window
        self.root = Tk()

        # Configure root window, sizing using constants
        self.root.geometry("{}x{}+{}+{}".format(Gui.WINDOW_WIDTH, Gui.WINDOW_HEIGHT, Gui.WINDOW_X_ORIGIN,
                                                Gui.WINDOW_Y_ORIGIN))
        self.root.title("Car Driving Game")
        self.root.config(bg=Gui.WINDOW_COLOUR)
        # This means that the user cannot click on the side of the windows and change the size, as this would ruin the
        #   gameplay through constantly changing resolutions
        self.root.resizable(False, False)

        # Create menu object
        MenuScreen(self.root)

        # Loop main window
        self.root.mainloop()


# Create Gui object
Gui()
