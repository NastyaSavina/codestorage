def main():
    arr = [1, 21, 131, 3, 4234, 23, 42345]

    counter: int = 0
    countMenshe4 = 0

    arrLen = len(arr)

    while counter < arrLen:
        if arr[counter] < 4:
            countMenshe4 += 1

        counter += 1

    print(countMenshe4)

if __name__ == "__main__":
    main()