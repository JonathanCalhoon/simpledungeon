from code import util
from save_game import login_manager
import cursor

cursor.hide()

util.clear_log()


SAVE = True

# Fork the repl and change the variable above
# to true if you want your game saved. 
# this will display the alternate menu
# that gives you the option to save your game.


###############
#  INIT GAME  #
###############


login = login_manager.LoginManager() #inits login

GAME = login.login() # Returns a game object

GAME.play() # runs the game object


