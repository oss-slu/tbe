#include "../include/tbe.h"

int main() {
    const char* input_path = "sample_data/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv";
    const char* output_path = "c/output_data/output_TBE.csv";

    TBEHeader* header = parse_TBE_header(input_path);
    if (!header) {
        fprintf(stderr, "Failed to parse TBE header\n");
        return EXIT_FAILURE;
    }

    printf("Parsed TBE Header:\n");
    print_tbe_header(header);

    if (export_TBE(header, output_path) != 0) {
        fprintf(stderr, "Failed to export TBE data\n");
        free_tbe_header(header);
        return EXIT_FAILURE;
    }

    printf("Exported TBE data to %s\n", output_path);

    // Free allocated memory
    free_tbe_header(header);

    return EXIT_SUCCESS;
}
