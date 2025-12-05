import random
import math

### IMPORTANT ###
# All numbers in ASP will be shifted left two positions
# So, 25 = 2500, 2.5 = 250, .25 = 25, .02 = 2

BUDGET = random.randint(10000, 60000)
PROFIT = 0.0

BOUGHT = []
SOLD = []
SHARES = {}

def asp_float_modification(value: float) -> int:
    """
    Transforms all standard values into ASP formed values which are essentially the current value * 100 rounded
    down.

    @param value the value to transform.

    @return the int value of the input * 100 rounded down.
    """

    return int(value * 100)

ASP_ENCODING = [
    "% Agent's budget'",
    f"#const budget={asp_float_modification(BUDGET)}.",

    "% The stoploss is -2.5 percent",
    "#const stoploss=-250.",

    "% The profitbar is 5 percent",
    "#const profitbar=500.",

    "% The buybar is -0.05 percent",
    "#const buybar=-5.",

    "% Agent buys company X at ask price Y",
    "buy(X, Y) :- company(X), askprice(Y, X), percentagemovetotal(P, X), P < buybar, not bought(X).",
    "-buy(X, Y) :- company(X), askprice(Y, X), percentagemovetotal(P, X), P > 0.",
    "-buy(X, Y) :- company(X), askprice(Y, X), percentagemovetotal(P, X), P <= 0, P > buybar.",
    "buy(X, Y)  :- company(X), askprice(Y, X), percentagemovepost(P, X), P < buybar, hour >= 4, hour < 8, not bought(X).",
    "-buy(X, Y) :- company(X), askprice(Y, X), percentagemovepost(P, X), P > 0.",
    "-buy(X, Y) :- company(X), askprice(Y, X), percentagemovepost(P, X), P < 0, P > buybar, hour >= 4, hour < 8.",
    "-buy(X, Y) :- company(X), askprice(Y, X), percentagemovetotal(P, X), P <= 0, P > buybar, percentagemovepost(P2, X), P2 < buybar, hour <= 4.",
    "-buy(X, Y) :- company(X), askprice(Y, X), percentagemovetotal(P, X), P <= 0, P > buybar, percentagemovepost(P2, X), P2 < buybar, hour > 8.",

    "% Agent sells company X at bid price Y",
    "sell(X, Y) :- company(X), bidprice(Y, X), bought(X), positionmovetotal(P, X), P > 0, P <= stoploss.",
    "sell(X, Y) :- company(X), bidprice(Y, X), bought(X), positionmovepost(P, X), P > 0, P <= stoploss, hour >= 4, hour < 8.",

    "% Agent choose to monitor company X",
    "monitor(X) :- company(X), -buy(X, Y), price(Y).",
    "monitor(X) :- company(X), bought(X), not buy(X, Y), price(Y).",
    "monitor(X) :- company(X), sold(X), not sell(X, Y), price(Y).",

    '% X is a price, either ask or bid',
    'price(Y) :- askprice(Y, X).',
    'price(Y) :- bidprice(Y, X).',

    ## Rules ##
    '%%%%%%%%%%%%%%%%%%%% RULES %%%%%%%%%%%%%%%%%%%%',
    "% Rule 1: Agent must close all positions by the end of after hours trading, 8PM",
    ":- not sold(X), not bought(X), company(X), hour = 8.",

    "% Rule 2: Agent cannot buy the same stock more than 1 time that day",
    ":- buy(X, Y), bought(X).",

    "% Rule 3: Agent cannot buy two different stocks at the same time",
    ":- buy(X, Y), buy(X2, Y2), X != X2, price(Y), company(X), company(X2), price(Y2).",

    "% Rule 4: Agent cannot buy & sell stocks at the same time",
    ":- buy(X, Y), sell(X2, Y2), company(X), price(Y).",
    ":- sell(X, Y), buy(X2, Y2), company(X), price(Y).",

    "% Rule 5: It is impossible to sell a stock Agent do not own",
    ":- sell(X, Y), not bought(X), price(Y), company(X).",

    "% Rule 6: Agent cannot sell two different stocks at the same time",
    ":- sell(X, Y), sell(X2, Y2), X != X2, price(Y), company(X), company(X2), price(Y2).",

    # "% Rule 7: Agent must sell if a move of >= -2.5 percent is observed. The duplicate below is for after hours",
    # "sell(X, Y) :- not sold(X), percentagemovetotal(P, X), P > stoploss, P < 0, company(X), price(Y), bought(X).",
    # "sell(X, Y) :- not sold(X), percentagemovepost(P, X), P > stoploss, P < 0, company(X), price(Y), hour >= 4, hour < 8.",

    "% Rule 8: Agent cannot sell the same stock more than 1 time that day",
    ":- sell(X, Y), sold(X).",

    "% Rule 9: Agent must spend as much of their balance as possible by the end of the day if not all",
    ":- budget > askprice(Y, X), hour = 8, not sold(X), company(X), price(Y).",

    "% Rule 10: Agent must sell if a move of >= 5 percent is observed. The duplicate below is for after hours",
    "sell(X, Y) :- not sold(X), percentagemovetotal(P, X), P >= profitbar, price(Y).",
    "sell(X, Y) :- not sold(X), percentagemovepost(P, X), P >= profitbar, price(Y), hour >= 4, hour < 8.",
    '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%',
]

############################################################
########## BELOW ARE PREDICATE CREATION FUNCTIONS ##########
############################################################
### The following rules will be written in by the script ###
# askprice(X, Y). <- X is the ask price of company Y
# bidprice(X, Y). <- X is the bid price of company Y
# asksize(X, Y). <- X is the ask size of company Y
# bidsize(X, Y). <- X is the bid size of company Y
# highprice(X, Y). <- X is the high price of company Y
# lowprice(X, Y). <- X is the low price of company Y
# closeprice(X, Y). <- X is the close price of company Y
# hour(X). <- X is the current hour
# minute(X). <- X is the current minute
# percentmovetotal(X, Y). <- X is the current percent total move of Y
# percentmovepost(X, Y). <- X is the current percent after hours move of Y
# bought(X). <- Agent has bought company X
# sold(X). <- Agent has sold company X
# profit(X). <- X is the profit on the day
# closedposition(X). <- Agent have closed out of position X
# price(X). <- X is a price (could be ask or bid, used to ensure safety in rules)

def company_predicates(company_info: dict) -> list:
    """
    Creates all company predicates which will be written to the ASP file. This is ONLY the askprice,
    bidprice, highprice, lowprice, and closeprice.

    @param company_info the dict containing all company information at a single time stamp.

    @return a list of strings ready to be written to the ASP file.
    """

    lines = []

    for company in company_info:
        if company == 'Start Cell':
            continue

        asp_bid = asp_float_modification(company_info[company]["Bid Price"])
        
        asp_ask = asp_float_modification(company_info[company]["Ask Price"])
        asp_ask_size = asp_float_modification(company_info[company]["Ask Size"] * 100)
        asp_bid_size = asp_float_modification(company_info[company]["Bid Size"] * 100)
        asp_high = asp_float_modification(company_info[company]["High Price"])
        asp_low = asp_float_modification(company_info[company]["Low Price"])
        asp_close = asp_float_modification(company_info[company]["Close Price"])

        lines.append(f'%%% INFORMATION FOR {company} %%%')

        lines.append(f'company({company.lower()}).')

        lines.append(f'% The bid price for {company}')
        lines.append(f'bidprice({asp_bid}, {company.lower()}).')
        
        lines.append(f'% The ask price for {company}')
        lines.append(f'askprice({asp_ask}, {company.lower()}).')
        
        lines.append(f'% The bid size for {company}')
        lines.append(f'bidsize({asp_bid_size}, {company.lower()}).')
        
        lines.append(f'% The ask size for {company}')
        lines.append(f'asksize({asp_ask_size}, {company.lower()}).')
        
        lines.append(f'% The high price for {company}')
        lines.append(f'highprice({asp_high}, {company.lower()}).')
        
        lines.append(f'% The low price for {company}')
        lines.append(f'lowprice({asp_low}, {company.lower()}).')
        
        lines.append(f'% The close price for {company}')
        lines.append(f'closeprice({asp_close}, {company.lower()}).')

        lines.append('%%%%%%%%%%%%%%%%%%%%%%%%')
    
    return lines

def time_predicates(timestamp: str) -> list:
    """
    Creates all timestamp predicates which will be written to the ASP file. These predicates only
    include hour and minute.

    @param timestamp the string representation of the timestamp.

    @return a list containing the ASP formatted timestamps.
    """

    timestamp_predicates = []
    timestamp_list = timestamp.split(':')

    timestamp_predicates.append('% The current hour')
    timestamp_predicates.append(
        f'#const hour={timestamp_list[0] if timestamp_list[0][0] != '0' else timestamp_list[0][1]}.'
    )

    timestamp_predicates.append('% The current minute')
    timestamp_predicates.append(
        f'#const minute={timestamp_list[1]}.' 
        if timestamp_list[1][0] != '0' else
        f'#const minute={timestamp_list[1][1]}.'
    )

    return timestamp_predicates

def percentage_move_predicates(company_info: dict, bid_dict: dict) -> list:
    """
    Creates all percentage move predicates which will be written to the ASP file. All percentage moves are
    based off the current bid price and the opening bid price.

    @param company_info the dictionary containing all company info for the timestamp.
    @param bid_price the dictionary containing the initial bid price and inital close bid price.

    @return a list containing the ASP formatted percentage movements.
    """

    percentage_predicates = []

    for company in company_info:
        if company == 'Start Cell':
            continue

        bid_price = float(company_info[company]["Bid Price"])
        init_bid_price = float(bid_dict[company]["First Bid"])
        init_close_bid_price = float(bid_dict[company]["Close Price"])

        bid_move_total = (bid_price - init_bid_price) / bid_price
        bid_move_post = (bid_price - init_close_bid_price) / init_close_bid_price
        
        asp_total = asp_float_modification(bid_move_total * 100)
        asp_post = asp_float_modification(bid_move_post * 100)

        percentage_predicates.append(f'%%% PERCENTAGE PREDICATES FOR {company} %%%')
        percentage_predicates.append(
            f'percentagemovetotal({asp_total}, {company.lower()}).'
        )

        percentage_predicates.append(
            f'percentagemovepost({asp_post}, {company.lower()}).'
        )

        percentage_predicates.append('%%%%%%%%%%%%%%%%%%%%%%')

    return percentage_predicates

def profit_predicate() -> list:
    """
    Creates the profit predicate formatted for ASP.

    @return a list containing the current profit predicate & comments formatted for ASP.
    """

    global PROFIT

    predicate = []

    asp_profit = asp_float_modification(PROFIT)

    predicate.append('% Current profit')
    predicate.append(f'#const profit={asp_profit}.')

    return predicate

def bought_sold_predicates() -> tuple[list, list]:
    """
    Packages BOUGHT and SOLD as predicates and returns both ASP formatted lists.

    @return a tuple containing a list of bought companies formatted for ASP and a list fo sold companies
    formatted for ASP.
    """

    global BOUGHT, SOLD

    bought_preds = []
    sold_preds = []

    if len(BOUGHT) == 0:
        bought_preds.append(f'bought(none).')
    
    if len(SOLD) == 0:
        sold_preds.append(f'sold(none).')

    for company in BOUGHT:
        bought_preds.append(f'bought({company.lower()}).')
    
    for company in SOLD:
        sold_preds.append(f'sold({company.lower()}).')

    return bought_preds, sold_preds

def position_move_predicates(company_info: dict) -> list:
    """
    Creates the predicates regarding the percentage move our entered positions. The default is 0 if we are not
    in that position.

    @param company_info the dict containing all companies for the day and their information.

    @return a list containing the ASP formatted predicates.
    """

    global BOUGHT, SOLD

    position_predicates = []

    for company in company_info:
        if company == "Start Cell":
            continue

        position_predicates.append(f"% The agent's position status of {company}")

        if company in BOUGHT and company not in SOLD:
            percentage_total = (
                (company_info[company]["Buy Price"] - company_info[company]["Bid Price"]) / 
                company_info[company]["Bid Price"]
            )

            percentage_post = (
                (company_info[company]["Buy Price"] - company_info[company]["Close Price"]) / 
                company_info[company]["Close Price"]
            )

            asp_percentage_total = asp_float_modification(percentage_total * 100)
            asp_percentage_post = asp_float_modification(percentage_post * 100)

            position_predicates.append(f"positionmovetotal({asp_percentage_total}, {company.lower()}).")
            position_predicates.append(f"positionmovepost({asp_percentage_post}, {company.lower()}).")
        else:
            position_predicates.append(f"positionmovetotal(0, {company.lower()}).")
            position_predicates.append(f"positionmovepost(0, {company.lower()}).")

    return position_predicates

############################################################
###### BELOW ARE CALCULATION & MODIFICATION FUNCTIONS ######
############################################################

def modify_budget(value: float, company: str, company_info: dict):
    """
    Modify the budget based on the value the stock was bought at.

    @param value the purchase price of the stock.
    @param company the string of the bought stock.
    @param company_info the dictionary containing the stock information.
    """

    global BUDGET, BOUGHT, SHARES

    purchasing_power = BUDGET * (1 / (11 - len(BOUGHT)))
    shares_to_buy = purchasing_power / value

    company_info[company.upper()]["Buy Price"] = value

    if shares_to_buy <= company_info[company.upper()]["Ask Size"] * 100:
        rounded_shares = math.floor(shares_to_buy)
        SHARES[company.upper()] = rounded_shares
        spent = value * rounded_shares
        BUDGET -= spent
    else:
        SHARES[company.upper()] = company_info[company.upper()]["Ask Size"] * 100
        spent = value * (company_info[company.upper()]["Ask Size"] * 100)
        BUDGET -= spent

    return None

def modify_profit(value: float, company: str, company_info: dict):
    """
    Modify the profit based on the value the stock was sold at.

    @param value the selling price of the stock.
    @param company the string of the stock sold.
    @param company_info the dictionary containing all company information.
    """

    global PROFIT, SHARES

    PROFIT += ((value - company_info[company.upper()]["Buy Price"]) * SHARES[company.upper()])
    return None

def mofity_bought_sold(company: str, deposit: str ='') -> None:
    """
    Appends a company to either bought or sold depending on the action noticed by the ASP output parser.

    @param company the company that was either bought or sold.
    @param deposit an optional string argument that determines if the company is appended to the bought
    or sold list.
    """

    global BOUGHT, SOLD

    if deposit == 'bought':
        BOUGHT.append(company.lower())
    
    if deposit == 'sold':
        SOLD.append(company.lower())

    return None
