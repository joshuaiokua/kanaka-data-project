# Project Data

## Local Databases

A portion of the data that I have already preprocessed into SQL-compatible formats is stored in a local SQLite database. The file `kanaka_subset_base.db` is a direct mirror of the dataset initially stored in CockroachDB. This local database is strictly for testing and development purposes and is not intended for production use. As I experiment with optimal data structuring and naming conventions for effective interaction with LLM architecture, new versions of this local database subset will be created.

`kanaka_subset_base.db` includes the following datasets from the Office of Hawaiian Affairs' [Native Hawaiian Data Book 2023](https://ohadatabook.com/DB2023.html).

- Population Estimates of the Hawaiian Islands: 1778‑1896
- Population of the Territory and State of Hawaii: US Census 1900-2020
- Native Hawaiian Population by States: US Census 2020
- Native Hawaiian Grandparents Living with Own Grandchildren: State of Hawaii 2010-2022
- Native Hawaiian Household Income by Selected Characteristics in the US and Hawaii: 2010-2022
- Native Hawaiian Families Below Poverty Level in the US and Hawaii: 2010-2022
- Employment of Civilian Native Hawaiians by Industry in the US and Hawaii: 2010‑2022
- Employment of Civilian Native Hawaiians by Occupation in the US and Hawaii: 2010‑2022
- Native Hawaiian School Enrollment in the State of Hawaii: 2010-2022
- Native Hawaiian Educational Attainment: State of Hawaii 2010-2022

## Data Sources

The project utilizes data in three stages: unprocessed, preprocessed, and processed, as defined below:

- **Unprocessed**: Raw data as originally sourced.
- **Preprocessed**: Data that has been cleaned and transformed but may require additional processing.
- **Processed**: Fully cleaned data, ready for use in models or visualizations.

> **Note (9/24):** At present, the focus has shifted to building LLM interactivity using a cleaned subset of the data. The data cleaning process will resume once LLM functionality is more fully developed.

### Data Cleaning Progress

#### Native Hawaiian Data Book 2023 [[source]](https://ohadatabook.com/DB2023.html)

- **Unprocessed**
  - [Chapter 2: Housing](https://ohadatabook.com/go_chap02.23.html)
  - [Chapter 3: Labor and Employment](https://ohadatabook.com/go_chap03.23.html)
  - [Chapter 4: Income](https://ohadatabook.com/go_chap04.23.html)
  - [Chapter 5: Land, Water, and Air](https://ohadatabook.com/go_chap05.23.html)
  - [Chapter 6: Education](https://ohadatabook.com/go_chap06.23.html)
  - [Chapter 7: Health and Vital Statistics](https://ohadatabook.com/go_chap07.23.html)
  - [Chapter 8: Human Services](https://ohadatabook.com/go_chap08.23.html)
  - [Chapter 9: Crime](https://ohadatabook.com/go_chap09.23.html)
  - [Chapter 10: Legacy Data](https://ohadatabook.com/go_chap10.23.html)[^1]
- **Preprocessed**
  - [Chapter 1: Population](https://ohadatabook.com/go_chap01.23.html) | ~5% complete
- **Processed**
  - None

[^1]: Legacy data may not be included in the final data set, depending on the relevance and potential redundancy of said legacy data.
