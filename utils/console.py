# define colors
W = '\033[0m'  # white
B = '\033[1;30m'  # black
BLUE = '\033[1;34m' 

def print_headline(message):
   print(B + "---------------------------------------------------------------------- \n")
   print("******** " + message + " ******** \n")
   print("---------------------------------------------------------------------- \n")
   print(W)


def h4(message):
   print(BLUE + "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓" + W)
   print(BLUE + "│" + W + message + BLUE + "│" + W)
   print(BLUE + "└─────────────────────────────────────────────────────────────────┘" + W)


### Console colors
W  = '\033[0m'  # white 
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan