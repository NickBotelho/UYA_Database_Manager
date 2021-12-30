class Symbols_Unicode:
    DEFAULT = '3038'
    BLUE = '3039'
    GREEN = '3041'
    PINK = '3042'
    WHITE = '3043'
    GRAY = '3044'
    BLACK = '3045'

    SELECT_BUTTON = '3141'
    CROSS = '3130'

COLOR_MAP_1 = {
    '1': Symbols_Unicode.DEFAULT,
    '2': Symbols_Unicode.BLUE,
    '3': Symbols_Unicode.GREEN,
    '4': Symbols_Unicode.PINK,
    '5': Symbols_Unicode.WHITE,
    '6': Symbols_Unicode.GRAY,
    '7': Symbols_Unicode.BLACK
}
CLANTAG_ALLOWED_CHARACTERS = {
    '3631': 'A', '3632': 'B', '3633': 'C', '3634': 'D',
    '3635': 'E', '3636': 'F', '3637': 'G', '3638': 'H',
    '3639': 'I', '3641': 'J', '3642': 'K', '3643': 'L',
    '3644': 'M', '3645': 'N', '3646': 'O', '3730': 'P',
    '3731': 'Q', '3732': 'R', '3733': 'S', '3734': 'T',
    '3735': 'U', '3736': 'V', '3737': 'W', '3738': 'X',
    '3739': 'Y', '3741': 'Z',
    '3330': '0', '3339': '9', '3338': '8', '3337': '7',
    '3336': '6', '3335': '5', '3334': '4', '3333': '3',
    '3332': '2', '3331': '1',
    '3431': 'a', '3432': 'b', '3433': 'c', '3434': 'd',
    '3435': 'e', '3436': 'f', '3437': 'g', '3438': 'h',
    '3439': 'i', '3441': 'j', '3442': 'k', '3443': 'l',
    '3444': 'm', '3445': 'n', '3446': 'o', '3530': 'p',
    '3531': 'q', '3532': 'r', '3533': 's', '3534': 't',
    '3535': 'u', '3536': 'v', '3537': 'w', '3538': 'x',
    '3539': 'y', '3541': 'z',
    '3230': ' ', '3231': '!', '3430': '@', '3233': '#',
    '3234': '$', '3235': '%', '3545': '^', '3236': '&',
    '3241': '*', '3238': '(', '3239': ')', '3546': '_',
    '3242': '+', '3742': '{', '3744': '}', '3232': '"',
    '3341': ':', '3346': '?', '3343': '<', '3345': '>',
    '3244': '-', '3344': '=', '3246': '/', '3542': '[',
    '3544': ']', '3342': ';', '3237': "'", '3245': '.',
    '3243': ',',
    '3030': 'empty',
    # Symbols_Unicode.DEFAULT: 'default color',
    Symbols_Unicode.BLUE: 'blue',
    Symbols_Unicode.GREEN: 'green',
    Symbols_Unicode.PINK: 'pink',
    Symbols_Unicode.WHITE: 'white',
    Symbols_Unicode.GRAY: 'gray',
    Symbols_Unicode.BLACK: 'black',
}