# File System Search Engine

A pure Python implementation of an in-memory search engine for text files in a directory. This tool recursively crawls through a directory, indexes text files, and provides a powerful query interface for searching through their contents.

## Features

- Fast in-memory search
- Recursive directory scanning
- Support for multiple text file formats (.txt, .md, .py, .java, .cpp, .c, .h, .js, .html, .css) (only .txt tested)
- Advanced query syntax with required and optional terms
- OR group support with multi-match ranking
- Smart result ranking based on both optional terms and OR group matches

## Installation

No external dependencies required! Just clone the repository and make sure the main script is executable:

```bash
chmod +x src/search.py
```

## Usage

1. Start the search engine by providing a directory to index:
```bash
./src/search.py --dir <directory_path>
```

2. Once started, enter queries at the prompt. The query syntax supports:
   - Regular words (optional matches)
   - Required words (prefix with +)
   - OR groups (+(word1 word2))

### Query Syntax

- `word` - Optional word (improves ranking if found)
- `+word` - Required word (must be present)
- `+(word1 word2)` - Required OR group (either word1 OR word2 must be present)

### Examples

```
> biz +foo +bar +(bat baz) bop
```
This query will:
- Require "foo" AND "bar"
- Require either "bat" OR "baz" (matching both improves ranking)
- Optionally match "biz" and "bop" (affects ranking)

Results are displayed as:
```
/path/to/file.txt line_number "matching line content"
```

### Result Ranking

Results are sorted in descending order based on:
1. Number of optional terms matched (primary sort key)
2. Number of terms matched within OR groups (secondary sort key)

For example, given the query `biz +foo +bar +(bat baz) bop`:
1. Lines with both optional terms ("biz" and "bop") and both OR terms ("bat" and "baz")
2. Lines with both optional terms but only one OR term
3. Lines with one optional term and both OR terms
4. Lines with one optional term and one OR term
5. Lines with no optional terms but both OR terms
6. Lines with no optional terms and one OR term

Running the query `biz +foo +bar +(bat baz) bop` on the test_folder directory will return the following results:

| File | Line | Content |
|------|------|---------|
| tests/test_folder/test1.txt | 2 | `1: biz foo bar bat baz bop biz` |
| tests/test_folder/test1.txt | 1 | `2: biz foo bar bat baz bop` |
| tests/test.txt | 1 | `3: foo bar bat baz bop` |
| tests/sample1.txt | 1 | `4: foo bar bat baz` |
| tests/test_folder/test1.txt | 4 | `5: foo bar bat` |
| tests/test.txt | 2 | `5: foo bar baz` |

## Implementation Details

The search engine:
1. Builds an inverted index mapping words to their locations
2. Processes queries using set operations for efficient matching
3. Ranks results using a two-level sorting system:
   - Primary: Count of optional term matches
   - Secondary: Count of OR group term matches
4. Uses only Python standard library (no external dependencies)

## Limitations

- Works entirely in memory (not suitable for very large directories)
- Basic tokenization (splits on whitespace and removes non-alphanumeric characters)
- Case-insensitive matching only 