from mytasks import add

if __name__ == '__main__':
    result = add.delay(2, 2)
    print(result.id)
