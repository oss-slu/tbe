#include "../../include/tbe.h"

// Exporter function implementation
int export_TBE(const TBEHeader* header, const char* filename) {
    if (!header) {
        fprintf(stderr, "Error: NULL header provided for export.\n");
        return -1;
    }

    FILE* file = fopen(filename, "w");
    if (!file) {
        perror("Error opening file for writing");
        return -1;
    }

    // Write BGN attributes
    const Attribute* attr = header->bgn_attributes;
    if (attr) {
        fprintf(file, "TBL,Global,Variable,Value\n");
        while (attr) {
            fprintf(file, "BGN,%s,%s\n", attr->name, attr->value);
            attr = attr->next;
        }
    }

    // Write TBL sections and their attributes
    const TBLSection* section = header->sections;
    while (section) {
        fprintf(file, "TBL,%s\n", section->name);
        const Attribute* section_attr = section->attributes;
        while (section_attr) {
            fprintf(file, "ATT,%s,%s\n", section_attr->name, section_attr->value);
            section_attr = section_attr->next;
        }
        section = section->next;
    }

    // Write EOT attributes
    attr = header->eot_attributes;
    if (attr) {
        while (attr) {
            fprintf(file, "EOT,%s,%s\n", attr->name, attr->value);
            attr = attr->next;
        }
    }

    fclose(file);
    return 0;
}
