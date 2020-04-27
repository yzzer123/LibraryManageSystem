
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
        elif ch.islower() or ch.isupper():
            alpha_num += 1
        elif ch in LEGAL_STR:
            legal_char_num += 1
        else:
            return "密码包含空格或非法字符"
    cnt = 0
    for i in (digital_num, alpha_num, legal_char_num):
        if i != 0:
            cnt += 1
    if cnt == 1:
        return "密码必须至少包含字母、数字和字符中的两种"

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
    if not (name[0].islower() or  name[0].isupper()):
        return "用户名必须以字母开头"
    ch: str
    for ch in name:
        if ch.isdigit() or ch.islower() or ch.isupper() or ch == '_':
            continue
        return "用户名含非法字符(只能包含数字字母下划线)"
    return ""


def check_id(idnum: str) -> str:
    """
    检查学号和工号
    :param idnum: 学号或工号
    :return:
    """
    if not idnum.isdigit():
        return "学工号含不合法字符"

    if len(idnum) < 10:
        return "学工号太短"
    elif len(idnum) > 10:
        return "学工号太长"
    return ""


def check_email(email: str) -> int:
    if not (email.endswith('.com') or email.endswith('.cn') or email.endswith('.net')):
        return "邮箱要以.com .cn .net结尾"
    emial_sep = email[:-4].split('@')
    if len(emial_sep) != 2:
        return "邮箱只能包含一个@"
    ch: str
    for ch in emial_sep[0]:
        if ch.isdigit() or ch.isupper() or ch.islower() or ch == '_':
            continue
        return "@前只能包含字母 下划线 和数字"
    if (not (emial_sep[1][0].islower() or emial_sep[1][0].isupper() or emial_sep[1][0].isdigit())) or emial_sep[1][-1] == '.':
        return "邮箱后缀格式非法"
    for index, ch in enumerate(emial_sep[1]):
        if ch.isupper() or ch.islower() or ch.isdigit() or (ch == '.' and emial_sep[1][index-1] != '.'):
            continue
        return "邮箱后缀包含非法字符"
    return ""


