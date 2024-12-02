#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

// Quicksort implementation using MPI

void quicksort(int *arr, int low, int high);
int partition(int *arr, int low, int high);

int main(int argc, char *argv[])
{
    int rank, size, n = 16, local_n;
    int *arr = NULL, *local_arr = NULL;
    int pivot;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (rank == 0)
    {
        // Master process initializes the array
        arr = (int *)malloc(n * sizeof(int));
        for (int i = 0; i < n; i++)
        {
            arr[i] = rand() % 100;
        }
        printf("Unsorted array: ");
        for (int i = 0; i < n; i++)
        {
            printf("%d ", arr[i]);
        }
        printf("\n");
    }

    // Scatter data to all processes
    local_n = n / size;
    local_arr = (int *)malloc(local_n * sizeof(int));
    MPI_Scatter(arr, local_n, MPI_INT, local_arr, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    // Local quicksort
    quicksort(local_arr, 0, local_n - 1);

    // Gather sorted subarrays back to master
    MPI_Gather(local_arr, local_n, MPI_INT, arr, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank == 0)
    {
        printf("Partially sorted array: ");
        for (int i = 0; i < n; i++)
        {
            printf("%d ", arr[i]);
        }
        printf("\n");
        free(arr);
    }

    free(local_arr);
    MPI_Finalize();
    return 0;
}

int partition(int *arr, int low, int high)
{
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++)
    {
        if (arr[j] <= pivot)
        {
            i++;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    return i + 1;
}

void quicksort(int *arr, int low, int high)
{
    if (low < high)
    {
        int pi = partition(arr, low, high);
        quicksort(arr, low, pi - 1);
        quicksort(arr, pi + 1, high);
    }
}
