# TBE File Processing Suite

A multi-language toolkit for handling TBE (Tabular Data with Metadata Blocks and Enrichment) files. This suite includes libraries 
in Python, C, Rust, R, JavaScript, and Java, designed for flexible use by both programmers and data analysts. Each language-specific
library allows you to parse, validate, manipulate, and export data from TBE files, facilitating cross-functional collaboration in 
data-driven projects.

## What is TBE?

TBE files are metadata-enriched tabular files that contain multiple structured "TBL" sections. Each section includes a unique 
name, column headers, and rows of data, with optional attributes and comments. TBE files use specific control markers (BGN, EOT) to 
define sections and organize data.
#### TBE Structure Overview
- **TBL:** A table-like data section with a unique name, column headers, and data rows.
- **ATT:** Optional attributes for TBL sections, represented as key-value pairs or lists.
- **CMT:** Comments associated with TBL sections.
- **Control Codes:** Specific codes within the first column indicate the start and end of sections (BGN, EOT).

## Tech Stack
- **JavaScript:** TBE Validator Tool – a JavaScript CLI tool to check structural and content compliance of TBE files.
- **Python:** TBE Library – a Python package enabling easy parsing, validation, and metadata aggregation of TBE files.
- **R:** TBE Library – an R package for statistical and tabular analysis of TBE files, ideal for research and analytics.
- **C:** TBE Library – a high-performance C library for file parsing, validation, and efficient data handling.
- **Java:** TBE Library – a Java package for enterprise applications to load, process, and validate TBE data.
- **Rust:** TBE Library – a Rust library optimized for fast parsing and validation of TBE files.

## Architecture
Each library is designed to meet the specific needs of its target environment while adhering to a common TBE file standard, enabling 
consistent cross-platform handling of TBE data.
