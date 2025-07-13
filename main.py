import json
import warnings
from datetime import date

import numpy as np
import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dateutil import parser

from modules.topsis.topsis import Topsis

warnings.filterwarnings('ignore')



# streamlit code
st.write('Press give your github url for the repo to be tested')

form = st.form(key='my-form')
x = form.text_input('Enter the github url to be tested : ')
submit = form.form_submit_button('Submit')

if submit:
    # got the url from user as argument as string
    a=x

    # running the script from here
    URL = a[0:8] + "api." + a[8:19] + "repos/" + a[19:]

    token="<YOUR_GITHUB_TOKEN>"
    headers={'Authorization':'token' + token}
    r = requests.get(URL,headers=headers)
    
    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

    table = soup.find('body').get_text()

    res = json.loads(table)

    res['owner_type'] = res["owner"]['type']

    del res['archive_url']
    del res['assignees_url']
    del res['blobs_url']
    del res['branches_url'] 
    del res['clone_url']
    del res['collaborators_url']
    del res['comments_url']
    del res['commits_url']
    del res['compare_url']
    del res['contents_url']
    del res['contributors_url']
    del res['deployments_url']
    del res['downloads_url']
    del res['events_url']
    del res['forks_url']
    del res['git_commits_url']
    del res['git_refs_url']
    del res['git_tags_url']
    del res['git_url']
    del res['hooks_url']
    del res['html_url']
    del res['issue_comment_url']
    del res['issue_events_url']
    del res['issues_url']
    del res['keys_url']
    del res['labels_url']
    del res['languages_url']
    del res['merges_url']
    del res['milestones_url']
    del res['notifications_url']
    del res['owner']
    del res['pulls_url']
    del res['releases_url']
    del res['ssh_url']
    del res['stargazers_url']
    del res['statuses_url']
    del res['subscribers_url']
    del res['subscription_url']
    del res['svn_url']
    del res['tags_url']
    del res['teams_url']
    del res['trees_url']
    del res['url']
    del res['allow_forking']
    del res['default_branch']
    del res['description']
    del res['disabled']
    del res['forks_count']
    del res['full_name']
    del res['has_downloads']
    del res['has_issues']
    del res['has_projects']
    del res['homepage']
    del res['id']
    del res['is_template']
    del res['language']
    del res['license']
    del res['mirror_url']
    del res['name']
    del res['network_count']
    del res['node_id']
    del res['open_issues']
    del res['private']
    del res['size']
    del res['temp_clone_token']
    del res['topics']
    del res['visibility']
    del res['watchers_count']
    del res['web_commit_signoff_required']
    del res['pushed_at']


    if res['fork']==False:
        res['fork']=0
    elif res['fork']==True:
        res['fork']=1
    if res['has_wiki']==False:
        res['has_wiki']=0
    elif res['has_wiki']==True:
        res['has_wiki']=1
        
    if res['has_pages']==False:
        res['has_pages']=0
    elif res['has_pages']==True:
        res['has_pages']=1
        
    if res['archived']==False:
        res['archived']=0
    elif res['archived']==True:
        res['archived']=1
        
    if res['owner_type']=='User':
        res['owner_type']=1
    elif res['owner_type']=='Organization':
        res['owner_type']=0
        

    res['created_at']=res['created_at'][0:10] 
    res['updated_at']=res['updated_at'][0:10] 
    res['created_at']=pd.to_datetime(res['created_at'])
    res['updated_at']=pd.to_datetime(res['updated_at'])

    today=date.today().strftime("%Y-%b-%d")
    today=parser.parse(today)
    res['created_at']=abs(res['created_at']-today)
    res['updated_at']=abs(res['updated_at']-today)

    res['created_at']=res['created_at']/ np.timedelta64(1, 'D')
    res['updated_at']=res['updated_at']/ np.timedelta64(1, 'D')
    res['created_at']=int(res['created_at'])
    res['updated_at']=int(res['updated_at'])

    if res['updated_at']==0:
        res['updated_at']=1

    owner_type=res['owner_type']
    is_archived=res['archived']
    is_forked=res['fork']
    open_issues=res['open_issues_count']
    forks=res['forks']
    stars=res['stargazers_count']
    watchers=res['watchers']
    has_wiki=res['has_wiki']
    has_pages=res['has_pages']
    recent_update=res['updated_at']
    days_created=res['created_at']


    row_to_add=[owner_type,is_archived,is_forked,open_issues,forks,stars,watchers,has_wiki,has_pages,recent_update,days_created]

    #importing DataFrame
    df=pd.read_csv(r'resources/datasets/repositories.csv',sep='\t')

    df=df.drop(['topic','name','owner','full_name','description','og_image','license','size','language','tags','has_sponsorship'],axis=1)
    df.owner_type[df.owner_type == 'Organization'] = 0
    df.owner_type[df.owner_type == 'User'] = 1
    df.is_archived[df.is_archived == False] = 0
    df.is_archived[df.is_archived == True] = 1
    df.is_forked[df.is_forked == False] = 0
    df.is_forked[df.is_forked == True] = 1
    df.has_wiki[df.has_wiki == False] = 0
    df.has_wiki[df.has_wiki == True] = 1
    df.has_pages[df.has_pages == False] = 0
    df.has_pages[df.has_pages == True] = 1


    df['created_date']=[d[0:10] for d in df['created_at']]
    df['updated_date']=[d[0:10] for d in df['updated_at']]

    df=df.drop(['created_at','updated_at'],axis=1)

    df['created_date']=pd.to_datetime(df['created_date'])
    df['updated_date']=pd.to_datetime(df['updated_date'])

    today=date.today().strftime("%Y-%b-%d")
    today=parser.parse(today)
    df['recent_update']=abs(df['updated_date']-today)
    df['days_created']=abs(df['created_date']-today)

    df=df.drop(['created_date','updated_date'],axis=1)

    df['recent_update']=df['recent_update'].astype('timedelta64[D]').astype(int)
    df['days_created']=df['days_created'].astype('timedelta64[D]').astype(int)

    df.loc[len(df.index)] = row_to_add

    df1=df
    df1=df1.to_numpy()

    weights = [1,2,1,2,6,8,5,1,1,1,1]
    criterias = np.array([True, False,False, False,True, True, True, True, True, False, True])
    t = Topsis(df1, weights, criterias)


    t.calc()

    b=t.best_similarity
    df = df.assign(best=b)

    df["Rank"] = df["best"].rank(method='max')
    row,col=df.shape
    rank=df['Rank']

    ranking=rank[rank.size-1]
    ans= (row-ranking)/row*10
    
    # print(format_float)
    ans = "{:.2f}".format(ans)

    st.write(f'Score : {ans}/10')