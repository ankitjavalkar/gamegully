TraderSim
==========

TraderSim is a simple script based CLI game along the lines of Trader Wars and Space Trader.

TraderSim is a single player, turn based CLI game in which the player assumes the role of a trader moving from city to city buying and selling goods and merchandise.

The objective of the game is to carry out arbitrage, pay off the debt and make most amount of cash at the end of the game.

Requirements:
--------------

You will need Python 3 installed to play.

To start the game, go to the directory containing the script and run the command;

	python3 tradersim.py

How To Play:
-------------

Once you start the game, you will be asked which City you wish to visit. Select the city to visit by typing in the number mentioned beside the City.

You can then run commands to carry out actions, like;

	buy <item-name> <item-quantity> => will buy the item name and the desired quantity (Shortcut: b)
	sell <item-name> <item-quantity> => will sell the item name and the desired quantity (Shortcut: s)
	repay <repayment-amount> => will repay the specified amount against the loan (Shortcut: r)
	end => will end the current turn (Shortcut: e)
