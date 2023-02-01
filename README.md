Getting tired of manually browsing hundreds of job postings? Being frustrated by not seeing the desired job postings after trying different combinations of keywords? No worries, why not let computers handle the dirty job for us? Imagine feed Python with some keywords and requirements and let your computer go gather all the information for you? 

This repo is providing some codes to web-scrape job searching websites, I used Job Street as an example. The final output is a table that contains job names, company names, job posting URLs, job descriptions & requirements, word frequencies, and custom flags. Below are the steps of how to get this final output:

Step 1: Use self-defined keywords (such as "data analyst') to browse the job searching page and extract all positions that are related to the keywords. Based on the extracted information, create a data table that contains job names, company names, job URLs, job descriptions and requirements. 

Step 2: Apply data cleaning to the job description and requirement column (e.g. remove stop words, remove punctuations, tokenize sentences), count word frequencies and report the top six frequently used words in each job description. 

Step 3: Add custom flags. Say the jobs we are interested in are related to R/python/SPSS programming and project management, so intuitively we'd wnat to find job postings that contain "R", "Python", "SPSS", "programming", "project", "management". We calculate how many keywords each job posting has and put the count into a column.

Step 4: Sort by the number of custom flags and find the job postings that are most likely aligning to our interests. Then click their URLs, read the job posting, and apply for the position. 
