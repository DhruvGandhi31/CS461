#include <stdio.h>
#include <omp.h>

void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

int partition(int arr[], int low, int high)
{
    int pivot = arr[high];
    int i = (low - 1);
    for (int j = low; j < high; j++)
    {
        if (arr[j] <= pivot)
        {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

void parallel_quicksort(int arr[], int low, int high)
{
    if (low < high)
    {
        int pi = partition(arr, low, high);

// Parallel regions using OpenMP
#pragma omp parallel sections
        {
#pragma omp section
            parallel_quicksort(arr, low, pi - 1);

#pragma omp section
            parallel_quicksort(arr, pi + 1, high);
        }
    }
}

int main()
{
    int arr[] = {10, 80, 30, 90, 40, 50, 70};
    int n = sizeof(arr) / sizeof(arr[0]);

// Parallel region with single thread to kick off quicksort
#pragma omp parallel
    {
#pragma omp single
        parallel_quicksort(arr, 0, n - 1);
    }

    printf("Sorted array: ");
    for (int i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");
    return 0;
}
