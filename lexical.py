'''
__title__ = ''
__author__ = 'CleverApril'
__mtime__ = '2016-05-05'
'''

import string

# 保留字
_key = ('program', 'type', 'integer', 'char', 'var', 'begin', 'end', 'read', 'write', 'while', 'if',
        'procedure', 'array', 'of', 'record', 'then', 'else', 'fi', 'do', 'endwh', 'return'
        )
# 界限符
_siginal = {'+': 'PLUS', '-': 'MINUS', '*': 'TIMES', '/': 'OVER', '(': 'LPAREN', ')': 'RPAREN',
            ';': 'SEMI', '[': 'LMIDPAREN', ']': 'RMIDPAREN', '=': 'EQ', '<': 'LT', 'EOF': 'ENDFILE',
            '.':'DOT',',':'COMMA'}
_nochar = '@%^&*~$'   # 标识符中的非法字符

_wrong = {'No.1': "数字中含有字母",
          'No.2': "数字以0开头",
          'No.3': "标识符含有非法字符",
          'No.4': "字符表示错误",
          'No.5': "数字中含有多个小数点"
          }

_content = ''   # 程序内容
_line = 1       # 代码行数
_word = ''      # 分析出的单词
_mean = ''      # 词法信息
_t = 0          # 下标
digit_state = 0  # 数字状态
char_state = 0  # 字符状态


# .............消除注释.................
def delete_comment():
    global _content
    state = 0
    index = -1

    for c in _content:
        index += 1

        if state == 0:
            if c == '{':
                state = 1
                startIndex = index

        elif state == 1:
            if c == '}':
                endIndex = index
                comment = _content[startIndex: endIndex + 1]
                _content = _content.replace(comment, '')
                index = startIndex - 1
                state = 0


# ..........获取程序代码.................
def get_program():
    global _content
    program = open(r'E:\program.txt', 'r')

    for line in program:   # 会读取一整行
        if line != '\n':
            _content = "%s%s" % (_content, line.lstrip())
        else:
            _content = "%s%s" % (_content, line)
    _content += '####'
    program.close()


# ............分析程序..................
def lexical(program):
    global _word, _t, _mean, char_state, digit_state

    _word = ''
    ch = program[_t]
    _t += 1
    while ch == ' ':      # 跳过空白字符
        ch = program[_t]
        _t += 1

# .........标识符 letter(letter|digit)*...............
    if ch.isalpha():
        while ch.isalpha() or ch.isalnum() or ch in _nochar:
            _word += ch
            ch = program[_t]
            _t += 1

        _t -= 1
        for char in _nochar:
            if char in _word:
                _mean = 'No.3'  # 错误代码，标识符含有非法字符
                break
            else:
                _mean = 'ID'

        if _word in _key:  # 判断是否为保留字
            _mean = _word.upper()

# .........字符  '(letter|digit)'........
    elif ch == '\'':
        while ch.isalpha() or ch.isalnum() or ch == '\'' or ch in _nochar:
            _word += ch
            if char_state == 0:
                if ch == '\'':
                    char_state = 1
            elif char_state == 1:
                if ch.isalpha() or ch.isalnum():
                    char_state = 2
                else:
                    char_state = 3

            elif char_state == 2:
                if ch == '\'':
                    char_state = 4
                else:
                    char_state = 3

            ch = program[_t]
            _t += 1
        _t -= 1
        if char_state == 4:
            _mean = 'INCHAR'
        if char_state == 3:
            _mean = 'No.4'    # 错误代码，字符表示错误
        char_state = 0


# .........无符号整数  digit(digit)*.................
    # elif ch.isalnum():

        # while ch.isalnum() or ch.isalpha():
        # _word += ch
        # if digit_state == 0:
        # if ch == '0':
        # digit_state = 1
        # else:
        # digit_state = 2
        # ch = program[_t]
        # _t += 1

        # for c in _word:
        # if c.isalpha():
        # _mean = 'No.1'     # 错误代码，数字中含有字母
        # digit_state = 0

        # if _mean != 'No.1':
        # if digit_state == 1:
        # _mean = 'No.2'     # 错误代码，数字以0开头
        # digit_state = 0
        # else:
        # digit_state = 0
        # _mean = 'INTC'
        # _t -= 1

# ...........(add) 无符号实数  ............................
    elif ch.isalnum():
        while ch.isalnum() or ch.isalpha() or ch == '.':
            _word += ch
            if digit_state == 0:
                if ch == '0':
                    digit_state = 1
                else:
                    digit_state = 2
            elif digit_state == 1:
                if ch == '.':
                    digit_state = 3
                else:
                    digit_state = 5
            elif digit_state == 2:
                if ch == '.':
                    digit_state = 3
            ch = program[_t]
            _t += 1

        for c in _word:
            if c.isalpha():
                _mean = 'No.1'  # 错误代码，数字中含有字母
                digit_state = 0

        if _mean != 'No.1':
            if digit_state == 5:
                _mean = 'No.2'  # 错误代码，数字以0开头
                digit_state = 0
            else:
                digit_state = 0
                if '.' not in _word:
                    _mean = 'INTC'
                else:
                    if _word.count('.') == 1:
                        _mean = 'FRACTION'
                    else:
                        _mean = 'No.5'  # 错误代码，数字中含有多个小数点
        _t -= 1

# ...............单分界符...............
    elif ch in _siginal:
        _word = ch
        _mean = _siginal[ch]
# ..............赋值符.................
    elif ch == ':':
        _word = ch
        ch = program[_t]

        if ch == '=':
            _word += ch
            _t += 1
            _mean = 'ASSIGN'
# ............... 换行符................
    elif ch == '\n':
        _mean = 'enter'              # 换行符


if __name__ == '__main__':
    get_program()
    # print(_content)
    delete_comment()
    # print(_content)
    token_file = open(r'E:\token.txt', 'w')

    while _content[_t] != '#':
        lexical(_content)
        if _mean == 'enter':
            _line += 1
        elif _mean in _wrong:
            print(str(_line) + '  ' + _word + '  ' + _wrong[_mean])
        else:
            token_file.write(
                '{0} {1} {2}\n'.format(_line, _mean, _word))
    token_file.close()
