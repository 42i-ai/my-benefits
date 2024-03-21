O que tenho que entregar hoje:

> Interação - 1
> Um docker que quando aperta um botão lê todos os pdfs e gera um grafico de topic modelig.
> Interação - 2
> Adicionar duckdb ao processo

> Que tenho que entregar amanhã a mesma coisa utilizando bibliotecas de OCR.

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

# Solution for data extract:

To tackle the challenge of data extraction, we will employ four storage layers:
Landing: Place where the PDF files are landing from external sources.
Bronze: Data with a low level of transformation(text extraction, table extraction)
Silver: Pre-processed data extracted text tokenized and lemmatized.
Gold: Documents after to extract meaningful information.

We will approach the problem of information extraction in these stages:

1 - Extract textual information from PDF and store it inside the raw directory in a folder named after the PDF file name. The file will be named pfd-file-name-text-extracted.txt.
2- Extract tables from the PDF and store them in the same folder as the previous step.
3 - Pre-process the extracted text for lemmatization, stop word removal, and store it in the raw folder.

> [!NOTE]
> In the production scenario for this solution, we can have two scenarios: Process the files soon,
> arrive at the landing folder, or schedule batch processing. We can use Airflow[^12] to schedule a job or a
> lambda function[^11] to trigger when a file arrives in the folder. With those scenarios in mind, we created a container to test possible solutions using Kubernetes.

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

For to extract information from PDF for further analysis we will to use PDFtoText. According with the article on Medium [^9] the python package PyMuPDF[^10] is a good choice because it preserves tables and original pdf structure. But after doing test with PyMuPDF the library does not extract tables correctly so I used tabular.

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
[^11]: [AWS Lambda Function — Watermarking a PDF via S3 Trigger in Python](https://supremecodr.medium.com/aws-lambda-function-watermarking-a-pdf-via-s3-trigger-in-python-5080b1afb72)
[^12]: [How to build a data extraction pipeline with Apache Airflow](https://towardsdatascience.com/how-to-build-a-data-extraction-pipeline-with-apache-airflow-fa83cb8dbcdf)
[^13]: [Downloading Multiple Files from DigitalOcean Spaces with Python](https://medium.com/@rahmanazhar/downloading-multiple-files-from-digitalocean-spaces-with-python-1531e3174347)
[^14] [Document Topic Extraction with Large Language Models (LLM) and the Latent Dirichlet Allocation (LDA) Algorithm](https://medium.com/@rahmanazhar/downloading-multiple-files-from-digitalocean-spaces-with-python-1531e3174347)
[^15] [Topic Modeling and Semantic Clustering with spaCy](https://fouadroumieh.medium.com/topic-modeling-and-semantic-clustering-with-spacy-960dd4ac3c9a)

duckdb

https://www.youtube.com/watch?v=n0npcfsZvnk


streamlit

https://www.youtube.com/watch?v=TkwOmjMtjLk

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

Abas Abertas

AbasAbertas
https://chat.openai.com/c/971d6749-4783-43a5-900d-8ad904bd4d37
https://colab.research.google.com/drive/1Evf5U0KgPnKoXNhpg2DFScG9OHG1YWrZ#scrollTo=LO-Gz8G-NhAw
https://medium.com/@rahmanazhar/downloading-multiple-files-from-digitalocean-spaces-with-python-1531e3174347
https://cloud.digitalocean.com/spaces/my-benefits?i=e52d76&path=pdf-no-ocr-data%2F&endpoints=&type=
https://fouadroumieh.medium.com/topic-modeling-and-semantic-clustering-with-spacy-960dd4ac3c9a
https://pomofocus.io/
https://spacy.io/usage/spacy-101
https://www.udemy.com/course/ocr-for-smart-data-extraction-from-pdf-and-images-with-ner/learn/lecture/34889070?components=add_to_cart%2Cavailable_coupons%2Cbase_purchase_section%2Cbuy_button%2Cbuy_for_team%2Ccacheable_buy_button%2Ccacheable_deal_badge%2Ccacheable_discount_expiration%2Ccacheable_price_text%2Ccacheable_purchase_text%2Ccurated_for_ufb_notice_context%2Ccurriculum_context%2Cdeal_badge%2Cdiscount_expiration%2Cgift_this_course%2Cincentives%2Cinstructor_links%2Clifetime_access_context%2Cmoney_back_guarantee%2Cprice_text%2Cpurchase_tabs_context%2Cpurchase%2Crecommendation%2Credeem_coupon%2Csidebar_container%2Cpurchase_body_container#overview
https://medium.com/@pranaysuyash/extracting-and-cleaning-data-from-pdfs-a-step-by-step-tutorial-using-python-tabula-and-jupyter-c3e0a8063c28
https://www.udemy.com/course/computer-vision-ocr-using-python/learn/lecture/25701872#overview
https://www.udemy.com/course/learn-streamlit-python/learn/lecture/23148022#overview
https://www.udemy.com/course/hands-on-natural-language-processing-using-python/learn/lecture/10042864#overview
https://www.udemy.com/course/awesome-natural-language-processing-tools-in-python/?couponCode=KEEPLEARNING
https://learning.oreilly.com/search/?q=spaCy&type=*&rows=10
https://learning.oreilly.com/library/view/practical-natural-language/9781492054047/ch02.html#preliminaries
https://learning.oreilly.com/library/view/mastering-spacy/9781800563353/B16570_Section_1_Final_JM_ePub.xhtml
https://learning.oreilly.com/library/view/mastering-spacy/9781800563353/B16570_01_Final_JM_ePub.xhtml#_idParaDest-17
https://www.linkedin.com/learning/hands-on-natural-language-processing/data-preprocessing-for-custom-ner?autoSkip=true&resume=false
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html
https://www.youtube.com/watch?v=bPbwA0wgh3I
https://rapidapi.com/collection/top-address-validation-api
https://www.google.com/
https://radimrehurek.com/gensim/intro.html
https://app.grammarly.com/ddocs/2404601678
https://towardsdatascience.com/how-to-build-a-data-extraction-pipeline-with-apache-airflow-fa83cb8dbcdf
https://docs.github.com/pt/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
https://www.digitalocean.com/community/questions/how-to-download-a-private-file-from-spaces-using-boto3
https://drive.google.com/drive/u/0/folders/1dw5Ib8RnyYbEMXrXvJQmpvjGzVDQiKnU
https://stackoverflow.com/questions/44441929/how-to-share-global-variables-between-tests
https://stackoverflow.com/questions/64943243/assert-a-list-containing-strings-with-specific-length
https://stackoverflow.com/questions/65819357/python-type-hints-for-spacy
https://emaddehnavi.medium.com/how-to-download-spacy-models-in-a-poetry-managed-environment-a174f5b77f1d
https://pynative.com/python-write-list-to-file/

