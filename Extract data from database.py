#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2
import numpy as np
import pandas as pd


# In[2]:


conn = psycopg2.connect(
        host=" ",
        database=" ",
        user=" ",
        password=" ")
print("Database opened successfully")


# In[3]:


sql_query = f"""
SELECT *
FROM latest_cards
;
"""

latest_cards = pd.read_sql(sql_query, con=conn)
latest_cards.tail()


# In[4]:


latest_cards.to_csv('latest_cards.csv')


# In[5]:


sql_query = f"""
SELECT *
FROM latest_deliverables
;
"""

latest_deliverables = pd.read_sql(sql_query, con=conn)
latest_deliverables.tail(3)


# In[6]:


latest_deliverables.to_csv('latest_deliverables.csv')


# In[7]:


sql_query = f"""
SELECT *
FROM latest_projects
;
"""

latest_projects = pd.read_sql(sql_query, con=conn)
latest_projects.tail(3)


# In[8]:


latest_projects.to_csv('latest_projects.csv')


# In[9]:


sql_query = f"""
SELECT *
FROM latest_tags
;
"""

latest_tags = pd.read_sql(sql_query, con=conn)
latest_tags.tail(3)


# In[10]:


latest_tags.to_csv('latest_tags.csv')


# In[11]:


sql_query = f"""
SELECT *
FROM latest_todos
;
"""

latest_todos = pd.read_sql(sql_query, con=conn)
latest_todos.tail(3)


# In[12]:


latest_todos.to_csv('latest_todos.csv')


# In[13]:


sql_query = f"""
SELECT *
FROM previous_cards
;
"""

previous_cards = pd.read_sql(sql_query, con=conn)
previous_cards.tail(3)


# In[14]:


previous_cards.to_csv('previous_cards.csv')


# In[15]:


sql_query = f"""
SELECT *
FROM previous_deliverables
;
"""

previous_deliverables = pd.read_sql(sql_query, con=conn)
previous_deliverables.tail(3)


# In[16]:


previous_deliverables.to_csv('previous_deliverables.csv')


# In[17]:


sql_query = f"""
SELECT *
FROM previous_projects
;
"""

previous_projects = pd.read_sql(sql_query, con=conn)
previous_projects.tail(3)


# In[18]:


previous_projects.to_csv('previous_projects.csv')


# In[19]:


sql_query = f"""
SELECT *
FROM previous_tags
;
"""

previous_tags = pd.read_sql(sql_query, con=conn)
previous_tags.tail(3)


# In[20]:


previous_tags.to_csv('previous_tags.csv')


# In[21]:


sql_query = f"""
SELECT *
FROM previous_todos
;
"""

previous_todos = pd.read_sql(sql_query, con=conn)
previous_todos.tail(3)


# In[22]:


previous_todos.to_csv('previous_todos.csv')

