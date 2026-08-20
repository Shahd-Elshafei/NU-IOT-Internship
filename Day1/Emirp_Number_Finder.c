/*
 * task1.c
 * 
 * Copyright 2026  <Intern@Intern>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

// 1. Structure to bundle paired calculation metrics
typedef struct {
    int prime;
    int inverse;
    int difference;
} EmirpData;

// 2. Helper Function: Validate primality
bool isPrime(int num) {
    if (num < 2) return false;
    for (int i = 2; i <= sqrt(num); i++) {
        if (num % i == 0) return false;
    }
    return true;
}

// 3. Helper Function: Reverse an integer's digits
int getInverse(int num) {
    int reversed = 0;
    while (num > 0) {
        reversed = reversed * 10 + (num % 10);
        num /= 10;
    }
    return reversed;
}

// 4. Main Program Routine
int main(int argc, char **argv)
{
    int A, B;
    
    printf("Enter A and B\n");
    scanf("%d %d", &A, &B);
    
    // Check the inputs - positive
    if (A <= 0 || B <= 0) {
        printf("[Error] A or B is not postive integer\n");
        return 0;
    }
    
    // Logical arrange
    if (A >= B) {
        printf("[Error] A is larger than B\n");
        return 0;
    }
    
    // Even check validation logic
    if ((A % 2 == 0 && A != 2) || B % 2 == 0) {
        printf("[Info] A OR B are even numbers B\n");
        return 0;
    }

    // Allocate memory based on the worst-case size of the input range
    int maxPossiblePairs = B - A + 1;
    EmirpData *pairs = malloc(maxPossiblePairs * sizeof(EmirpData));
    if (pairs == NULL) {
        printf("[Error] Memory allocation failed!\n");
        return 1;
    }

    int pairCount = 0;

    // Filter, evaluate, and dynamically populate your array structural data
    for (int i = A; i <= B; i++) {
        if (isPrime(i)) {
            int inv = getInverse(i);
            
            // Structural constraint: The inverse must fall within the range [A, B]
            if (i != inv && inv >= A && inv <= B && isPrime(inv)) {
                pairs[pairCount].prime = i;
                pairs[pairCount].inverse = inv;
                pairs[pairCount].difference = abs(i - inv);
                pairCount++;
            }
        }
    }

    // Core execution boundary guard for empty result windows
    if (pairCount == 0) {
        printf("\nEmirp numbers from %d to %d:\nNone found.\n", A, B);
        free(pairs);
        return 0;
    }

    // Step 5: Print matching dataset cleanly to stdout
    printf("\nEmirp numbers from %d to %d:\n", A, B);
    for (int i = 0; i < pairCount; i++) {
        printf("%d, %d (diff = %d)\n", pairs[i].prime, pairs[i].inverse, pairs[i].difference);
    }

    // Step 6: Post-processing calculation loop to find min/max values
    int minDiff = pairs[0].difference;
    int maxDiff = pairs[0].difference;

    for (int i = 1; i < pairCount; i++) {
        if (pairs[i].difference < minDiff) minDiff = pairs[i].difference;
        if (pairs[i].difference > maxDiff) maxDiff = pairs[i].difference;
    }

    // Step 7: Print clean summary footer block
    printf("\nSummary:\n");
    printf("Total emirps found: %d\n", pairCount);

    // Dynamic print logic for Largest Difference matching pairs
    printf("Largest difference: %d (achieved by ", maxDiff);
    bool firstMax = true;
    for (int i = 0; i < pairCount; i++) {
        if (pairs[i].difference == maxDiff) {
            if (!firstMax) printf(",");
            printf("%d", pairs[i].prime);
            firstMax = false;
        }
    }
    printf(")\n");

    // Dynamic print logic for Smallest Difference matching pairs
    printf("Smallest difference: %d (achieved by ", minDiff);
    bool firstMin = true;
    for (int i = 0; i < pairCount; i++) {
        if (pairs[i].difference == minDiff) {
            if (!firstMin) printf(",");
            printf("%d", pairs[i].prime);
            firstMin = false;
        }
    }
    printf(")\n");

    // Clear runtime heap allocation block
    free(pairs);
    return 0;
}
