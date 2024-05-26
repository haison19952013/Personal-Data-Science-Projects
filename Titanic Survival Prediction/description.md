# The Challenge
![](https://www.kaggle.com/competitions/titanic)
The sinking of the Titanic is one of the most infamous shipwrecks in history.

On April 15, 1912, during her maiden voyage, the widely considered “unsinkable” RMS Titanic sank after colliding with an iceberg. Unfortunately, there weren’t enough lifeboats for everyone onboard, resulting in the death of 1502 out of 2224 passengers and crew.

While there was some element of luck involved in surviving, it seems some groups of people were more likely to survive than others.

In this challenge, we ask you to build a predictive model that answers the question: “what sorts of people were more likely to survive?” using passenger data (ie name, age, gender, socio-economic class, etc).

# What Data Will I Use in This Project?
In this competition, you’ll gain access to two similar datasets that include passenger information like name, age, gender, socio-economic class, etc. One dataset is titled `train.csv` and the other is titled `test.csv`.

Train.csv will contain the details of a subset of the passengers on board (891 to be exact) and importantly, will reveal whether they survived or not, also known as the “ground truth”.

The `test.csv` dataset contains similar information but does not disclose the “ground truth” for each passenger. It’s your job to predict these outcomes.

Using the patterns you find in the `train.csv` data, predict whether the other 418 passengers on board (found in `test.csv`) survived.

# Data Dictionary
|Variable|Definition|Key|
|--------|----------|---|
|Survived|	Survival|	0 = No, 1 = Yes|
|Pclass|	Ticket class|	1 = 1st, 2 = 2nd, 3 = 3rd|
|Sex|	Sex	|
|Age|	Age in years|	
|SibSp	|# of siblings / spouses aboard the Titanic	|
|Parch	|# of parents / children aboard the Titanic	|
|Ticket	|Ticket number	|
|Fare	|Passenger fare	|
|Cabin	|Cabin number	|
|Embarked	|Port of Embarkation|	C = Cherbourg, Q = Queenstown, S = Southampton|

# Goal
It is your job to predict if a passenger survived the sinking of the Titanic or not.
For each in the test set, you must predict a 0 or 1 value for the variable.

# Metric
Metric Your score is the percentage of passengers you correctly predict. This is known as [accuracy](https://en.wikipedia.org/wiki/Accuracy_and_precision#In_binary_classification).

# Procedure
1. **Descriptive Analysis**:
   -  Understand the data by Exploring the data and visualizing it.
   -  Create a wrangle function to clean the data and make it ready for the model.
   -  Keywords: pie charts, bar plots, histograms, box plots, data imbalance, data cleaning, data wrangling, feature engineering, etc.

2. **Diagnostic Analysis**:
   -  Perform a diagnostic analysis to understand the relationship between the features and the target variable.  
   -  Keywords: correlation matrix, scatter plots, pair plots,histogram, etc.  

3. **Predictive Analysis**:
   -  Perform a predictive analysis using different models and select the best model based on the accuracy score.
   -  Keywords: Data transformation, Nested cross-validation, hyperparameter tuning, confusion matrix ,Logistic Regression, Decision Tree, Random Forest, SVM, KNN, etc.
 
 4. **Prescriptive Analysis**:
   -  Provide insights and recommendations on how to improve the model.
   -  Keywords: SHAP, Feature importance, model interpretation, etc.
