# HI!CKATHON 2023

<img src="images/logo-hi-paris-retina.png" alt="Hi! Paris logo" width="500"/>

GROUP NAME  : Group 14

Date : January 14th, 2023

# I.	OVERVIEW
## 1.	Project Background and Description

Nowadays, while real estate greatly contributes to GHG emissions, investments in 
insulation works are still far behind their objectives.

The purpose of the project is to use Machine Learning to predict energy consumption 
of buildings. A better understanding of the importance of insulation works on the 
energy consumption of buildings will enhance energy transition investments.

## 2.	Project Scope

The project scope will include the Machine Learning regression task 
and the business pitch.

Therefore, on a technical standpoint, the project will aim to preprocess the data 
to facilitate learning, designing and training a model capable of 
predicting the target values.

On a business standpoint, the project will also aim to prepare a business pitch 
that leverages said ML model and that estimate energy and cost savings.

However, while a proper ML pipeline will be designed using Python libraries, 
the said application will not be developed during the Hackathon.

The repository containing the code for preprocessing, training and inference 
will be uploaded on Gitlab, alongside this document.

## 3.	Presentation of the group

| First name | Last name | Year of studies & Profile | School        | Skills                         | Roles/Tasks                         |
| ---------- | --------- |--------------------|---------------|--------------------------------|-------------------------------------|
| Agathe     | MINARO    | Master 2 ENSAE     | ENSAE         | Data Science                   | Modeling, Training                  |
| Guillaume     | PHILIPPE    | Master 2 Data Science | IP Paris      | Data Science, Computer Science | Training, Testing                   |
| Huu Tan     | MAI    | Master 2 Telecom Paris | Telecom Paris | Data Engineering/Science       | Preprocessing, Refactoring, Writing |
| Max Cameron     | WU    | Master 2 Data Science | IP Paris      | Data Science                   | Feature Engineering, Finetuning     |
| Yassine     | HARGANE    | Master 2 HEC Paris | HEC Paris     | Business Engineering           | Business                            |


## 4.	Task Management

The team set a meeting every morning to discuss the progress and the next steps.
Regarding the code, we use a git repository for version control and collaborative working. 

On the first day, most of the team effort was directed towards preprocessing. 
Max and Tan worked on feature engineering and the whole team contributed to 
preprocessing. Tan further refactored the preprocessing pipeline and 
Guillaume made the exploratory data analysis and wrote a 
script to easily train and compare models. Yassine started working on the business pitch.

On the second day, Agathe and Max continued to train and fine-tune models. Tan and Guillaume
worked on the report. Afterwards, the whole team worked on the business pitch.

# II.	PROJECT MANAGEMENT
## 1.	Data Understanding

At the start of the challenge, the team spent time on the exploratory data analysis (EDA).

We noticed that the quality of the data was not optimal. For instance, some features 
were missing for a large number of observations, and some continuous features 
contain outliers. Regarding categorical features, some of them were poorly encoded.

Following this analysis, we agreed that the preprocessing step will be very 
important for the quality of the predictive model. 

## 2.	Data Preprocessing

A lot of time and effort was put in data preprocessing.

Many problems were encountered because of inconsistencies in `sklearn` libraries 
that did not allow us to recover the feature names after the column transformations in pipelines.
As our team have not had time to edit the `sklearn` classes and to fix the inconsistencies, 
we decided to manually edit the datasets in order to engineer the features 
outside of pipelines.

The training data was truncated so to remove the outliers and to include more samples
that represent the majority of the data. The test data was not truncated.

Likewise, since our group emphasized interpretability for our model, we refrained from using dimensionality reduction methods such as PCA.

## 3.	Modeling Development

To preface this section, we would like to emphasize that we completely excluded models with
little interpretability such as neural networks. Hence, our group prioritized models that allow us to
visualize features importance, such as linear models or forest models.

We started by training a linear model, a decision tree and a random forest as baselines. We finally decided to opt for
a XGBoost model, which is a forest model with gradient boosting that is known to perform well on tabular data.

We then fine-tuned the model by performing a grid search on the hyperparameters. We also used a cross-validation to
evaluate the quality of the model. The metric used to evaluate the model is the explained variance score.

## 4.	 Deployment Strategy

In the pre-inference time, the data will be preprocessed using our 
unique pipeline and the model will be loaded.

We plan to deploy the AI solution as Software as a Service (SaaS) on a cloud platform. 
This will allow us to easily scale the solution and to make it available to a large number of users.
We could deploy it both as an API, to permit users to easily request the service 
, and also as a platform with an user-friendly interface.  

Since the model is explainable, the user could also view the most important 
features that contribute to the energy consumption of their buildings.

The AI solution can be used either by private and public companies or private individuals.

Furthermore, in the case where we could receive new data, we could retrain the model to keep it up to date.

# III.	CARBON FOOTPRINT LIMITATION

The group has tried to limit the models to strictly classic Machine Learning approaches (no Deep Learning approach) and to work with relatively lightweight models whenever possible.

Energy consumption of GPUs is notoriously high. Therefore, we decided against using GPUs for training our models.
Moreover, we shortened the training time by using a smaller yet better dataset.

We also slept and ate locally :)

# IV.	CONCLUSION

During this intense 48 hours, we have been able to develop a model that is 
able to predict the energy consumption of buildings with a good explained variance. 

We have also been able to prepare a business pitch that leverages the model to 
estimate energy and cost savings. We have focused on performance and 
explainability to enable our future customers to anticipate, identify and 
solve their problems.