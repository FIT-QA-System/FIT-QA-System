
# coding: utf-8

# In[1]:


from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import WordNetError
from nltk import word_tokenize, pos_tag   ##implementation of similarity() from http://nlpforhackers.io/wordnet-sentence-similarity/
def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'
 
    return None
 
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
 
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None
def pathsim(ss1, ss2):
    if ss1.path_similarity(ss2) is None:
        return 0
    return ss1.path_similarity(ss2)
def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    NoneType = type(None)
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence1nv = []
    sentence2 = pos_tag(word_tokenize(sentence2))
    sentence2nv = []
    # Get the synsets for the tagged words
    synsets1 = []
    count1 = 0
    count2=0
    tup = ()
    synsetnone1 = []
    for tagged_word in sentence1:
        if type(tagged_to_synset(*tagged_word))== NoneType and tagged_word[0][0].isupper() and penn_to_wn(tagged_word[1]) == 'n':
            count1 += 1
            tup = (tagged_word[0], tagged_word[1])
            sentence1nv.append(tup)
            synsetnone1.append(tup)
            continue
        if penn_to_wn(tagged_word[1]) == 'n':
            count1 += 1
            tup = (tagged_word[0], tagged_word[1])
            sentence1nv.append(tup)
    synsets2 = []
    tup = ()
    synsetnone2 = []
    for tagged_word in sentence2:
        if type(tagged_to_synset(*tagged_word))== NoneType and tagged_word[0][0].isupper() and penn_to_wn(tagged_word[1]) == 'n':
            count2+=1
            tup = (tagged_word[0], tagged_word[1])
            sentence2nv.append(tup)
            synsetnone2.append(tup)
            continue
        if penn_to_wn(tagged_word[1]) == 'n':
            count2+=1
            tup = (tagged_word[0], tagged_word[1])
            sentence2nv.append(tup)
    synsets1 = [tagged_to_synset(tagged_word, tag) for tagged_word, tag in sentence1nv]
    synsets2 = [tagged_to_synset(tagged_word, tag) for tagged_word, tag in sentence2nv]
    
    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if not type(ss) == NoneType]
    synsets2 = [ss for ss in synsets2 if not type(ss) == NoneType]
    score = 0.0
    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        if not synsets2 == []:
            best_score = max([pathsim(synset, ss) for ss in synsets2])
        # Check that the similarity could have been computed
            if best_score is not None:
                score += best_score
    for synset in synsets2:
        # Get the similarity value of the most similar word in the other sentence
        if not synsets1 == []:
            best_score = max([pathsim(synset, ss) for ss in synsets1])
        # Check that the similarity could have been computed
            if best_score is not None:
                score += best_score
    for synsetnone in synsetnone2:
        if synsetnone in synsetnone1:
            score += 1
    for synsetnone in synsetnone1:
        if synsetnone in synsetnone2:
            score += 1
    # Average the values
    score /= (count1 + count2)
    return score



# In[16]:



def namedentity():
    sent = tb.tagged_sents()[22]
    print() 


# In[17]:


namedentity()


# In[31]:



import pickle
import re
import spacy
from Milestone2.course_info.get_info import Course
def hasclass(question):
    courses = pickle.load(open("Milestone2/course_info/courses.txt", "rb"))
    #nlp = spacy.load("en")

   # print(nlp(question))
    #course = nlp(question).ents[0].text

    answer_course = None

    for c in courses:
        if c.title in question:
            answer_course = c
    if answer_course!=None :
        return True
    return False


# In[130]:



import pickle
import re
import spacy
import json
def hasfaculty(question):
    with open('website/FIT_QA_SYSTEM/QA/data/department_staff_json.json', 'r') as f:
        data = json.load(f)
    for d in data:
        astaff=None
        staff = d['department_employees']['records']
        if staff!=None:
            for s in staff:
                if s['name']['first'] in question or s['name']['last'] in question:
                    astaff = s
        if astaff!=None :
            return True
    #nlp = spacy.load("en")

    #building = nlp(question).ents[0].text

    return False


# In[79]:



import pickle
import re
import spacy
import json
def hasbuilding(question):
    with open('website/FIT_QA_SYSTEM/QA/data/buildings.json', 'r') as f:
        data = json.load(f)

    buildings = data['records']
    nlp = spacy.load("en")

    #building = nlp(question).ents[0].text
    answer_building = None

    for b in buildings:
        if b['code'] in question or b['name'] in question:
            answer_building = b
    if answer_building!=None :
        return True
    return False


# In[34]:


def hasevent(question):
    if "event" in question:
        return True
    return False


# In[35]:


def hasdate(question):
    if "date" in question:
        return True
    return False


# In[86]:


import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import treebank as tb
from nltk.corpus.reader.wordnet import WordNetError
from nltk import word_tokenize, pos_tag 

def categorize_questions(question):
    
    categories=["Location","Instructor","Class Time","Classroom","Office Location","Office Hours","Building Hours","Contact","Others"]
    #maxsimilarity = 0
    #tags = pos_tag(word_tokenize(question))
    #print(nltk.ne_chunk(tags))
    ##building hours:
    if "When" in question or "when" in question or "time" in question: #1.1 & 1.3 & 1.4 & 1.5, 1.2
        if hasbuilding(question):
            return categories[6]
    if "open" in question or "close" in question or "closed" in question:
        if "Why" in question or "How" in question:
            return categories[8]
        return categories[6]
    if "building hours" in question:
        return categories[6]
    ##instructor
    if "instructor" in question or "teacher" in question or "teaches" in question: #2.1 2.2 2.3 class info-instructor=who+class title
   #     for word in tags:
   #         if pos_tag(word)[1]==
        if hasclass(question):
            return categories[1]
    ##class time
    if "what" in question or "What" in question:
        if "time" in question:
            if hassclass(question):
                return categories[2] ##3.1
    if "when" in question or "When" in question:
        if hasclass(question):
            return categories[2] ##3.2 3.3
    ##classroom location
    if "Where" in question or "where" in question or "location" in question or "Which building" in question:
        if hasclass(question):
            return categories[3] ##4.1 4.2 4.3
    ##faculty office location
    if "Where" in question or "where" in question or "location" in question:
        if hasbuilding(question):
            return categories[0]
        if hasfaculty(question):
            if "from" in question:
                return categories[8]
            return categories[4] ##5.1 5.2
        
    ##office hours
    if "office hours" in question or "When" in question and "office" in question:
        return categories[5]##6.2
    ##contact
    if "contact" in question or "email" in question or "phone number" in question:
        if hasfaculty(question):
            return categories[7] ##7.1 7.2
    if "When" in question:
        if hasevent(question):
            return "Calendar"
    if "event" in question:
        if hasdate(question):
            return "Calendar"
    
    #for sample in samples:
    #    similarity = sentence_similarity(question,sample)
    #    if similarity > maxsimilarity:
    #        maxsimilarity = similarity
    #        category = sample
    return categories[8]


# In[37]:


print(categorize_questions("Who's the instructor of cse 4001"))
print(categorize_questions("who teaches cse 4001"))


# In[38]:


print(categorize_questions("What's the location of the dining hall"))
print(categorize_questions("Where is the dining hall"))


# In[41]:


print(categorize_questions("When is the dining hall open"))
print(categorize_questions("the building hours of the dining hall"))
print(categorize_questions("is the dining hall open now?"))
print(categorize_questions("Why is the dining hall closed now?"))


# In[42]:


print(categorize_questions("Where is Dr. John Doe"))
print(categorize_questions("location of Dr. Chan's office"))
print(categorize_questions("Where is Dr. John Doe from"))


# In[43]:


print(categorize_questions("Dr. John Doe's office hours"))
print(categorize_questions("When can I go to Dr. XX's office?"))


# In[44]:


print(categorize_questions("What's Dr. Shoaff's phone number"))
print(categorize_questions("What's Dr. Shoaff's email address"))
print(categorize_questions("how can I contact Dr. John Doe"))


# In[45]:


print(categorize_questions("What is Dr.Stansifer's phone number"))


# In[10]:


print(categorize_questions("is wds@fit.edu Dr.Shoaff's email address?"))


# In[90]:


print(categorize_questions("How can I log in to TRACKS"))


# In[92]:



print(categorize_questions("location of the classroom of cse 4001"))

print(categorize_questions("Where is cse 4001"))
print(categorize_questions("can I bring food into the classroom of cse 4001"))


# In[8]:


print(categorize_questions("When is the XX event"))
print(categorize_questions("what event is on date xx"))


# In[73]:


import pickle
import re
import spacy
def answer_location(question):
    with open('website/FIT_QA_SYSTEM/QA/data/buildings.json', 'r') as f:
        data = json.load(f)
    nlp = spacy.load("en")
    buildings = data['records']
    #print(nlp(question))
    #building = nlp(question).ents[0].text

    ab = None

    for b in buildings:  ##index(hashtable(unique key--ID,multiple indices,can be course number,building number,teacher,+value, can ask database to do it), tree) on top of data
        if b['code'] in question or b['name'] in question:
            ab = b
    return ab['street']+' '+str(ab['number'])


# In[49]:



import pickle
import re
import spacy
from Milestone2.course_info.get_info import Course
def answer_class(question,subtype):
    courses = pickle.load(open("Milestone2/course_info/courses.txt", "rb"))
    #nlp = spacy.load("en")

    #print(nlp(question))
    #course = nlp(question).ents[0].text

    answer_course = None

    for c in courses:  ##index(hashtable(unique key--ID,multiple indices,can be course number,building number,teacher,+value, can ask database to do it), tree) on top of data
        if c.title in question:
            answer_course = c
    #print(answer_course)
    if subtype == "Instructor":
        return answer_course.instructor
    elif subtype == "Classroom":
        return answer_course.place
    elif subtype == "Class Time":
        return answer_course.days + " " + answer_course.time
    else:
        return answer_course.__dict__


# In[145]:



import pickle
import re
import spacy
import json
def answer_staff(question,cat):
    with open('website/FIT_QA_SYSTEM/QA/data/department_staff_json.json', 'r') as f:
        data = json.load(f)
    astaff=None
    for d in data:
        
        staff = d['department_employees']['records']
        if staff!=None:
            for s in staff:
                if s['name']['first'] in question or s['name']['last'] in question:
                    if cat=="Office Location":
                        if 'building' in s['position']['primary'].keys():
                            astaff=s['position']['primary']['building']['code']+' '+str(s['position']['primary']['building']['number'])
                    elif cat=="Contact":
                        astaff='email: '+s['email']
                        if 'phone' in s['position']['primary'].keys():
                            astaff = astaff+' '+'phone: '+s['position']['primary']['phone']['display']["area_code"]+s['position']['primary']['phone']['display']["number"]

    return astaff


# In[51]:


def answer_buildinghours(question):
    return "hours"


# In[148]:


def answer_frompassage(question):
    from googleapiclient.discovery import build
    service = build("customsearch", 'v1',developerKey="AIzaSyDjsBfa0igZZQUL6gMdDKEMIGsX6j-2HVA")
    res = service.cse().list(q=question, cx="006188269277128775091:loi0aooxt4w").execute()
    return res['url']


# In[53]:


def exists(question):
    return False;


# In[54]:


def get_answer(question):
    return "old"


# In[150]:


def typeof(question):
    cat = categorize_questions(question)
    t=1
    if cat=="Instructor" or cat=="Class Time" or cat=="Classroom":
        t=0
    elif cat=="Office Hours" or cat=="Contact":
        t=0
    elif cat=="Building Hours":
        t=0
    return t


# In[55]:


from Milestone2.course_info.get_info import Course
def answer(question):
    if exists(question):
        answer=get_answer(question)
        return answer
    cat = categorize_questions(question)
    if cat=="Location":
        answer = answer_location(question)
    elif cat=="Instructor" or cat=="Class Time" or cat=="Classroom":
        answer = answer_class(question,cat);
    elif cat=="Office Location" or cat=="Office Hours" or cat=="Contact":
        answer = answer_staff(question,cat);
    elif cat=="Building Hours":
        answer = answer_buildinghours(question);
    else:
        answer = answer_frompassage(question);
    return answer


# In[56]:


print(answer("Who's the instructor of Intro to Human Factors"))
print(answer("Where is the classroom of Intro to Human Factors"))
print(answer("Who teaches Intro to Human Factors"))
print(answer("When is Intro to Human Factors"))
print(answer("Can you bring food into the classroom of Intro to Human Factors"))


# In[38]:


print(answer("Who's the instructor of Intro to Human Factors"))


# In[87]:


print(answer("Where is Aberdeen - Building 5442"))


# In[139]:


print(answer("how can I contact Dr. Shoaff"))


# In[147]:


print(answer("where's Dr. Shoaff's office"))


# In[149]:


print(answer("what a nice day"))

