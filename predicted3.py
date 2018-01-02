#encoding=utf-8
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer

if __name__ == '__main__':

   # vocabulary = ['word', 'hello', 'apple', 'milk']
   # tv = TfidfVectorizer(analyzer=u'word', vocabulary = vocabulary)
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer,TfidfVectorizer
#为了解决测试集vocabulary维度不同，先加载训练集的vocabulary
    #参考文章http://blog.csdn.net/u013083549/article/details/51262721?locationNum=2

    #tv = joblib.load('waf.m')tfidf_1234.m
    tv = joblib.load('tfidf_1234.m')

    df = pd.read_csv('POSTblackdata.csv', encoding='utf-8')
    n_grams_tfidf = tv.transform(df['uri'].values.astype('U'))
    print(n_grams_tfidf[0])
    print('*************')



   # sgd = joblib.load('waf.pkl')test1234.pkl
    sgd = joblib.load('test1234.pkl')
    from sklearn.metrics import accuracy_score
    predicted = sgd.predict(n_grams_tfidf)
    print('start')
    for i in range(0,len(predicted)):
        if(predicted[i]!= df['label'][i] ):
            print((str(df['uri'][i]))+'预测的'+ str(predicted[i]) +'实际的'+str(df['label'][i] ))
    print('end')
    print("Classifier accuracy:", accuracy_score(df['label'], predicted))






   # n_grams_train = count_vectorizer.fit_transform(x_train['uri'])
   # n_grams_dev = count_vectorizer.transform(x_dev['uri'])



   # n_grams_dev = count_vectorizer.transform(x_dev['uri'])
  #  print('Number of features:', len(count_v1.vocabulary_))