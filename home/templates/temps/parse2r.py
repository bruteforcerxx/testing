from string_reader import string

def parse(a):
    print(f'{len(string)} characters detected from string.')
    print(f'Parsing {len(string)} characters from detected string...')

    a = a.replace("""dash""", """.""")
    print('Parsing completed.')

    return a


def method_1():
    data = input('Enter file name->(example.html): ')

    try:
        text_file = open(data, "r")
        data_content = text_file.read()
        text_file.close()
        parsed_data = parse(data_content)
        print(f'writing to new file..')
        text_file = open(f"new_{data}", "w")
        text_file.write(parsed_data)
        text_file.close()
        print(f" new_{data} file has been created successfully!")
    except Exception as e:
        print(e)


def method_2():
    try:
        parsed_data = parse(string)
        text_file = open(f"new_string_data.html", "w")
        print(f'writing to new file..')
        text_file.write(parsed_data)
        text_file.close()
        print(f"new_string_data.html file has been created successfully!")
    except Exception as e:
        print(e)

# method_2()
method_1()


