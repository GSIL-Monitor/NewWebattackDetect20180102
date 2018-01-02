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
    x_train, x_test, y_train, y_test = train_test_split(df['uri'], df['label'], test_size=0.5,
                                                        stratify=df['label'], random_state=0)



   # x_train, x_dev, y_train, y_dev = train_test_split(x_train, y_train, test_size=0.1,
    #                                                  stratify=y_train, random_state=0)


    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer,TfidfVectorizer

    from sklearn.tree import DecisionTreeClassifier

    tv = TfidfVectorizer(analyzer='char',ngram_range={1,4})
    train_grams_tfidf = tv.fit_transform(x_train.values.astype('U'))
    clf = DecisionTreeClassifier(random_state=0).fit(train_grams_tfidf, y_train)

    test_grams_tfidf = tv.transform(x_test.values.astype('U'))
    test_predicted = clf.predict(test_grams_tfidf)

    from sklearn.metrics import accuracy_score
    print("SGDClassifier accuracy:", accuracy_score(y_test, test_predicted))




