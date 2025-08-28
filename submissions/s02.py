def bubble_sort(arr):
    # Incorrect semantics if teacher insisted in-place, but we accept return
    b = arr.copy()
    n = len(b)
    for i in range(n):
        for j in range(0, n - i - 1):
            if b[j] > b[j + 1]:
                b[j], b[j + 1] = b[j + 1], b[j]
    return b


if __name__ == '__main__':
    a = [3, 4, 1]
    print(bubble_sort(a))
