# NLP and Data Extraction Challenge

> [!TIP]
> If you have Markdown Preview Enhanced on Vs code you can preview by (shift + command + v)

> [!TIP]
> Consider to use VScode as default python editor. Consider to install Pylint to enforce the python standards.
> Also the following extensions: vscode-icons, Python Debugger, Python, Pylint, Pylance,Markdown Preview Enhanced, Docker, TODO Tree.
> Happy code!!! and have a nice cup of coffe.

The idea of this test is to understand your way of thinking, coding, and problem-solving skills. There is no right answer, just follow your instincts and share with us the solutions of the challenges below:

> [!CAUTION]
> Do not feed any of these files into generative AI providers (ChatGPT, Bard, etc) or use any output from these models to solve this challenge

1. Data Extraction

Automated fundamental data extraction is very useful for large organizations who deal with data on a large scale to generate meaningful information.

The first challenge is: extract information from all the PDF files found at /data/1
You can choose your preferred techniques or tools, but be aware that the data you'd extracted may be necessary for the next challenge!

# Solution for extract:

For the extraction solution the pipeline will create a raw area where it will save the raw text extract from the file. This approch is usefull if we need to reprocess the data without reprocess the pdf files again. In a solution the pdf files can be storage on a landing area. On the second step of the pipeline will transform the data on tables pre-processing the data. On the last step we will have the analitycs table can be used for datascience purpose.

1 - Read the pdf data and write the extracted data on raw directory in txt format with the same name of the pdf file.
2 - Clean the data removing spaces, text breaking and lower case the text[^8].
3 - Write cleaned data on duckdb table[^7].

# Enviroment:

For the enviroment solution we use Poetry[^2] for manage python depencencies. The solution will be packet on a docker compose file whish can be used for deploy on production and execute test on CD/CI process.

- [x] docker with streamlit
- [x] generate raw data
- [ ] create silver layer with transformed data and duckdb
- [ ] create jupyter notebook to analyze and create the gold layer
- [ ] create a dashboard connecting streamlit and duckdb
- [ ] create a pipeline using airflow to automatize the process
- [ ] add to the pipeline functionality for read ocr pdf
- [ ] create a mlflow for all the process

## Libraires used on this project:

### PDFtoText

For to extract information from PDF for further analysis we will to use PDFtoText. According with the article on Medium [^9] the python package PyMuPDF[^10] is a good choice because it preserves tables and original pdf structure.

### Duckdb

DuckDB aims to bring together fast & efficient SQL query execution engine that can run complex queries on large sets of data. It integrates tightly with Pandas DataFrames and allows us to run these queries directly on top of them without needing to take data in and out of the dataframe[^7].

- Mypds
- streamlit[^1]

For extract text from PDF I will use pypdf2 and write the data as json.

```bash
docker build -t nlp-challenge -f my_benefits/extract/Dockerfile --no-cache --progress=plain . 2>&1 | tee build.log
```

The following command runs the container

```bash
docker run -p 8501:8501 nlp-challenge
```

### References

[^1]: [Build a stremlit image](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)
[^2]: [Poetry site](https://python-poetry.org/)
[^3]: [Build a pipeline using duckdb](https://www.youtube.com/watch?v=eXXImkz-vMs)
[^4]: [Extract text from pdf tutorial](https://www.youtube.com/watch?v=RULkvM7AdzY)
[^5]: [Natural Language Processing with Python](https://www.udemy.com/course/nlp-natural-language-processing-with-python/learn/lecture/12744493#overview)5
[^6]: [Thoughtful Machine Learning](https://www.amazon.com/Thoughtful-Machine-Learning-Test-Driven-Approach/dp/1449374069)
[^7]: [Supercharge your data processing with DuckDB](https://medium.com/learning-sql/supercharge-your-data-processing-with-duckdb-cea907196704)
[^8]: [Extracting-information-from-pdf-file-using-OCR-and-NLP](https://github.com/archowdhury/Extracting-information-from-PDF-files-using-OCR-and-NLP/blob/master/PDF%20Extractor.ipynb)
[^9]: [Python Packages for PDF Data Extraction](https://medium.com/analytics-vidhya/python-packages-for-pdf-data-extraction-d14ec30f0ad0)
[^10]: [https://pymupdf.readthedocs.io/en/latest/](https://pymupdf.readthedocs.io/en/latest/)

Maybe I can use

https://github.com/PBPatil/Keyword-Extracter/tree/master
https://dashboard.render.com/
https://docs.github.com/pt/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

Talvez possa utilizar para melhorar os metodos

https://learning.oreilly.com/library/view/real-world-natural-language/9781617296420/
https://learning.oreilly.com/library/view/python-natural-language/9781838987312/
https://learning.oreilly.com/library/view/practical-natural-language/9781492054047/

Tutoriais

https://www.kaggle.com/code/jpandeinge/nlp-analysis-of-pdf-documents
https://ydv-poonam.medium.com/how-to-extract-text-from-a-pdf-nlp-b6409422cfd2
https://blog.developer.adobe.com/natural-language-processing-adobe-pdf-extract-and-deep-pdf-intelligence-31ae07139b66

Name Entity

https://blog.knowledgator.com/extract-any-named-entities-from-pdf-using-custom-spacy-pipeline-9fd0af2c3e13

PyMuPDF

https://neurondai.medium.com/how-to-extract-text-from-a-pdf-using-pymupdf-and-python-caa8487cf9d

TDD DataScience
https://medium.com/doctolib/yes-test-driven-development-is-useful-in-data-science-857f38208349
https://towardsdatascience.com/tdd-datascience-689c98492fcc

Tabula can be used to extrac tables
https://www.youtube.com/watch?v=w2r2Bg42UPY

Read image from pdf

https://www.youtube.com/watch?v=oyqNdcbKhew

Entity Recognition

https://www.youtube.com/watch?v=tMLEPtwFklQ

Antes do Minio

https://www.youtube.com/watch?v=X76h_QPMww0

Minio data lake

https://www.youtube.com/watch?v=5kx5SLlrTH0&t=377s

Extracting and processing table data from PDFs can be quite complex, especially when categorizing and grouping similar elements from multiple tables. Here are the general steps you could follow, along with some Python libraries that might be useful:

### 1. PDF Parsing:

First, you need to extract tables from the PDF files. Libraries like `Tabula` and `PyPDF2` can be useful here.

- **Tabula**: This is a popular library for extracting table data from PDFs. It works well with PDFs that contain well-defined tables.
- **PyPDF2**: Useful for more general PDF parsing, including text extraction. It might be necessary if you also need to extract contextual information around tables.

### 2. Data Extraction:

Once you have the raw table data, you'll need to clean and preprocess it to ensure it's in a usable format.

- **Pandas**: After extracting tables, you can load this data into Pandas DataFrames for easier manipulation and analysis.
- **Openpyxl** or **xlrd**: If your tables are exported to Excel format, these libraries can help read and write .xlsx and .xls files, respectively.

### 3. Data Cleaning:

Clean your data to ensure consistency, especially if tables vary in structure or formatting.

- **Regular Expressions (re)**: Useful for cleaning text data, such as removing unwanted characters or standardizing text formats.
- **Pandas**: Offers numerous functions for data cleaning, including handling missing values, renaming columns, and changing data types.

### 4. Categorization and Similarity Detection:

To categorize and find similar elements, consider the nature of your data. Are you comparing text, numbers, or mixed data?

- **Natural Language Processing (NLP)**: For text data, NLP techniques can help. Libraries like `NLTK` or `spaCy` can assist in text processing, feature extraction, and similarity detection.
- **Scikit-learn**: Provides numerous algorithms for clustering and classification, which can help group similar elements. Techniques like TF-IDF (for text data), K-Means clustering, or hierarchical clustering might be useful.

### 5. Grouping Similar Elements:

Once you have identified similar elements, you can group them using Pandas functionality or custom algorithms.

- **Pandas**: Use grouping and aggregation functions like `groupby()` to collect similar elements into new tables.
- **Custom Algorithms**: Depending on your similarity criteria, you might need to implement custom logic to group elements effectively.

### 6. Output:

Finally, you might want to export your grouped tables into a format that's easy to use or analyze further.

- **Pandas**: Can export DataFrames to various formats, including CSV, Excel, JSON, or even back to PDF.

### Example Workflow in Python:

```python
import tabula
import pandas as pd

# Step 1: Extract tables from PDF
tables = tabula.read_pdf("your_file.pdf", pages='all')

# Step 2-3: Process and clean data
for table in tables:
    # Perform cleaning operations like removing unwanted rows/columns, standardizing text, etc.
    pass

# Step 4-5: Categorize and group similar elements
# This could involve NLP processing, similarity scoring, clustering, etc.
# Then, use Pandas or custom logic to group similar items.

# Step 6: Export grouped tables
grouped_table.to_csv("grouped_data.csv")
```

This workflow is quite high-level. Each step might require significant detail, especially the categorization and grouping of similar elements, which could involve complex logic depending on your specific needs. If you have a particular part of the process you'd like to dive deeper into, let me know!
