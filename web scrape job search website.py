base_url = 'https://www.jobstreet.com.sg/en/job-search/job-vacancy.php'
pay_load = {'key':'','area':1,'option':1,'pg':None,'classified':1,'src':16,'srcr':12}
pay_load['key'] = 'health data project' # this can be changed to any other keywords

# Load the first 20 pages that are having job postings related to the keywords, extract position names, company names, and URLs
pn = 1
job_list = []
position_links = []
loaded = True
while loaded and pn < 21:
    print('Loading page {} ...'.format(pn))
    pay_load['pg'] = pn
    r = requests.get(base_url, headers=headers, params=pay_load)

    soup = BeautifulSoup(r.text,'html.parser')
    links = soup.find_all('div',{'class':'sx2jih0 zcydq8bm'})
        
    for link in links:
        sub_link = link.find('h1')
        sub_link_1 = link.find('a', {'class':'_6xa4xb0 sx2jih0 sx2jihf rqoqz4'})
            
        if sub_link:
            urllist = [sub['href'] for sub in sub_link]
            joblist = [sub.get_text() for sub in sub_link]
            
        if sub_link_1:
            companylist = [sub.get_text() for sub in sub_link_1]
            
            job_list.append([joblist, companylist, urllist])
        
   
        if not len(links):
            loaded = False
        else:
            position_links += links
            pn += 1
 
# Put the extracted information into a data frame
job_df = pd.DataFrame (job_list, columns = ['job', 'company', 'URL'])
job_df['job'] = job_df['job'].str[0]
job_df['company'] = job_df['company'].str[0]
job_df['URL'] = job_df['URL'].str[0]
job_df = job_df.drop_duplicates()
job_df = job_df.reset_index()
job_df["URL_full"] = "https://www.jobstreet.com.sg" + job_df['URL'] 

# Get the full job description and requirements based on the URLs
job_requirements_list = []
for i in range(len(job_df['URL_full'])):
    url = job_df['URL_full'][i]
    job_page = requests.get(url)
    job_soup = BeautifulSoup(job_page.text,'html.parser')
    
    job_requirements = job_soup.find_all('li')
    
    if job_requirements:
        if str(job_requirements).startswith("[<li"):
            job_requirements = [req.string for req in job_requirements if req]
            job_requirements = [str(job_req).replace('None, ', '') for job_req in job_requirements if job_req] 
        else:
            job_requirements = [job_req for job_req in [job_requirements]][0]
        
            job_requirements = [str(job_req).replace('<li>', '') for job_req in job_requirements if job_req]  
            job_requirements = [str(job_req).replace('<strong>', '') for job_req in job_requirements if job_req] 
            job_requirements = [str(job_req).replace('</li>', '') for job_req in job_requirements if job_req]  
            job_requirements = [str(job_req).replace('</strong>', '') for job_req in job_requirements if job_req] 
            job_requirements = [str(job_req).replace('&amp;', '') for job_req in job_requirements if job_req] 
    
    if job_requirements == []:
        job_requirements = ['NA']
 
    job_requirements_list.append(job_requirements)


job_df['job requirements'] = job_requirements_list
job_df['job requirements'] = job_df['job requirements'].apply(lambda x: str(x).replace('[','').replace(']','')) 
job_df['job requirements'] = job_df['job requirements'].apply(lambda x: str(x).replace('\\xa0','')) 

# Apply data cleaning to job descriptions (remove stopwords, punctuations, space, numbers etc.)
def preprocess(text):
    text = text.lower() 
    text=text.strip()  
    text=re.compile('<.*?>').sub('', text) 
    text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text)  
    text = re.sub('\s+', ' ', text)  
    text = re.sub(r'\[[0-9]*\]',' ',text) 
    text=re.sub(r'[^\w\s]', '', str(text).lower().strip())
    text = re.sub(r'\d',' ',text) 
    text = re.sub(r'\s+',' ',text) 
    return text

def stopword(string):
    a= [i for i in string.split() if i not in stopwords.words('english')]
    return ' '.join(a)

def finalpreprocess(string):
    return stopword(preprocess(string))

job_df['job requirements clean'] = job_df['job requirements'].apply(lambda x: finalpreprocess(x))

# Find the most frequently used words in each job description
def findtopwords(text):
    counts = Counter(re.findall('\w+', text))
    return counts.most_common()[0:5]

job_df['job requirements word counts'] = job_df['job requirements clean'].apply(lambda x: findtopwords(x))

# Create custom flags to find postings that are most related to our interestes
job_df['flag - programming'] = job_df['job requirements clean'].str.contains('programming', regex=False)
job_df['flag - r'] = job_df['job requirements clean'].str.contains(' r ', regex=False)
job_df['flag - python'] = job_df['job requirements clean'].str.contains('python', regex=False)
job_df['flag - spss'] = job_df['job requirements clean'].str.contains('spss', regex=False)
job_df['flag - mental'] = job_df['job requirements clean'].str.contains('mental', regex=False)
job_df['flag - project'] = job_df['job requirements clean'].str.contains('project', regex=False)
job_df['flag - survey'] = job_df['job requirements clean'].str.contains('survey', regex=False)

cols = ['flag - programming', 'flag - r', 'flag - python', 'flag - spss', 'flag - mental', 'flag - project', 'flag - survey']
job_df['flag numbers'] = job_df[cols].sum(axis=1)

# Export the data frame to a csv file
job_df.to_csv(r'your working directory\Job search.csv', index=False)

# In the data frame or csv file we can further sort by number of flags and filter out the job postings that are more related to our interests.
