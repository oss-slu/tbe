#ifndef STRIP_HEADER_H
#define STRIP_HEADER_H

#include <stddef.h> // For size_t

// Define a structure to store metadata as key-value pairs
typedef struct {
    char **keys;
    char **values;
    size_t count; // Number of metadata entries
} Metadata;

// Function prototypes
Metadata strip_header(const char *filename);
void free_metadata(Metadata *metadata);

#endif // STRIP_HEADER_H
