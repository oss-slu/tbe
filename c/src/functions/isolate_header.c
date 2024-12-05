#include "../../include/tbe.h"
#include <ctype.h>
#include <string.h>

// Function prototypes
static void add_attribute(Attribute** head, const char* name, const char* value);
static void trim_newline(char* str);
static void strip_quotes(char* str);
static int split_csv_line(const char* line, char* tokens[], int max_tokens);

// Helper function to strip surrounding quotes from a string
static void strip_quotes(char* str) {
    size_t len = strlen(str);
    if (len >= 2 && str[0] == '"' && str[len - 1] == '"') {
        // Shift the string left by one and null-terminate before the last quote
        memmove(str, str + 1, len - 2);
        str[len - 2] = '\0';
    }
}

// Helper function to add an attribute to a linked list
static void add_attribute(Attribute** head, const char* name, const char* value) {
    Attribute* new_attr = malloc(sizeof(Attribute));
    if (!new_attr) {
        perror("Memory allocation failed for Attribute");
        exit(EXIT_FAILURE);
    }
    strncpy(new_attr->name, name, MAX_NAME_LEN - 1);
    new_attr->name[MAX_NAME_LEN - 1] = '\0';
    strncpy(new_attr->value, value, MAX_VALUE_LEN - 1);
    new_attr->value[MAX_VALUE_LEN - 1] = '\0';

    // Strip surrounding quotes if present
    strip_quotes(new_attr->name);
    strip_quotes(new_attr->value);

    new_attr->next = NULL;

    if (!*head) {
        *head = new_attr;
    }
    else {
        Attribute* current = *head;
        while (current->next) current = current->next;
        current->next = new_attr;
    }
}

// Helper function to trim newline and carriage return characters
static void trim_newline(char* str) {
    size_t len = strlen(str);
    while (len > 0 && (str[len - 1] == '\n' || str[len - 1] == '\r')) {
        str[len - 1] = '\0';
        len--;
    }
}

// Function to split a CSV line into tokens, handling quoted fields
static int split_csv_line(const char* line, char* tokens[], int max_tokens) {
    int token_count = 0;
    bool in_quotes = false;
    const char* start = line;
    const char* ptr = line;
    size_t len = strlen(line);

    while (*ptr && token_count < max_tokens) {
        if (*ptr == '"') {
            in_quotes = !in_quotes;
        }
        else if (*ptr == ',' && !in_quotes) {
            size_t field_len = ptr - start;
            // Allocate memory for the token
            char* token = malloc(field_len + 1);
            if (!token) {
                perror("Memory allocation failed for token");
                exit(EXIT_FAILURE);
            }
            strncpy(token, start, field_len);
            token[field_len] = '\0';
            tokens[token_count++] = token;
            start = ptr + 1;
        }
        ptr++;
    }

    // Add the last token
    if (token_count < max_tokens) {
        size_t field_len = ptr - start;
        char* token = malloc(field_len + 1);
        if (!token) {
            perror("Memory allocation failed for token");
            exit(EXIT_FAILURE);
        }
        strncpy(token, start, field_len);
        token[field_len] = '\0';
        tokens[token_count++] = token;
    }

    return token_count;
}

// Parser function implementation
TBEHeader* parse_TBE_header(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("Error opening TBE file");
        return NULL;
    }

    TBEHeader* header = malloc(sizeof(TBEHeader));
    if (!header) {
        perror("Memory allocation failed for TBEHeader");
        fclose(file);
        return NULL;
    }
    header->bgn_attributes = NULL;
    header->eot_attributes = NULL;
    header->sections = NULL;
    TBLSection* current_section = NULL;

    char line[4096]; // Increased buffer size for longer lines
    int line_number = 0;
    bool in_bgn_section = false;
    bool in_eot_section = false;

    while (fgets(line, sizeof(line), file)) {
        line_number++;
        // Remove newline characters
        trim_newline(line);

        // Check if the line is empty or contains only delimiters
        bool is_empty_or_delimiter = true;
        for (size_t i = 0; i < strlen(line); i++) {
            if (line[i] != ',' && !isspace((unsigned char)line[i])) {
                is_empty_or_delimiter = false;
                break;
            }
        }
        if (is_empty_or_delimiter) continue;   // Silently skip empty or delimiter-only lines

        // Split the line into tokens
        char* tokens[100]; // Increased token limit
        int token_count = split_csv_line(line, tokens, 100);

        if (token_count == 0) {
            // Completely empty line
            continue;
        }

        // Handle section headers
        if (token_count >= 1 && strncmp(tokens[0], "BGN", 3) == 0) {
            in_bgn_section = true;
            in_eot_section = false;
            if (token_count >= 3) {
                add_attribute(&header->bgn_attributes, tokens[1], tokens[2]);
            }
            else if (token_count == 2) {
                add_attribute(&header->bgn_attributes, tokens[1], "");
            }
            else {
                fprintf(stderr, "Warning [Line %d]: BGN line missing key or value.\n", line_number);
            }
            // Free allocated tokens
            for (int i = 0; i < token_count; i++) free(tokens[i]);
            continue;
        }

        if (token_count >= 1 && strncmp(tokens[0], "EOT", 3) == 0) {
            in_eot_section = true;
            in_bgn_section = false;
            if (token_count >= 3) {
                add_attribute(&header->eot_attributes, tokens[1], tokens[2]);
            }
            else if (token_count == 2) {
                add_attribute(&header->eot_attributes, tokens[1], "");
            }
            else {
                fprintf(stderr, "Warning [Line %d]: EOT line missing key or value.\n", line_number);
            }
            // Free allocated tokens
            for (int i = 0; i < token_count; i++) free(tokens[i]);
            continue;
        }

        // Handle TBL sections
        if (token_count >= 1 && strncmp(tokens[0], "TBL", 3) == 0) {
            // Reset section flags
            in_bgn_section = false;
            in_eot_section = false;

            if (token_count >= 2) {
                TBLSection* new_section = malloc(sizeof(TBLSection));
                if (!new_section) {
                    perror("Memory allocation failed for TBLSection");
                    fclose(file);
                    free_tbe_header(header);
                    // Free allocated tokens
                    for (int i = 0; i < token_count; i++) free(tokens[i]);
                    return NULL;
                }
                strncpy(new_section->name, tokens[1], MAX_NAME_LEN - 1);
                new_section->name[MAX_NAME_LEN - 1] = '\0';
                new_section->attributes = NULL;
                new_section->next = NULL;

                if (!header->sections) {
                    header->sections = new_section;
                }
                else {
                    TBLSection* last_section = header->sections;
                    while (last_section->next) last_section = last_section->next;
                    last_section->next = new_section;
                }
                current_section = new_section;
            }
            else {
                fprintf(stderr, "Warning [Line %d]: TBL section missing name.\n", line_number);
            }
            // Free allocated tokens
            for (int i = 0; i < token_count; i++) free(tokens[i]);
            continue;
        }

        // Handle ATT lines
        if (token_count >= 1 && strncmp(tokens[0], "ATT", 3) == 0) {
            if (!current_section) {
                fprintf(stderr, "Warning [Line %d]: ATT line encountered without an active TBL section.\n", line_number);
                // Free allocated tokens
                for (int i = 0; i < token_count; i++) free(tokens[i]);
                continue;
            }
            for (int i = 1; i < token_count; i++) {
                if (strlen(tokens[i]) == 0) {
                    fprintf(stderr, "Warning [Line %d]: Empty attribute name in ATT line.\n", line_number);
                    continue;
                }
                // Check if there's a corresponding value
                char* value = "";
                if (i + 1 < token_count && strlen(tokens[i + 1]) > 0) {
                    value = tokens[i + 1];
                    i++; // Skip the value in the next token
                }
                add_attribute(&current_section->attributes, tokens[i], value);
            }
            // Free allocated tokens
            for (int i = 0; i < token_count; i++) free(tokens[i]);
            continue;
        }

        // Handle continuation lines for BGN and EOT
        if (in_bgn_section || in_eot_section) {
            if (token_count >= 3 && strlen(tokens[1]) > 0) {
                Attribute** attr_list = in_bgn_section ? &header->bgn_attributes : &header->eot_attributes;
                add_attribute(attr_list, tokens[1], tokens[2]);
            }
            else if (token_count >= 2 && strlen(tokens[1]) > 0) {
                Attribute** attr_list = in_bgn_section ? &header->bgn_attributes : &header->eot_attributes;
                add_attribute(attr_list, tokens[1], "");
            }
            // Silently skip lines that don't have enough tokens
            // Free allocated tokens
            for (int i = 0; i < token_count; i++) free(tokens[i]);
            continue;
        }

        // Handle data lines or unknown lines
        fprintf(stderr, "Warning [Line %d]: Unknown line type '%s' encountered. Skipping.\n", line_number, tokens[0]);
        // Free allocated tokens
        for (int i = 0; i < token_count; i++) free(tokens[i]);
    }

    fclose(file);
    return header;
}

// Function to free allocated memory
void free_tbe_header(TBEHeader* header) {
    if (!header) return;

    // Free BGN attributes
    Attribute* attr = header->bgn_attributes;
    while (attr) {
        Attribute* next_attr = attr->next;
        free(attr);
        attr = next_attr;
    }

    // Free EOT attributes
    attr = header->eot_attributes;
    while (attr) {
        Attribute* next_attr = attr->next;
        free(attr);
        attr = next_attr;
    }

    // Free TBL sections and their attributes
    TBLSection* section = header->sections;
    while (section) {
        Attribute* section_attr = section->attributes;
        while (section_attr) {
            Attribute* next_attr = section_attr->next;
            free(section_attr);
            section_attr = next_attr;
        }
        TBLSection* next_section = section->next;
        free(section);
        section = next_section;
    }

    free(header);
}

// Function to print the TBE header for debugging
void print_tbe_header(const TBEHeader* header) {
    if (!header) {
        printf("No header to display.\n");
        return;
    }

    printf("=== Global Metadata (BGN) ===\n");
    const Attribute* attr = header->bgn_attributes;
    while (attr) {
        if (strlen(attr->value) > 0) {
            printf("  %s: %s\n", attr->name, attr->value);
        }
        else {
            printf("  %s: \n", attr->name);
        }
        attr = attr->next;
    }
    printf("\n");

    printf("=== Global Metadata (EOT) ===\n");
    attr = header->eot_attributes;
    while (attr) {
        if (strlen(attr->value) > 0) {
            printf("  %s: %s\n", attr->name, attr->value);
        }
        else {
            printf("  %s: \n", attr->name);
        }
        attr = attr->next;
    }
    printf("\n");

    const TBLSection* section = header->sections;
    while (section) {
        printf("TBL Section: %s\n", section->name);
        const Attribute* section_attr = section->attributes;
        while (section_attr) {
            printf("  Attribute: %s = %s\n", section_attr->name, section_attr->value);
            section_attr = section_attr->next;
        }
        section = section->next;
        printf("\n");
    }
}
