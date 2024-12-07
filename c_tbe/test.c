#include <stdio.h>
#include <stdlib.h>
#include "strip_header.h"

int main() {
    // Path to the sample TBE file
    const char *filename = "../sample_data/saq_bluesky_dku_20210715_20230131_inv_tbe.csv";

    // Call the strip_header function
    Metadata metadata = strip_header(filename);

    // Print the extracted metadata
    printf("Extracted Metadata:\n");
    for (size_t i = 0; i < metadata.count; i++) {
        printf("%s: %s\n", metadata.keys[i], metadata.values[i]);
    }

    // Free allocated memory
    free_metadata(&metadata);

    return 0;
}
