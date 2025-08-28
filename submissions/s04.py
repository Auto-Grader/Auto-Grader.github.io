def bubble_sort(arr):
    # Not robust: will raise if arr contains None or uncomparable types
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return None


if __name__ == '__main__':
    a = [1, None, 2]
    bubble_sort(a)
    print(a)
