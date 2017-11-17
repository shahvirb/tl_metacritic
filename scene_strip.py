import re

def strip_title(title):
    m = re.search('(.*)-', title)
    return m.group(1)

def main():
    while True:
        title = raw_input('>    ')
        stripped = strip_title(title)
        print(stripped)

if __name__ == '__main__':
    main()