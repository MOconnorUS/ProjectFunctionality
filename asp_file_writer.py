
from typing import TextIO
from asp_file_functions import ASP_ENCODING
from templates import ASP_HEADER_INFORMATION, ASP_FOOTER_INFORMATION

ASP_ENCODING_FILE_PATH = "./ASP Encoding/project_encoding.txt"

def iterative_writer(write_list: list, file: TextIO) -> None:
    """
    Write ASP list information to an open text file.

    @param write_list the list to write to the file.
    @param file the open text file to write to.
    """

    for item in write_list:
        file.write(f'{item}\n')

    file.write('\n')
    return None

def file_writer(
        company_predicates: list, 
        time_predicates: list, 
        percentage_move_predicates: list, 
        profit_predicate: list,
        bought_predicates: list,
        sold_predicates: list,
        position_predicates: list,
    ) -> None:
    """
    Writes all ASP formatted information to the designated project encoding text file.

    @param company_predicates the predicates containing all company information formatted for ASP.
    @param time_predicates the predicates containing all time information formatted for ASP.
    @param percentage_move_predicates the predicates containing all percentage move information formatted for ASP.
    @param profit_predicate the predicates containing the profit information formatted for ASP.
    @param bought_predicates the bought predicates containing the bought companies formatted for ASP.
    @param sold_predicates the sold predicates containing the sold companies formatted for ASP.
    @param position_predicates the predicates containing the current position information formatted for ASP.
    """

    with open(ASP_ENCODING_FILE_PATH, 'w') as file:
        iterative_writer(ASP_HEADER_INFORMATION, file)
        iterative_writer(time_predicates, file)
        iterative_writer(ASP_ENCODING, file)
        iterative_writer(company_predicates, file)
        iterative_writer(position_predicates, file)
        iterative_writer(percentage_move_predicates, file)
        iterative_writer(bought_predicates, file)
        iterative_writer(sold_predicates, file)
        iterative_writer(profit_predicate, file)
        iterative_writer(ASP_FOOTER_INFORMATION, file)

    file.close()

    return None
