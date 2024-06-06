# Urdu Stories Web Scraping 

## Description
This project involves scraping Urdu stories using Scrapy. It allows users to extract data from the website [UrduZone](https://www.urduzone.net) and process it for various purposes.

## Setup

Follow the following steps to get the web scraping code running.

### 1. Create and Activate Virtual Environment
First, we need to create a virtual environment. For that, use the following command:
```bash
virtualenv venv
```

```bash
source venv/bin/activate
```

### 2. Install Scrapy library
Now, we need to install Scrapy. You can install it using pip:
```bash
pip install scrapy
```

### 3. Creating a Spider
cd urdu_stories

```bash
scrapy genspider I200603urdu_stories_spider https://www.urduzone.net
```