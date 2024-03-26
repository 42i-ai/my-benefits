# NLP and Data Extraction Challenge

This solution aims to solve the problem of data extraction from PDF files. We tested it using data extracted from readable PDF and OCR pfd. After extracting the data, we used Streamlit for data visualization. All the solutions employ containers as a way to deploy on production. To run the application locally you need to run the following command:

```bash
streamlit run my_benefits/app.py
```

- [x] Create a dashboard app to preset topic modeling (think of a better way to store data)
- [ ] Extract data from OCR pdf (This task is working. We can solve the dashboard for OCR in the same way as the previous step)
- [x] Add Duckdb to the extraction pipeline
- [ ] complete the containerizing the application
- [ ] Draw an architecture for the solution
- [ ] To architect how to add MLFlow to this solution to improve the PDF model extraction.

This solution can be used as a base to build a cost data lake with machine learning capabilities.

> [!TIP]
> If you have Markdown Preview Enhanced on Vs code, you can preview by (shift + command + v)

> [!TIP]
> Consider using VScode as the default Python editor. Consider installing Pylint to enforce the Python standards.
> Also the extensions: vscode-icons, Python Debugger, Python, Pylint, Pylance, Markdown Preview Enhanced, Docker, TODO Tree.
> Happy code!!! And have a nice cup of coffee.

This test aims to understand your way of thinking, coding, and problem-solving skills. There is no correct answer; follow your instincts and share with us the solutions to the challenges below:

> [!CAUTION]
> Do not feed any of these files into generative AI providers (ChatGPT, Bard, etc) or use any output from these models to solve this challenge

# 1. Data Extraction

Automated fundamental data extraction is beneficial for large organizations that deal with data on a large scale to generate meaningful information.

The first challenge is to extract information from all the PDF files found at /data/1
You can choose your preferred techniques or tools, but be aware that the data you've extracted may be necessary for the next challenge!

## Solution for data extract:

To tackle the challenge of data extraction, we will employ four storage layers:

- _Landing_: Place where the PDF files are landing from external sources.
- _Bronze_: Data with a low level of transformation(text extraction, table extraction)
- _Silver_: Pre-processed data extracted text tokenized and lemmatized.
- _Gold_: Documents after to extract meaningful information.

> [!NOTE]
> To run the code we should put the pdf files on the data folder inside my_benedits app folder.
> In our case we have the files on a bucket on s3 to got the files.
> To use this approach, rename the example.env to env and replace the variables.
> So just run the Python script [^13] as follows:

```bash
python my_benefits/get_files.py
```

We will approach the problem of information extraction in these stages:

**Step 1 - Extract PFD**

 Extract textual information from the PDF stored on **landing** directory. We will process the pdf using PyMuPDF[10] and store the data extracted on the raw directory,  raw database **raw** on the table **document_pages** using duckdb[^7]. To extract information from PDF for further analysis, we will use PyMuPDF[10]. According to the article on Medium [9], the Python package PyMuPDF is a good choice because it preserves tables and the original PDF structure.DuckDB aims to create a fast and efficient SQL query execution engine to run complex queries on large data sets. It integrates tightly with Pandas DataFrames and allows us to run these queries directly on top of them without needing to move data in and out of the dataframe[^7][^18].

**Step 2 - Pre-Processing**

Pre-process the extracted text for lemmatization, stop word removal and store it in the silver directory. We will employ Polars data frame to manipulate the extracted data to improve performance. Polars stands out as a high-performance alternative to Pandas, especially for large datasets, thanks to its foundation in Rust and its integration with Apache Arrow, which ensure speedy operations and efficient memory usage. The language-independent Arrow format reduces computational overhead by minimizing serialization/deserialization processes, further enhancing performance. Additionally, Polars' ability to utilize multi-core processing for complex queries significantly outpaces Pandas, which primarily operates on a single core. While Polars excels in data manipulation and performance, Pandas still maintains an edge in data exploration and integration with machine learning pipelines due to its extensive compatibility with Python's data ecosystem.​[^19]. For the lemmatization process, we will use SpaCy[^20] stands out in the NLP library landscape for its efficiency, speed, and object-oriented approach, making it a favored choice for developers and application builders over NLTK, which is often seen as more suitable for educational and research purposes. 

**Step 2 - Topic-Modeling**

We will employ topic modeling to solve this challenge, which is a statistical model used in the discovery of abstract topics that occur in a collection of documents, in this solution. Topics modeling can be fully unsupervised, although semi-supervised and supervised variants exist. Among the most commonly used techniques is latent Dirichlet Allocation (LDA)[^14][^15][^16].

Step 1: Load and Pre-process Data
Step 2: Cluster Data to Identify Groups
Step 3: Topic Modeling Generated Labels

> [!NOTE]
> In the production scenario for this solution, we can have two scenarios: Process the files soon,
> arrive at the landing folder, or schedule batch processing. We can use Airflow[^12] to schedule a job or a
> lambda function[^11] to trigger when a file arrives in the folder. Considering those scenarios, we created a container to test possible solutions using Kubernetes.


# 2 - Data Visualization

The second challenge is to display meaningful information from the extracted data (challenge 1)
You can choose your preferred techniques or tools, be aware that sometimes less is more, present meaningful insights, and show us what you have found interesting in those files! (i.e., topic modeling, word distributions, etc)

## Solution for visualization:



As a tool for visualization, we will use Streamlit[^17]. Streamlit is a powerful open-source Python library designed to effortlessly transform machine learning and data science projects into interactive web apps, ideal for sharing complex insights with non-technical audiences. Its standout feature is the rapid development cycle, allowing scripts to become fully functional web applications in mere hours, enhancing communication with decision-makers. Streamlit's pure Python approach obviates the need for web development expertise, streamlining the workflow for data scientists. Despite its simplicity, Streamlit efficiently handles user interactions through an immediate mode UI and smart caching, ensuring a smooth and responsive user experience. This blend of ease of use, quick development, and no requirement for additional web technology skills makes Streamlit a highly accessible tool for sharing data-driven insights. To run the Stremlit app from the project folder, exectue the following code:


# 3 - Data Extraction OCR

The Third, as last challenge, is: extract, process, and infer text images, using the 2 PDF files available at data/2
You can choose your preferred techniques or tools, extract the most text you can and apply one of the analysis techniques you'd applied on challenge 2.

## Solution for OCR extraction

pdf2image is a Python library used for converting PDF files into images, making it easier to work with the visual content of PDF documents in Python applications. It relies on **Poppler**, a PDF rendering library, to execute the conversion. Poppler must be installed on your system for pdf2image to function, as it's not a Python package but rather a separate utility that **pdf2image** calls behind the scenes. This setup is commonly used in projects where PDF content needs to be displayed or processed as images. For installation and usage, refer to the respective documentation of each tool. Also we to use the **Tesseract-ocr** an optical character recognition (OCR) tool the library the python package Python-tesseract is a wrapper for google library.

> [!CAUTION]
> The ocr solution depends of Poppler [^21] and  Tesseract-ocr[^22]. To install on the mac os both use:

```bash
brew install poppler
```
```bash
brew install tesseract
```
We will containerizing an application with dependencies like pdf2image, Poppler, and Tesseract-OCR . For to encapsulate the environment, ensuring that all the necessary tools are available on the specific version. This approach facilitates easier deployment across different systems without compatibility issues.

# Architecture

# Enviroment:

We use Poetry[2] to manage Python dependencies for the environment solution. The solution will be packaged in a docker-compose file, which can be used to deploy it to production and execute tests on the CD/CI process.

```bash
docker build -t nlp-challenge -f my_benefits/extract/Dockerfile --no-cache --progress=plain . 2>&1 | tee build.log
```

The following command runs the container.

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
[^17]: [Stremlit](https://docs.streamlit.io/)
[^18]: [Birds versus Bear: Comparing DuckDB and Polars ](https://www.linkedin.com/pulse/bird-versus-bear-comparing-duckdb-polars-jorrit-sandbrink-xdfoe/)
[^19]: [Polars vs. pandas: What's the Difference?](https://blog.jetbrains.com/dataspell/2023/08/polars-vs-pandas-what-s-the-difference/)
[^20]: [Spacy](https://spacy.io/)
[^21]: [Poppler](https://poppler.freedesktop.org/)
[^22]: [Tesseract](https://tesseract-ocr.github.io/)

