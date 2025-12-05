# Template the manage the information for each company
COMPANY_INFO_TEMPLATE = {
    'Bid Price': float,
    'Ask Price': float,
    'Bid Size': int,
    'Ask Size': int,
    'High Price': float,
    'Low Price': float,
    'Close Price': float
}

# Template to manage the information keys for each company
COMPANY_INFO_LIST = [
    'Bid Price',
    'Ask Price',
    'Bid Size',
    'Ask Size',
    'High Price',
    'Low Price',
    'Close Price'
]

# Template to manage the beginning header cells for each company
COMPANY_CELL_TITLES = [
    'B',
    'I',
    'P',
    'W',
    'AD',
    'AK',
    'AR',
    'AY',
    'BF',
    'BM',
    'BT'
]

# Template to manage the close price cells for each company
COMPANY_CLOSE_CELLS = [
    'H',
    'O',
    'V',
    'AC',
    'AJ',
    'AQ',
    'AX',
    'BE',
    'BL',
    'BS',
    'BZ'
]

# Template to manage the information cells for each company
COMPANY_INFO_CELLS = {
    0: [
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H'
    ],
    1: [
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        'O'
    ],
    2: [
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V'
    ],
    3: [
        'W',
        'X',
        'Y',
        'Z',
        'AA',
        'AB',
        'AC'
    ],
    4: [
        'AD',
        'AE',
        'AF',
        'AG',
        'AH',
        'AI',
        'AJ'
    ],
    5: [
        'AK',
        'AL',
        'AM',
        'AN',
        'AO',
        'AP',
        'AQ'
    ],
    6: [
        'AR',
        'AS',
        'AT',
        'AU',
        'AV',
        'AW',
        'AX'
    ],
    7: [
        'AY',
        'AZ',
        'BA',
        'BB',
        'BC',
        'BD',
        'BE'
    ],
    8: [
        'BF',
        'BG',
        'BH',
        'BI',
        'BJ',
        'BK',
        'BL'
    ],
    9: [
        'BM',
        'BN',
        'BO',
        'BP',
        'BQ',
        'BR',
        'BS'
    ],
    10: [
        'BT',
        'BU',
        'BV',
        'BW',
        'BX',
        'BY',
        'BZ'
    ]
}

# Introductary comments to be placed at the top of the ASP file during each iteration
ASP_HEADER_INFORMATION = [
    '% CSE 620 Final Project - Day Trading Profit Capitalization',
    "% Author: Matthew O'Connor",
    "% KRR Methodology: Temporal Projection"
]

# Show statements to be written at the bottom of the ASP encoding
ASP_FOOTER_INFORMATION = [
    "#show monitor/1.",
    "#show buy/2.",
    "#show sell/2."
]