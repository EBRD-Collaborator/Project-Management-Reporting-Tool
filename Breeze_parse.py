#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import os.path
from ast import literal_eval
from sqlalchemy import create_engine
import psycopg2


# In[2]:


projects = requests.get('https://api.breeze.pm/V2/projects.json?api_token=zm5rrkdMjZsf-Mv_pPTi')
print(projects.status_code)


# In[3]:


cards = {}
not_read_projects = []
all_projects = []
for project in projects.json():    
    url = str(project['id']).join(('https://api.breeze.pm/V2/projects/', '/cards.json?api_token=zm5rrkdMjZsf-Mv_pPTi'))    
    print(url)    
    card = requests.get(url)
    print(card.status_code)
    name_with_id = ' - '.join((project['name'],str(project['id']))) 
    all_projects.append(name_with_id)
    try:
        cards[name_with_id] = card.json()        
    except:        
        not_read_projects.append((project['id'], card.status_code))
        pass
print(not_read_projects)


# In[4]:


table = {}
final = pd.DataFrame()
for card_i in cards.keys():
    table[card_i] = {'Project Name':[], 'Project ID':[],'Deliverable Name':[], 'Deliverable ID' : [],'Task Name':[], 
                     'Task ID':[], 'Target Date': [], 'Due Date': [], 'Deliverable Status': [], 'Flag':[], 
                     'Deliverable Value':[], 'Deliverable Currency':[], 'Comment':[], 'Deliverable Outcome':[],  
                     'Description':[], 'To-do lists' : [], 'Tags' : [], 'Task Column': [], 'Start Date':[], 'Date Updated':[], 'Assignee_first':[], 'Card Type':[], 'Deliverable Owner' : [], 'Deliverable Outcome Indicator' : []}  
    for card_list in cards[card_i]:          
        table[card_i]['Project Name'].append(card_i[:card_i.rfind(' ')-2])
        table[card_i]['Project ID'].append(card_i[card_i.rfind(' ')+1:])
        
        
        table[card_i]['Task Name'].append(card_list['name'])            
        table[card_i]['Due Date'].append(card_list['duedate'])
        table[card_i]['Deliverable ID'].append(card_list['swimlane_id'])
        table[card_i]['Task ID'].append(card_list['id'])
        table[card_i]['Task Column'].append(card_list['stage']['name'])
        table[card_i]['Deliverable Status'].append(card_list['status_name'])
        table[card_i]['Start Date'].append(card_list['startdate'])
        table[card_i]['Date Updated'].append(card_list['updated_at'])
        table[card_i]['Assignee_first'].append(card_list['user']['name'])
        if len(card_list['tags']) > 0:
            table[card_i]['Tags'].append(card_list['tags'])
        else:
            table[card_i]['Tags'].append(None)
        #print(item['description'])
        if 'description' in card_list.keys():
            #print(card_list['description'])
            table[card_i]['Description'].append(card_list['description'])
        else:
            table[card_i]['Description'].append(None)
        if 'swimlane' in card_list.keys():
            table[card_i]['Deliverable Name'].append(card_list['swimlane'])
        else:
            table[card_i]['Deliverable Name'].append(None)

        if len(card_list['custom_fields']) > 0:
            temp = {}
            needed_fields = {'RAG Status':'Flag', 'target date':'Target Date', 'deliverable_value':'Deliverable Value',
                            'deliverable_currency':'Deliverable Currency', 'status_comment':'Comment', 'deliverable_outcome':'Deliverable Outcome', 'deliverable_milestone' : 'Card Type', 'deliverable_owner':'Deliverable Owner', 'deliverable_outcome_indicator':'Deliverable Outcome Indicator'}
            for field in card_list['custom_fields']:
                temp[field['name']] = field['value']
                
            for field in needed_fields.keys():
                    
                if field in temp.keys():
                    if field == 'RAG Status':  
                        try:
                            table[card_i][needed_fields[field]].append(temp[field][:temp[field].index(' ')])                                
                        except ValueError:
                            table[card_i][needed_fields[field]].append(temp[field])                            
                    else:
                        table[card_i][needed_fields[field]].append(temp[field])
                       
                else:
                    table[card_i][needed_fields[field]].append(None)   
        else:
            table[card_i]['Flag'].append(None)
            table[card_i]['Target Date'].append(None)
            table[card_i]['Deliverable Value'].append(None)
            table[card_i]['Deliverable Currency'].append(None)
            table[card_i]['Comment'].append(None)
            table[card_i]['Deliverable Outcome'].append(None)
            table[card_i]['Card Type'].append(None)
            table[card_i]['Deliverable Owner'].append(None)
            table[card_i]['Deliverable Outcome Indicator'].append(None)    
                
        if len(card_list['todo_lists']) > 0:
            todos = []
            for unit in card_list['todo_lists']:
                #print(card_i)                    
                for unity in unit['todos']:
                    to_add = ()
                    to_add = to_add + (unity['name'],)
                    #print(unity.keys())
                    if 'duedate' in unity.keys():                            
                        to_add = to_add + (unity['duedate'],)
                    else:
                        to_add = to_add + (None,)
                    if 'done' in unity.keys():
                        if unity['done'] == True:
                            to_add = to_add + ('Done',)
                        else:
                            to_add = to_add + ('Not Done',) 
                    else:
                        to_add = to_add + (None,)
                    todos.append(to_add)
            table[card_i]['To-do lists'].append(todos)
        else:
            table[card_i]['To-do lists'].append(None)    


# In[5]:


final = pd.DataFrame()
for i in table.keys():        
    asas = pd.DataFrame.from_dict(table[i])
    final = final.append(asas)  
    
final = final.fillna(value=float('Nan'))
if not os.path.isfile(r'/Users/uzer/Downloads/test.xlsx'):   
    final.to_excel(r'/Users/uzer/Downloads/test.xlsx',sheet_name='Latest Download')
final.head(3)


# In[6]:


last = pd.read_excel(r'/Users/uzer/Downloads/test.xlsx', engine='openpyxl', sheet_name='Latest Download')
last.set_index(['Unnamed: 0'],inplace=True)
last.index.name = None


# In[7]:


final = final.fillna(value=float('Nan'))
final['Project ID'] = final['Project ID'].astype('int64')


# In[8]:


difference = pd.DataFrame()
for i in all_projects:    
    new = last[last['Project Name'] == i[:i.rfind(' ')-2]].merge(final[final['Project Name'] == i[:i.rfind(' ')-2]], how='right', on=['Project Name', 'Project ID', 'Deliverable Name',
                                                                                                                                      'Deliverable ID','Task Name', 'Task ID', 
                                                                                                                                      'Target Date', 'Due Date', 'Deliverable Status',
                                                                                                                                      'Flag', 'Deliverable Value',
                                                                                                                                      'Deliverable Currency', 'Comment', 
                                                                                                                                      'Deliverable Outcome', 'Description',
                                                                                                                                      'To-do lists', 'Tags', 'Task Column', 'Start Date', 'Date Updated',
                                                                                                                                      'Assignee_first'], left_index=True, right_index=True)
   
    difference = difference.append(new)
difference.head(2)


# In[9]:


list_of_dfs = [last, final, difference]
sheets = ['Previous Download', 'Latest Download', 'Difference']
total = list(zip(list_of_dfs, sheets))


# In[10]:


with pd.ExcelWriter(r'C:\Users\Zver\Desktop\Breeze_report.xlsx') as writer:
    for df, sheet in total:        
        df.to_excel(writer,sheet_name=sheet)


# In[11]:


def create_card(df, columns):
    new_df = df[columns]
    return new_df

cards_columns = ['Task ID', 'Deliverable ID', 'Project ID', 'Task Name', 'Description', 'Task Column', 'Deliverable Status', 
                'Assignee_first', 'Due Date', 'Start Date', 'Date Updated', 'Flag']
previous_cards_df = create_card(last, cards_columns)
latest_cards_df = create_card(final, cards_columns)


# In[12]:


def create_to_do(df, mode='previous'):
    df = df[~df['To-do lists'].isnull()]
    if mode == 'latest':
        pass
    else:
        df['To-do lists'] = df['To-do lists'].apply(literal_eval) #convert to list type
    df = df.explode('To-do lists')
    df[['To-do Name', 'To-do Due Date', 'To-do Status']] = pd.DataFrame(df['To-do lists'] .tolist(), index=df.index)
    df.drop(columns=['To-do lists'],inplace=True)
    return df

todos_columns = ['Task ID', 'Task Name', 'To-do lists']
previous_todos_df = create_card(last, todos_columns)
previous_todos_df = create_to_do(previous_todos_df)
latest_todos_df = create_card(final, todos_columns)
latest_todos_df = create_to_do(latest_todos_df, 'latest')


# In[13]:


tags_columns = ['Task ID', 'Tags']

def create_tags(df, mode='previous'):  
    df = df[~df['Tags'].isnull()]
    if mode == 'latest':
        pass
    else:
        df['Tags'] = df['Tags'].apply(literal_eval)
    df = df.explode('Tags')
    return df
previous_tags_df = create_card(last, tags_columns)
previous_tags_df = create_tags(previous_tags_df)
latest_tags_df = create_card(final, tags_columns)
latest_tags_df = create_tags(latest_tags_df, 'latest')


# In[14]:


delivs_cols = ['Deliverable Name', 'Deliverable ID', 'Deliverable Value', 'Target Date']
previos_delivs_df = create_card(last, delivs_cols)
latest_delivs_df = create_card(final, delivs_cols)


# In[15]:


project_cols = ['Project Name', 'Project ID']
previous_projects = create_card(last, project_cols)
latest_projects = create_card(final, project_cols)
previous_projects.drop_duplicates(inplace=True)
latest_projects.drop_duplicates(inplace=True)


# In[16]:


engine = create_engine('postgresql://john:myPassword@116.202.173.47:5432/johndb')
previous_cards_df.to_sql('previous_cards', engine, if_exists='replace')
print('previous_cards is saved')
latest_cards_df.to_sql('latest_cards', engine, if_exists='replace')
print('latest_cards is saved')
previous_todos_df.to_sql('previous_todos', engine, if_exists='replace')
print('previous_todos_df is saved')
latest_todos_df.to_sql('latest_todos', engine, if_exists='replace')
print('latest_todos_df is saved')
previous_tags_df.to_sql('previous_tags', engine, if_exists='replace')
print('previous_tags_df is saved')
latest_tags_df.to_sql('latest_tags', engine, if_exists='replace')
print('latest_tags_df is saved')
previos_delivs_df.to_sql('previous_deliverables', engine, if_exists='replace')
print('previos_delivs_df is saved')
latest_delivs_df.to_sql('latest_deliverables', engine, if_exists='replace')
print('latest_delivs_df is saved')
previous_projects.to_sql('previous_projects', engine, if_exists='replace')
print('previous_projects is saved')
latest_projects.to_sql('latest_projects', engine, if_exists='replace')
print('latest_projects is saved')


# In[ ]:




