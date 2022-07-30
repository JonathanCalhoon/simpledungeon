from code import screen, terminal


screen = screen.Screen()


def die(player, reason):
    """Die"""
    death_screen = f"""
      @@@@@@@@@@@@@@@@@@
     @@@@@@@@@@@@@@@@@@@@@@@
   @@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@
 @@@@@@@@@@@@@@@/      \\@@@/   @
@@@@@@@@@@@@@@@@\\      @@  @___@
@@@@@@@@@@@@@ @@@@@@@@@@  | \@@@@@
@@@@@@@@@@@@@ @@@@@@@@@\\__@_/@@@@@
 @@@@@@@@@@@@@@@/,/,/./'/_|.\\'\\,\\
   @@@@@@@@@@@@@|  | | | | | | | |
                 \\_|_|_|_|_|_|_|_|

    {reason}
"""
    screen.display_card(player, death_screen.split("\n"))

    input()

    terminal.clear()

    with open("gameover.txt", 'r') as file:
        string = screen.build_out_string(file.read())
    print(string)

    exit()