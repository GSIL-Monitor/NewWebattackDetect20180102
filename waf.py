#encoding=utf-8
import importlib,sys
importlib.reload(sys)
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib

if __name__ == '__main__':
    df = pd.read_csv('3.csv',encoding='utf-8')
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


    tv = TfidfVectorizer(analyzer='char',sublinear_tf=True, ngram_range=(1,3))
    n_grams_tfidf = tv.fit_transform(df['uri'].values.astype('U'))

    print('************************')
    print(n_grams_tfidf[0])
    '''
    print('************************')
    print(n_grams_tfidf[1])
    print('************************')
    print(n_grams_tfidf[2])
    print('************************')
    print(n_grams_tfidf[3])
    print('************************')
    print(n_grams_tfidf[4])
    print('************************')
    print(n_grams_tfidf[5])
    print('************************')
    print(n_grams_tfidf[6])
'''


    from sklearn.tree import DecisionTreeClassifier


    clf = DecisionTreeClassifier(random_state=0).fit(n_grams_tfidf, df['label'])


    from sklearn.externals import joblib
    joblib.dump(clf,'waf.pkl')

    joblib.dump(tv, "waf.m")
  #  x = '12345'

  #  print(clf.predict(x))



   # n_grams_train = count_vectorizer.fit_transform(x_train['uri'])
   # n_grams_dev = count_vectorizer.transform(x_dev['uri'])



   # n_grams_dev = count_vectorizer.transform(x_dev['uri'])
  #  print('Number of features:', len(count_vectorizer.vocabulary_))