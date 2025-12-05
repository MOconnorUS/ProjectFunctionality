import subprocess

from asp_file_functions import modify_budget, modify_profit, mofity_bought_sold

ENCODING_PATH = './asp encoding/project_encoding.txt'

def run_clingo() -> tuple[list, bool]:
    """
    Runs clingo on the encoded ASP text file and returns the answer output and satisfiability.

    @return a tuple containing the answer set and satisfiability output by the clingo execution.
    """

    clingo_result = subprocess.run(['clingo', ENCODING_PATH], capture_output=True, text=True)
    output = clingo_result.stdout.split('\n')

    answer_set = []
    satisfiable = False
    
    for item in output:
        if 'Answer:' in item:
            answer_set = output[output.index(item) + 1].split(' ')
            satisfiable = False if 'unsatisfiable' in output[output.index(item) + 2].lower() else True
            break

    return answer_set, satisfiable

def numeric_conversion(input: str) -> float:
    """
    Converts all ASP value inputs into valid float strings.

    @param input the ASP input.

    @return a float string of the value in the input.
    """

    return float(input) / 100

def parse_answer_set(answer_set: list, company_info: dict) -> None:
    """
    Interprets the answer set that was parsed from the output of the ASP program and performs any actions
    if necessary.

    @param answer_set the list containing the satisfiable answer provided by the ASP program.
    @param company_info the dictionary containing all company information.
    """

    for ans in answer_set:
        if 'monitor' in ans:
            continue

        temp = ans[ans.find('(') + 1 : -1].split(',')
        temp_num = numeric_conversion(temp[1])

        if 'buy' in ans:
            modify_budget(temp_num, temp[0], company_info)
            mofity_bought_sold(temp[0], 'bought')
            print(f'BUYING: {ans}')
        
        if 'sell' in ans:
            modify_profit(temp_num, temp[0], company_info)
            mofity_bought_sold(temp[0], 'sold')
            print(f'SELLING: {ans}')

    return None
