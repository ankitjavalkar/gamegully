from random import randint

ITEMS = [
    {'id': 'arms', 'label': 'Arms', 'upper_range': 30000, 'lower_range': 18000},
    {'id': 'diamonds', 'label': 'Opium', 'upper_range': 20000, 'lower_range': 8000},
    {'id': 'gold', 'label': 'Gold', 'upper_range': 12000, 'lower_range': 4000},
    {'id': 'iron', 'label': 'Iron', 'upper_range': 8000, 'lower_range': 2000},
    {'id': 'coal', 'label': 'Stone', 'upper_range': 4000, 'lower_range': 500},
    {'id': 'wood', 'label': 'Wood', 'upper_range': 800, 'lower_range': 100},  
    {'id': 'food', 'label': 'Food', 'upper_range': 80, 'lower_range': 15},
]

LOCATIONS = [
    'Mumbai',
    'Delhi',
    'Amritsar',
    'Hyderabad',
    'Jholpur',
    'Wazzeypur'
]

PLAYER_CASH_AMOUNT = 2000

PLAYER_LOAN_AMOUNT = 5000

PLAYER_LOAN_RATE = 10

GAME_MAX_TURNS = 2


class Item():
    def __init__(self, id, label, upper_range, lower_range):
        if upper_range < lower_range:
            raise Exception('Item price upper range cannot be lesser than lower range')
        self.id = id
        self.label = label
        self.upper_range = upper_range
        self.lower_range = lower_range
        self.cost = 0

    def _get_random_cost(self, lower_range, upper_range):
        return randint(lower_range, upper_range)

    def _set_random_cost(self):
        self.cost = randint(self.lower_range, self.upper_range)

    def set_cost(self, new_cost=None):
        if new_cost is None:
            self._set_random_cost()
        else:
            self.cost = new_cost
        return self


class Inventory():
    def __init__(self, item_list, *args, **kwargs):
        self.contents = {
            item.id: {
                'item': item,
                'quantity': 0
            } for item in item_list
        }

    # TODO round off values to 2 dec point
    def _average_cost(self, item_cost, item_quantity, market_cost, delta_quantity):
        current_value = item_cost * item_quantity
        delta_value = market_cost * delta_quantity
        avg = (current_value + delta_value) / (item_quantity + delta_quantity)
        return avg

    def add_quantity(self, item_id, market_cost, delta_quantity):
        item_quant = self.contents.get(item_id)
        if item_quant:
            item = item_quant.get('item')
            item_quantity = item_quant.get('quantity')
            if item:
                item_cost = item.cost
                new_cost = self._average_cost(
                    item_cost, item_quantity, market_cost, delta_quantity
                )
                item.set_cost(new_cost=new_cost)
                item_quant.update({
                    'quantity': item_quantity + delta_quantity
                })
            else:
                raise Exception('Item not found in Inventory')
        else:
            raise Exception('Item Quantity mapping not found in Inventory')

    def remove_quantity(self, item_id, delta_quantity):
        item_quant = self.contents.get(item_id)
        if item_quant:
            item = item_quant.get('item')
            item_quantity = item_quant.get('quantity')
            if item_quantity < delta_quantity:
                raise Exception('Quantity sold cannot be higher than current quantity')
            item_quant['quantity'] = item_quantity - delta_quantity
            if item:
                if item_quant['quantity'] == 0:
                    item.set_cost(new_cost=0)
            else:
               raise Exception('Item not found in Inventory')     
        else:
            raise Exception('Item Quantity mapping not found in Inventory')



class Location():
    def __init__(self, name, items, *args, **kwargs):
        self.name = name
        self.price_list = self._create_price_list(items)

    def _create_price_list(self, items):
        for item in items:
            item.set_cost()
        return items

    def update_price_list(self):
        if not self.price_list:
            raise Exception('Price List cannot be empty')
        self.price_list = self._create_price_list(self.price_list)

    def update_cost(self, item_id):
        for item in self.price_list:
            if item.id == item_id:
                item.set_random_cost()

    def get_cost(self, item_id):
        for item in self.price_list:
            if item_id == item.id:
                return item.cost
        raise Exception(
            'Item ID: {0} Not found in Location'
            ' - {1} Price List'.format(item_id, self.name)
        )


class Player():
    # Add cash
    # Add loan
    # Add func to create and initialise inventory - optional
    def __init__(self, cash, loan, rate, item_list):
        self.cash = cash
        self.loan = loan
        self.loan_rate = rate
        self.inventory = self._init_inventory(item_list)

    # TODO round off values to 2 dec point
    def _calculate_interest(self):
        return (self.loan * self.loan_rate / 100)

    def _init_inventory(self, item_list):
        return Inventory(item_list)

    def sell(self, item_id, market_cost, delta_quantity):
        self.inventory.remove_quantity(item_id, delta_quantity)
        self.cash += market_cost * delta_quantity

    def buy(self, item_id, market_cost, delta_quantity):
        if self.cash > market_cost * delta_quantity:
            self.inventory.add_quantity(item_id, market_cost, delta_quantity)
            self.cash -= market_cost * delta_quantity
        else:
            raise Exception('Purchase Value should not be higher than Cash Amount')

    def update_loan(self):
        if self.loan > 0:
            interest = self._calculate_interest()
            self.loan += interest
        return self.loan

    def repay_loan(self, amount):
        repay_amount = amount if amount < self.loan else self.loan
        self.loan = self.loan - repay_amount
        self.cash = self.cash - repay_amount


class Game():
    # initialize game resources
    # initialize list of items > add to inventory
    # initialize price lists
    # initialize locations > add price lists
    # render game board
    # add random events - robbery, police
    def __init__(self, items, locations, cash, loan, rate, max_turns):
        self.item_list = self._create_item_list(items)
        self.locations = self._create_location_list(locations)
        self.player = self._create_player(cash, loan, rate, items)
        self.max_turns = max_turns
        self.curr_location = None

    def _create_item_list(self, items):
        return [Item(**item) for item in items]

    def _create_location_list(self, locations):
        return [Location(name, self.item_list) for name in locations]

    def _create_player(self, cash, loan, rate, items):
        player_inventory = self._create_item_list(items)
        return Player(cash, loan, rate, player_inventory)

    def get_turns_remaining(self, turn_number):
        return self.max_turns - turn_number

    def buy(self, item_id, delta_quantity):
        market_cost = self.curr_location.get_cost(item_id)
        self.player.buy(item_id, market_cost, delta_quantity)

    def sell(self, item_id, delta_quantity):
        market_cost = self.curr_location.get_cost(item_id)
        self.player.sell(item_id, market_cost, delta_quantity)

    def repay(self, amount):
        self.player.repay_loan(amount) 

    def goto(self):
        # Set current location
        next_location = self._change_location()
        if next_location and next_location != self.curr_location:
            next_location.update_price_list()
            self.curr_location = next_location
        return next_location

    # def start_turn(self):
    #     # render the state
    #     pass

    # def end_turn(self):
    #     # prompt for goto location
    #     # update turn number
    #     # update pricelist for next location
    #     pass

    def _change_location(self):
        next_location = None
        error_msg = (
            "Invalid Input: {0}."
            " Please select a location by providing it's"
            " index number or by name"
        )
        # Render locations list
        for ix, location in enumerate(self.locations):
            print('{} - {}'.format(ix, location.name))
        # Prompt for input
        loc_input = input("Enter the location to travel to: ")
        # Validate
        if loc_input.isdigit():
            try:
                next_location = self.locations[int(loc_input)]
            except IndexError:
                print(error_msg.format(loc_input))
        elif loc_input.isalpha():
            for location in self.locations:
                if loc_input in location.name:
                    next_location = location
        else:
            print(error_msg.format(loc_input))
        return next_location

    def render_turn(self):
        # Render player status
        status = ('Cash: {}'
            '\tLoan: {}'
        ).format(self.player.cash, self.player.loan)

        # Render inventory content
        inventory_content = [
            '{}\n{}\t{}\t{}\n{}'.format('*'*30, 'Item', 'Qty', 'Price', '*'*30)
        ]
        for item_quant_map in self.player.inventory.contents.values():
            item = item_quant_map.get('item')
            quantity = item_quant_map.get('quantity')
            inventory_item_detail = '{}\t{}\t{}'.format(
                item.label,
                quantity,
                item.cost,
            )
            inventory_content.append(inventory_item_detail)

        # Render location price list
        price_list_content = [
            '{}\n{}\t{}\t{}\n{}'.format('*'*30, 'Item', 'Code', 'Price', '*'*30)
        ]
        for item in self.curr_location.price_list:
            price_list_content.append(
                '{}\t{}\t{}'.format(
                    item.label, item.id, item.cost
                )
            )

        print(status)
        print()
        print('\n'.join(inventory_content))
        print()
        print('\n'.join(price_list_content))

    def parse_cmd_input(self, input_cmd):
        cmd, *args = input_cmd.split()
        error_msg = (
            "Invalid Input: {0}."
            " Please provide the correct command"
        )

        if cmd == 'b' or cmd == 'buy':
            try:
                # item_name, quantity = args
                item_name, quantity = args
                self.buy(item_name, int(quantity))
                return True
            except:
                print(error_msg.format(input_cmd))
                return False

        if cmd == 's' or cmd == 'sell':
            try:
                item_name, quantity = args
                self.sell(item_name, int(quantity))
                return True
            except Exception as e:
                print(e)
                print(error_msg.format(input_cmd))
                return False

        if cmd == 'r' or cmd == 'repay':
            try:
                amount = args[0]
                self.repay(int(amount))
                return True
            except:
                print(error_msg.format(input_cmd))
                return False

        if cmd == 'e' or cmd == 'end':
            try:
                self.goto()
                self.player.update_loan()
                self.max_turns = self.max_turns - 1
                return True
            except:
                print(error_msg.format(input_cmd))
                return False

    def prompt_input(self):
        # ask for input
        # validate
        # ask for input if wrong
        success = False
        while not success:
            print("**** Input *******************")
            input_cmd = input("Enter command: ")
            success = self.parse_cmd_input(input_cmd)
            
    def play_turn(self):
        self.render_turn()
        self.prompt_input()

    def run(self):
        self.goto()
        while self.max_turns:
            # pass
            # self.start_turn()
            # self.prompt_input()
            # self.end_turn()
            self.play_turn()
        print("****** End Of Game *******")

# # TODO
# class CommandParser():
#     def __init__(self, commands):
#         self.commands = []

#     def add_command(self, command, action, args=None, sep=' '):
#         pass

#     def parse_command(self):
#         pass

if __name__=='__main__':
    game = Game(
        ITEMS,
        LOCATIONS,
        PLAYER_CASH_AMOUNT,
        PLAYER_LOAN_AMOUNT,
        PLAYER_LOAN_RATE,
        GAME_MAX_TURNS
    )
    game.run()