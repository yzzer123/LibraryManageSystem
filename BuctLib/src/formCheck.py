
LEGAL_STR = "!@~`#$%^&*()_-+=,<>./?\'\"{}\\|[];"
ILLEGAL_CHAR = 1
TOO_LONG = 2
TOO_SHORT = 3
LOW_SECURITY = 4
LENGTH_ERR = 5
OK = 0
FIRST_CHAR_ERR = 6


def check_pwd(pwd: str) -> int:
    """
    检查密码正确性
    :param pwd: 密码
    """
    digital_num = 0  # 数字个数
    alpha_num = 0  # 字母个数
    legal_char_num = 0 # 合法字符个数
    ch: str
    if len(pwd) < 6:
        return "密码太短了(大于6位)"
    elif len(pwd) > 40:
        return "密码太长(小于40位)"
    for ch in pwd:
        if ch.isdigit():
            digital_num += 1
        elif ch.isalpha():
            alpha_num += 1
        elif ch in LEGAL_STR:
            legal_char_num += 1
        else:
            return "密码包含空格或非法字符"

    if digital_num == 0 or alpha_num == 0 or legal_char_num == 0:
        return "密码必须包含字母、数字和字符"
    return ""


def check_phone(phone: str) -> int:
    if not phone.isdigit():
        return "电话号码必须为数字构成"
    elif len(phone) != 11:
        return "电话号码必须为11位"
    return ""


def check_user_name(name: str) -> int:
    """
    检查用户名
    :param name:
    :return:
    """
    if len(name) > 20:
        return TOO_LONG
    if not name[0].isalpha():
        return "用户名必须以字母开头"
    ch: str
    for ch in name:
        if ch.isdigit() or ch.isalpha() or ch == '_':
            continue
        return "用户名含非法字符(只能包含数字字母下划线)"
    return ""


def check_id(idnum: str) -> str:
    """
    检查学号和工号
    :param idnum: 学号或工号
    :return:
    """
    if not idnum.isalnum():
        return "学工号含不合法字符"

    if len(idnum) < 10:
        return "学工号太短"
    elif len(idnum) > 10:
        return "学工号太长"
    return ""


def check_email(email: str) -> int:
    if not email.endswith('.com'):
        return ILLEGAL_CHAR
    emial_sep = email[:-4].split('@')
    if len(emial_sep) != 2:
        return ILLEGAL_CHAR

    ch: str
    for ch in emial_sep[0]:
        if ch.isdigit() or ch.isalpha() or ch == '_':
            continue
        return ILLEGAL_CHAR
    if (not emial_sep[1][0].isalnum()) or emial_sep[1][-1] == '.':
        return ILLEGAL_CHAR
    for index, ch in enumerate(emial_sep[1]):
        if ch.isalnum() or (ch == '.' and emial_sep[1][index-1] != '.'):
            continue
        return ILLEGAL_CHAR
    return ""


