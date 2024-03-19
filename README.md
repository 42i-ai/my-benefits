# NLP and Data Extraction Challenge

> [!TIP]
> If you have Markdown Preview Enhanced on Vs code you can preview by (shift + command + v)

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
