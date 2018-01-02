#encoding=utf-8
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib

if __name__ == '__main__':
    df = pd.read_csv('dateset1.csv',encoding='utf8')
   # df.info()
    print(type(df['uri']))

    print(df['label'].value_counts())
    print('########################')
    #df.head()


    print(df[df['label'] == 1].head())
    print('????????????????????????')
    attributes = ['uri', 'label']
   # x_train, x_test, y_train, y_test = train_test_split(df[attributes], df['label'], test_size=0.1,
   #                                                     stratify=df['label'], random_state=0)



   # x_train, x_dev, y_train, y_dev = train_test_split(x_train, y_train, test_size=0.1,
    #                                                  stratify=y_train, random_state=0)


    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer,TfidfVectorizer

   # tv = TfidfVectorizer(analyzer='word', use_idf= True)


    tv = TfidfVectorizer(analyzer=u'word')
    n_grams_tfidf = tv.fit_transform(df['uri'])


    dftrain = pd.read_csv('dateset2.csv', encoding='utf8')
    n_test_grams_tfidf = tv.transform(dftrain['uri'])


    print(n_test_grams_tfidf[0])
    print('*************')
    print(n_test_grams_tfidf[1])
    print('*************')
    print(n_test_grams_tfidf[2])
    print('*************')
    print(n_test_grams_tfidf[3])