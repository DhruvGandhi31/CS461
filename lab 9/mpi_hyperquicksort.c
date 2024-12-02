#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

void quicksort(int *array, int low, int high)
{
    if (low < high)
    {
        int pivot = array[high];
        int i = (low - 1);
        for (int j = low; j < high; j++)
        {
            if (array[j] < pivot)
            {
                i++;
                int temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
        }
        int temp = array[i + 1];
        array[i + 1] = array[high];
        array[high] = temp;
        int pi = i + 1;

        quicksort(array, low, pi - 1);
        quicksort(array, pi + 1, high);
    }
}

void merge(int *array, int *left, int left_size, int *right, int right_size)
{
    int i = 0, j = 0, k = 0;

    while (i < left_size && j < right_size)
    {
        if (left[i] <= right[j])
        {
            array[k++] = left[i++];
        }
        else
        {
            array[k++] = right[j++];
        }
    }

    while (i < left_size)
    {
        array[k++] = left[i++];
    }

    while (j < right_size)
    {
        array[k++] = right[j++];
    }
}

int main(int argc, char **argv)
{
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int n = 100; // Number of elements to sort
    int *array = NULL;

    if (rank == 0)
    {
        array = malloc(n * sizeof(int));
        for (int i = 0; i < n; i++)
        {
            array[i] = rand() % 1000; // Random numbers between 0 and 999
        }
    }

    // Broadcast the size of the array to all processes
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // Calculate the size of each subarray
    int local_n = n / size;
    int *local_array = malloc(local_n * sizeof(int));

    // Scatter the array to all processes
    MPI_Scatter(array, local_n, MPI_INT, local_array, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    // Sort the local array
    quicksort(local_array, 0, local_n - 1);

    // Gather sorted subarrays
    int *sorted_array = NULL;
    if (rank == 0)
    {
        sorted_array = malloc(n * sizeof(int));
    }
    MPI_Gather(local_array, local_n, MPI_INT, sorted_array, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    // Only the root process will merge the sorted subarrays
    if (rank == 0)
    {
        int *final_array = malloc(n * sizeof(int));
        int *left = sorted_array;
        int *right = sorted_array + local_n;

        for (int i = 1; i < size; i++)
        {
            merge(final_array, left, local_n, right, local_n);
            left = final_array;
            right += local_n;
        }

        // Print the sorted array
        for (int i = 0; i < n; i++)
        {
            printf("%d ", final_array[i]);
        }
        printf("\n");

        free(array);
        free(sorted_array);
        free(final_array);
    }

    free(local_array);
    MPI_Finalize();
    return 0;
}