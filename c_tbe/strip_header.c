#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "strip_header.h"

#define MAX_LINE_LENGTH 1024

// Function to strip the header and return metadata
Metadata strip_header(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }

    Metadata metadata = {NULL, NULL, 0}; // Initialize empty metadata
    char line[MAX_LINE_LENGTH];
    int is_first_line = 1; // Flag to skip the first line (header row)

    while (fgets(line, sizeof(line), file)) {
        // Trim newline character
        line[strcspn(line, "\n")] = 0;

        // Skip the first line (column headers)
        if (is_first_line) {
            is_first_line = 0;
            continue;
        }

        // Stop parsing if we reach the main data section
        if (strncmp(line, "TBL Sites", 9) == 0) {
            break;
        }

        

        // Split the line into tokens
        char *tokens[3] = {NULL, NULL, NULL};
        int token_count = 0;

        // Handle splitting with consideration for empty fields
        char *token_start = line;
        while (token_start && token_count < 3) {
            char *token_end = strchr(token_start, ',');
            if (token_end) {
                *token_end = '\0'; // Replace ',' with null terminator
                tokens[token_count++] = token_start;
                token_start = token_end + 1;
            } else {
                tokens[token_count++] = token_start;
                token_start = NULL;
            }
        }

        // Fill missing tokens with empty strings
        for (int i = token_count; i < 3; i++) {
            tokens[i] = "";
        }

        // Assign key and value
        char *key = tokens[1];
        char *value = tokens[2];

        // Skip invalid lines (missing key or value)
        if (strlen(key) == 0 || strlen(value) == 0) {
            continue;
        }

        // Allocate memory for the new key-value pair
        metadata.count++;
        metadata.keys = realloc(metadata.keys, metadata.count * sizeof(char *));
        metadata.values = realloc(metadata.values, metadata.count * sizeof(char *));
        metadata.keys[metadata.count - 1] = strdup(key);
        metadata.values[metadata.count - 1] = strdup(value);
    }

    fclose(file);

    if (metadata.count == 0) {
        fprintf(stderr, "Warning: No header detected in file\n");
    }

    return metadata;
}

// Function to free allocated memory for metadata
void free_metadata(Metadata *metadata) {
    for (size_t i = 0; i < metadata->count; i++) {
        free(metadata->keys[i]);
        free(metadata->values[i]);
    }
    free(metadata->keys);
    free(metadata->values);
    metadata->keys = NULL;
    metadata->values = NULL;
    metadata->count = 0;
}
