# IRWA Project — Part 1

This folder contains the notebook for preparing the fashion product collection, building two positional inverted indexes, and performing exploratory data analysis (EDA).

## Files and input data

| File | Purpose |
| --- | --- |
| [IRWA_part1.ipynb](IRWA_part1.ipynb) | Implementation, explanations, example lookup, tables, and plots. |
| [requirements-notebook.txt](requirements-notebook.txt) | Dependencies for running the notebook independently of the Flask application. |
| [../../data/fashion_products_dataset.json](../../data/fashion_products_dataset.json) | Input collection, currently containing 28,080 products. |

Place the supplied dataset at `data/fashion_products_dataset.json`, relative to the repository root. The notebook finds this path by checking its working directory and its parent directories, so it can be run from either the repository root or this folder. Original product identifiers (`pid`) and fields are preserved.

## Installation

Run the following commands **from the repository root**, using Python 3.8 or later. If you already have the project's `.venv`, activate it and skip its creation.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r project_progress/part_1/requirements-notebook.txt
python -m ipykernel install --user --name irwa-part1 --display-name "IRWA (.venv)"
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

The notebook downloads the NLTK English stopword list and `punkt_tab` tokenizer data if they are missing. Internet access is therefore required on the first run. `certifi` supplies the certificate bundle used for these downloads.

## Running the notebook

Open `IRWA_part1.ipynb` in a notebook editor, select the **IRWA (.venv)** kernel, then restart the kernel and run all cells in order. The cells share variables, so running them sequentially is necessary. The example query is `cotton`; change `search_query` to try another term.

If you want to use the Jupyter Notebook browser interface, install and launch it from the activated environment:

```bash
python -m pip install notebook
python -m notebook project_progress/part_1/IRWA_part1.ipynb
```

Alternatively, execute the entire notebook from the terminal and save the generated tables and figures directly into it:

```bash
python -m nbconvert --to notebook --execute \
  --ExecutePreprocessor.kernel_name=irwa-part1 \
  --ExecutePreprocessor.timeout=600 \
  --inplace project_progress/part_1/IRWA_part1.ipynb
```

Figures appear inline in the notebook. To export a standalone HTML copy after execution:

```bash
python -m nbconvert --to html project_progress/part_1/IRWA_part1.ipynb
```

## What the notebook implements

### Collection loading and preprocessing

Each JSON record becomes a `Product` object. A dictionary keyed by `pid` provides access to the original products.

`build_terms` applies the same processing to indexed text and example queries:

1. Lowercase the text and split joined words around `/`, `.`, `,`, and `-` when these characters are next to letters.
2. Normalize forms such as `t-shirt`, `t shirt`, and `tshirts` to `tshirt`.
3. Remove English stopwords, filter punctuation, and discard empty tokens. Numeric separators such as those in decimals and fractions can be retained.
4. Apply NLTK's Porter stemmer, caching repeated stemming operations.

`preprocess_details` selects descriptive product attributes, such as fabric, fit, color, sleeve, and material. It normalizes whitespace and case, splits comma-separated values, removes missing values and duplicates, and maps fit variants such as `slim fit` to `slim`. For `hooded`, `reversible`, and `stretchable`, an affirmative value becomes the attribute name. Numeric-only values and negative values are discarded.

### Two positional inverted indexes

| Index | Input used by the current implementation |
| --- | --- |
| `text_index` | Product title followed by description. |
| `detail_index` | Selected and normalized values from `product_details`. |

The separate indexes allow free-text descriptions and structured attributes to be retrieved independently. Each posting stores a product identifier and the term's positions in the processed token sequence:

```text
term -> [[pid, [position, ...]], ...]
```

Positions refer to the tokens after preprocessing. The current details index uses `product_details` only: `sub_category` is retained in the original product object, and `discount` is handled as numeric metadata. The code does not explicitly append either the subcategory or a `discount` marker to this index.

The example lookup displays matching product counts and sample postings for each processed query term in both indexes.

### Numeric metadata

Prices, discounts, and ratings are converted to finite numbers and stored separately in `numeric_fields_by_pid`; missing or invalid values become `None`. Original display values remain available in the `Product` objects.

The notebook prepares `quality_score = rating / 5`, using the collection's mean observed rating when a product's rating is missing. Stock availability is also retained for future use. These values prepare later retrieval work; the notebook's example lookup does not implement a ranking algorithm.

## Exploratory data analysis and outputs

The analysis produces text statistics, numeric summaries, stock counts and percentages, counts of products rated 5 or below 3, examples of the most expensive product and largest discount, and a brand rating table restricted to brands with at least 100 products.

Five figures are displayed:

| Figure | What it shows |
| --- | --- |
| Description length histogram | Variation in the amount of descriptive text per product. |
| Top 20 content words | The most frequent non-stopword terms in titles and descriptions. |
| Word cloud | A visual summary of frequent content words. |
| Rating, selling price, and discount histograms | Distributions of the main numeric product fields. |
| Top 10 brands and sellers | Product counts for the most represented brands and sellers. |

Text statistics use tokenized text before stemming; the word frequency plot and word cloud exclude English stopwords. Consequently, the EDA vocabulary and index vocabulary need not have the same size. The word cloud uses a fixed random seed for reproducibility.

The selling-price histogram displays values up to INR 5,000. Prices above this limit remain in the dataset and in the summary statistics. Rating statistics use observed ratings; the mean-rating substitution is used only for `quality_score`.

## Main libraries

- **NLTK:** English stopwords, sentence tokenization, and Porter stemming.
- **pandas and NumPy:** Data preparation, summaries, and histogram binning.
- **Matplotlib and WordCloud:** Inline figures and word cloud generation.
- **IPython, ipykernel, and nbconvert:** Notebook execution, rich table display, and export.
- **certifi:** Certificate bundle for resource downloads.

The Python standard library supplies JSON loading, path handling, dictionaries, counters, caching, and numeric validation.
