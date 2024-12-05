#ifndef TBE_H
#define TBE_H

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX_NAME_LEN 256
#define MAX_VALUE_LEN 256

typedef struct Attribute {
    char name[MAX_NAME_LEN];
    char value[MAX_VALUE_LEN];
    struct Attribute* next;
} Attribute;

typedef struct TBLSection {
    char name[MAX_NAME_LEN];
    Attribute* attributes;
    struct TBLSection* next;
} TBLSection;

typedef struct TBEHeader {
    Attribute* bgn_attributes;
    Attribute* eot_attributes;
    TBLSection* sections;
} TBEHeader;

// Parser function
TBEHeader* parse_TBE_header(const char* filename);

// Exporter function
int export_TBE(const TBEHeader* header, const char* filename);

// Free memory function
void free_tbe_header(TBEHeader* header);

// Print function for debugging
void print_tbe_header(const TBEHeader* header);

#endif
