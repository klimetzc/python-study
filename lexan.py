# import re # regular expressions для обработки инпут файла
# re оказался ненужен, но оставлю на память
import os

if os.name == 'nt':  # Просто наводим красоту для cmd (Windows)
    import ctypes

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Далее классы лексемм и запишем пары ключ-значение в словари
keywords = {
    'if': '1',
    'else': '2',
    'return': 'return'
}
separators = {
    '[': '1',
    ']': '2',
    '{': '3',
    '}': '4',
    ';': '5',
    '=': '6',
    '(': '7',
    ')': '7',
    '>': '9',
    '<': '10',
    '>=': '11',
    '<=': '12',
    '==': '13',
    '+': '14',
    '-': '15',
    '*': '16',
    '/': '17',
    '%': '18',
    '+=': '19',
    '-=': '20',
    '*=': '21',
    '/=': '22',
    '\'': '23',
    '\"': '24',
    '.': '25'
}
identifiers = {
    'id': '8',
    'NONE': '----'
}
constants = {
    'const': '9'
}
id_set = frozenset(['_', '$'])  # Символы, которые могут быть в имени Идентификатора

# Запишем ключи в соответствующие им массивы, чтобы проверить вхождение лексеммы в класс
kw = keywords.keys()
sp = separators.keys()
ids = identifiers.keys()
cs = constants.keys()

descr_text = []  # Дескрипторный текст
table_output = []  # Таблица классов
temp = None  # Костыльная переменная для соединения сепараторов :) Используется в функции table_append
lexemaTRUE, lexemaFALSE = 'ДОПУСТИТЬ','ОТВЕРГНУТЬ'
lexemaRESULT = lexemaTRUE


def iscorrect(any_str: str):
    """
    Функция определяет является ли лексемма корректным Идентификатором
    На вход подаётся строка
    Вычитаем из строки множество допустимых спец. символов id_set
    и проверяем явлется ли оставшаяся часть набором цифр и букв
    """
    global id_set
    if not any_str[0].isnumeric():  # if any_str[0].isnumeric() == False:
        difference = set(any_str) - id_set
        final = ''
        for i in difference:
            final += i
        return final.isalnum()
    else:
        return False


def table_append(token, token_class, set_get: set, d_key): 
    """
    Функция формирует таблицу классов в таком виде:
    ЛЕКСЕММА КЛАСС_ЛЕКСЕММЫ ЗНАЧЕНИЕ
    На вход подаётся:
    token = анализируемая лексема
    token_class = Класс лексеммы, пишется строкой вручную
    set_get = Множество для выбора значения
    d_key = Ключ, по которому ищем значение
    """
    global table_output
    global temp
    nt = str(temp) + str(
        token)  # Складываем с предыдущим сепаратором, чтобы убедиться в (не)наличии сложного сепаратора(их 2 символов)
    if nt in sp:
        del table_output[:-4:-1]  # Удаляем последние три элемента таблицы, чтобы заменить их на сложный сепаратор
        table_output.append(nt)
        table_output.append(token_class)
        table_output.append(separators.get(str(nt)))
    else:
        table_output.append(token)
        table_output.append(token_class)
        table_output.append(set_get.get(str(d_key)))
        # print(temp, end= "    ")
        # print(nt)
        # Две строчки для отладки, чтобы понять почему сепараторы не складывались
    temp = table_output[-3]  # Каждый раз в temp обновляем лексемму


f = open('input.txt', 'r')  # Открываем файлик с программой для чтения
i = f.read()
count = 0
program = i.split('\n')
counter = 0
print('Входная программа для лексического анализа:\n')
for line in program:
    count += 1
    print("\033[33m {0} {1}\033[0m  {2}".format('#', count, line))

    tokens = line.split(' ')
    # print('Слова в строке: {}'.format(tokens))
    # Верхняя страка ыбал нужная для отладки, показывает список лексемм в строке

    for token in tokens:
        if token != '':  # Убираем лишние пробелы
            # Проверяем входит ли лексемма полностью в какой-то класс. В каждой первой строке условия мы добавляли
            # значение ключа в дескирпторный код, но потом получилось сделать это по таблице классов
            if token in kw:
                # descr_text.append(keywords.get(str(token)))
                table_append(token, 'KEYWORD', keywords, token)
            elif token in sp:
                # descr_text.append(separators.get(str(token)))
                table_append(token, 'SEPARATOR', separators, token)
            elif token.isnumeric():
                # descr_text.append(constants.get(str('const')))
                table_append(token, 'CONST', constants, 'const')
            elif iscorrect(token):
                # descr_text.append(identifiers.get(str('id')))
                table_append(token, 'IDENT', identifiers, 'id')
            elif not iscorrect(token):
                # Если целая лексемма не является часть класса, то читаем побуквенно и ищем в строке новые лексеммы
                x = []  # В массив побуквенно считывается лексемма
                for i in token:
                    if i not in sp:
                        x.append(i)

                    elif i in sp:
                        xs = ''.join(x)
                        #print(xs) #для отладки
                        x = []
                        if xs in kw:
                            # descr_text.append(keywords.get(xs))
                            table_append(xs, 'KEYWORDS', keywords, xs)
                        elif xs.isdigit():
                            # descr_text.append(constants.get('const'))
                            table_append(xs, 'CONSTS', constants, 'const')
                        elif len(xs) != 0:  # len(xs)!=0
                            if iscorrect(xs):
                                table_append(xs, 'IDENTS', identifiers, 'id')
                            else:
                                table_append(xs, '----', identifiers, 'NONE')
                                lexemaRESULT = lexemaFALSE
                            # descr_text.append(identifiers.get('id'))
                        
                        # descr_text.append(separators.get(str(i)))
                        table_append(i, 'SEPARATORS', separators, i)
                        

f.close()  # Обязательно закрыть файлик
# print(table_output) Для отладки

# Дальше просто вывод результатов, комментировать не буду
print('\033[36m{:~^50}\033[0m'.format('ТАБЛИЦА КЛАССОВ'))
tnames = ['ЛЕКСЕММА', 'КЛАСС', 'ДЕСКРИПТОР']
for i in tnames:
    print("{:25}".format(i), end=' ')
print('\n')
tcount = 0
for i in table_output:
    if tcount < 2:
        print("{:25}".format(i), end=' ')
        # print(i, end='          ')
        tcount += 1
    else:
        tcount = 0
        print(i)

print('\n')
print('{:-^50}'.format('ДЕСКРИПТОРНЫЙ ТЕКСТ') + '\n')
descr_text = table_output[2::3]
for i in descr_text:
    print(i, end=' ')
if lexemaRESULT == lexemaTRUE:
    print('\n', "\033[42m\033[1m{: ^50}\033[0m".format(lexemaRESULT))
elif lexemaRESULT == lexemaFALSE:
    print('\n', "\033[41m\033[1m{: ^50}\033[0m".format(lexemaRESULT))
print('\n', 'Кол-во лексемм:', len(descr_text))
print(' Кол-во ячеек в таблице: ', len(table_output))
if os.name == 'nt':
    os.system("PAUSE")
