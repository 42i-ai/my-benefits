# NLP and Data Extraction Challenge

This solution aims to solve the problem of data extraction from PDF files. We tested it using data extracted from readable PDF and OCR pfd. After extracting the data, we used Streamlit for data visualization. All the solutions employ containers as a way to deploy on production.

- [ ] Create a dashboard app to preset topic modeling (think of a better way to store data)
- [ ] Extract data from OCR pdf (This task is working. We can solve the dashboard for OCR in the same way as previous step)
- [ ] Add Duckdb to the extraction pipeline
- [ ] To container app
- [ ] Draw an architecture to the solution

> [!TIP]
> If you have Markdown Preview Enhanced on Vs code, you can preview by (shift + command + v)

> [!TIP]
> Consider using VScode as the default Python editor. Consider installing Pylint to enforce the Python standards.
> Also the extensions: vscode-icons, Python Debugger, Python, Pylint, Pylance, Markdown Preview Enhanced, Docker, TODO Tree.
> Happy code!!! And have a nice cup of coffee.

This test aims to understand your way of thinking, coding, and problem-solving skills. There is no correct answer; just follow your instincts and share with us the solutions to the challenges below:

> [!CAUTION]
> Do not feed any of these files into generative AI providers (ChatGPT, Bard, etc) or use any output from these models to solve this challenge

1. Data Extraction

Automated fundamental data extraction is beneficial for large organizations that deal with data on a large scale to generate meaningful information.

The first challenge is: to extract information from all the PDF files found at /data/1
You can choose your preferred techniques or tools, but be aware that the data you've extracted may be necessary for the next challenge!

# Solution for data extract:

To tackle the challenge of data extraction, we will employ four storage layers:

- _Landing_: Place where the PDF files are landing from external sources.
- _Bronze_: Data with a low level of transformation(text extraction, table extraction)
- _Silver_: Pre-processed data extracted text tokenized and lemmatized.
- _Gold_: Documents after to extract meaningful information.

> [!NOTE]
> To run the code we should put the pdf files on the data folder inside my_benedits app folder.
> In our case we have the files on a bucket on s3 to got the files.
> To use this approach rename the example.env to env and replace the variables.
> So just run the python script [^13] as follows:

```bash
python my_benefits/get_files.py
```

We will approach the problem of information extraction in these stages:

Step 1 - Extract textual information from PDF and store it inside the raw directory in a folder named after the PDF file name. The file will be named pfd-file-name-text-extracted.txt.
Step 2- Extract tables from the PDF and store them in the same folder as the previous step.
Step 3 - Pre-process the extracted text for lemmatization, stop word removal, and store it in the raw folder.

> [!NOTE]
> In the production scenario for this solution, we can have two scenarios: Process the files soon,
> arrive at the landing folder, or schedule batch processing. We can use Airflow[^12] to schedule a job or a
> lambda function[^11] to trigger when a file arrives in the folder. Considering those scenarios, we created a container to test possible solutions using Kubernetes.

2 - Data Visualization

The second challenge is: display meaningful information from the extracted data (challenge 1)
You can choose your preferred techniques or tools, be aware that sometimes less is more, present meaningful insights, and show us what you have found interesting on those files! (i.e: topic modeling, word distributions, etc)

# Solution for data extract:

Step 1: Load and Pre-process Data
Step 2: Cluster Data to Identify Groups
Step 3: AI Generated Labels

# Architecture

# Enviroment:

For the environment solution, we use Poetry[2] to manage Python dependencies. The solution will be packaged in a docker compose file, which can be used to deploy it to production and execute tests on the CD/CI process.

## Libraries used on this project:

### PDFtoText

To extract information from PDF for further analysis, we will use PDFtoText. According to the article on Medium [9], the Python package PyMuPDF[10] is a good choice because it preserves tables and the original PDF structure. However, after testing with PyMuPDF, the library does not extract tables correctly, so I used tabular.

### Duckdb

DuckDB aims to create a fast and efficient SQL query execution engine that can run complex queries on large data sets. It integrates tightly with Pandas DataFrames and allows us to run these queries directly on top of them without needing to move data in and out of the dataframe[7].

- Mypds
- streamlit[^1]

I will use pypdf2 to extract text from the PDF and write the data as json.

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
[^8]: [Extracting information from pdf file using OCR and NLP](https://github.com/archowdhury/Extracting-information-from-PDF-files-using-OCR-and-NLP/blob/master/PDF%20Extractor.ipynb)
[^9]: [Python Packages for PDF Data Extraction](https://medium.com/analytics-vidhya/python-packages-for-pdf-data-extraction-d14ec30f0ad0)
[^10]: [PyMupdf](https://pymupdf.readthedocs.io/en/latest/)
[^11]: [AWS Lambda Function — Watermarking a PDF via S3 Trigger in Python](https://supremecodr.medium.com/aws-lambda-function-watermarking-a-pdf-via-s3-trigger-in-python-5080b1afb72)
[^12]: [How to build a data extraction pipeline with Apache Airflow](https://towardsdatascience.com/how-to-build-a-data-extraction-pipeline-with-apache-airflow-fa83cb8dbcdf)
[^13]: [Downloading Multiple Files from DigitalOcean Spaces with Python](https://medium.com/@rahmanazhar/downloading-multiple-files-from-digitalocean-spaces-with-python-1531e3174347)
[^14]: [Document Topic Extraction with Large Language Models (LLM) and the Latent Dirichlet Allocation (LDA) Algorithm](https://towardsdatascience.com/document-topic-extraction-with-large-language-models-llm-and-the-latent-dirichlet-allocation-e4697e4dae87)
[^15]: [Topic Modeling and Semantic Clustering with spaCy](https://fouadroumieh.medium.com/topic-modeling-and-semantic-clustering-with-spacy-960dd4ac3c9a)
[^16]: [Transforming Data Science: Building a Topic Modelling App with Cohere and Databutton](https://medium.com/databutton/transforming-data-science-building-a-topic-modeling-app-with-cohere-and-databutton-aab5d37e94fa)
