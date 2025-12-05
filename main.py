import copy

from templates import (
    COMPANY_INFO_TEMPLATE
)
from file_reader import (
    open_workbook, 
    read_bids_for_percentages, 
    read_file, 
    read_time_from_file, 
    close_workbook
)
from asp_file_functions import (
    company_predicates, 
    time_predicates, 
    percentage_move_predicates, 
    profit_predicate,
    bought_sold_predicates,
    position_move_predicates
)
from asp_output_parsing import (
    run_clingo,
    parse_answer_set
)
from asp_file_writer import (
    file_writer
)

company_info = {}

INFO_START_CELL = '3'

DAY_ONE_PATHING = "Days/Day1.xlsx"
DAY_TWO_PATHING = "Days/Day2.xlsx"
DAY_THREE_PATHING = "Days/Day3.xlsx"

DAY_ONE_COMPANIES = 'FUBO,ROKU,AFRM,ABNB,ELF,NFLX,SPOT,ARM,GTLB,VEEV,XYZ'
DAY_TWO_COMPANIES = 'TSLA,CART,COIN,GBX,DASH,SNAP,APP,IONQ,TOST,HIMS,CMG'
DAY_THREE_COMPANIES = 'SBUX,CVNA,META,PLTR,FFIV,INTC,IBM,SAP,IBKR,NKE,ADBE'

def select_day() -> str:
    """
    Prompt the user to select a day (one, two, or three) to run that respective day.

    @return the day selected by the user.
    """

    day = input("Please enter the day you wish to run (one, two, or three): ")

    if 'one' in day or '1' in day:
        return 'one'
    
    if 'two' in day or '2' in day:
        return 'two'
    
    if 'three' in day or '3' in day:
        return 'three'
    
    return ''

def init_company_info(companies: list) -> None:
    """
    Initializes company info to the deepcopy of COMPANY_INFO_TEMPLATE.

    @param companies the list of companies to use as keys for company_info.
    """

    global company_info

    for company in companies:
        company_info[company] = copy.deepcopy(COMPANY_INFO_TEMPLATE)
        company_info[company]["Buy Price"] = 0.0

    company_info["Start Cell"] = INFO_START_CELL

    return None

def get_company_list(day: str) -> list:
    """
    Splits the companies for a day input by the user from a string into a list.

    @param day the day input by the user.

    @return a list of the companies for the day input by the user.
    """

    global DAY_ONE_COMPANIES, DAY_TWO_COMPANIES, DAY_THREE_COMPANIES

    if day == 'one':
        return DAY_ONE_COMPANIES.split(',')

    if day == 'two':
        return DAY_TWO_COMPANIES.split(',')
    
    if day == 'three':
        return DAY_THREE_COMPANIES.split(',')
    
    return 'RE-RUN THE SCRIPT AND PLEASE ENTER EITHER ONE, TWO, OR THREE FOR YOUR DAY OF CHOICE.'

def main() -> None:
    """
    Main method to tie all functionality together.
    """

    day = select_day()
    company_list = get_company_list(day)

    if type(company_list) is not list:
        return None
    
    init_company_info(company_list)

    wb_path = ''

    if day == 'one':
        wb_path = DAY_ONE_PATHING

    if day == 'two':
        wb_path = DAY_TWO_PATHING

    if day == 'three':
        wb_path = DAY_THREE_PATHING

    ws = open_workbook(wb_path)

    bid_dict = read_bids_for_percentages(ws, company_list)

    while company_info["Start Cell"] != '6401':
        time = read_time_from_file(ws, company_info["Start Cell"])
        read_file(ws, company_info)

        company_preds = company_predicates(company_info)
        time_preds = time_predicates(time)
        percentage_preds = percentage_move_predicates(company_info, bid_dict)
        profit_pred = profit_predicate()
        bought_pred, sold_pred = bought_sold_predicates()
        position_preds = position_move_predicates(company_info)

        file_writer(
            company_preds, 
            time_preds,
            percentage_preds, 
            profit_pred, 
            bought_pred, 
            sold_pred, 
            position_preds
        )

        answer_set, satisfiable = run_clingo()

        if satisfiable is False:
            print(f'UNSATISFIABLE PROGRAM')
            return None
        
        parse_answer_set(answer_set, company_info)
        # break

    close_workbook()
    
    return None

if __name__ == '__main__':
    main()