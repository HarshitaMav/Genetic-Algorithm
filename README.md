# Genetic-Algorithm

This project shows the application of genetic algorithm. Here genetic algorithm one of the optimization technique is used for selecting features from the dataset that can be further used for rule generation. This project generates rules for four datasets from Healthcare domain. 

## Datasets :

Data used here is numeric as genetic algorithm works on Numeric Data only.
List of datasets are as below : 
* [Diabetes](https://github.com/HarshitaMav/Genetic-Algorithm/blob/main/data/diabetes.csv)
* [Mental Health](https://github.com/HarshitaMav/Genetic-Algorithm/blob/main/data/mental.csv)
* [Heartfailure](https://github.com/HarshitaMav/Genetic-Algorithm/blob/main/data/heartfailure.csv)
* [Strokedata](https://github.com/HarshitaMav/Genetic-Algorithm/blob/main/data/strokedata.csv)

## Working :
1. For rule generation, first step is to run [rule.py](https://github.com/HarshitaMav/Genetic-Algorithm/blob/main/Notebooks/rule.py) which have various functions that will help in rule generation.
2. [rule_extraction.py](https://github.com/HarshitaMav/Genetic-Algorithm/blob/main/Notebooks/rule_extraction.py) file is executed.
3. Juypter notebook is created for individual topic from the above datasets.
4. Run individual notebooks.

## Notebooks :

These notebooks contains functions for genetic algorithm which helps in feature selection from the dataset and using the columns obtained in the results after optimization are used for generating rules. This rules are generated from the .py files executed in the start. Links to the notebook:
1. [Diabetes](https://github.com/HarshitaMav/Genetic-Algorithm/blob/main/Notebooks/diabetes_final.ipynb)
2. [Mental Health](https://github.com/HarshitaMav/Genetic-Algorithm/blob/main/Notebooks/mental_final.ipynb)
3. [Heartfailure](https://github.com/HarshitaMav/Genetic-Algorithm/blob/main/Notebooks/heartfailure_final.ipynb)
4. [Strokedata](https://github.com/HarshitaMav/Genetic-Algorithm/blob/main/Notebooks/strokedata_final.ipynb)

## Results :

After execution of the above notebooks various rules are generated using Random Forest Classifier keeping depth = 4. Out of all this rules we select rules having age as primary parameters as that is the only common factor present in every dataset. This helps in easy comparison of rules for urther usage. These rules with age as their parameter are individually stored in [rules generated](https://github.com/HarshitaMav/Genetic-Algorithm/tree/main/rules%20generated) folder.

## Accuracy Chart from all the generations(Total generation = 6):
1. Diabetes :

![image](https://user-images.githubusercontent.com/51914662/146673876-18c54569-2dc5-4e47-af6a-93cad735b748.png)

2. Mental Health :

![image](https://user-images.githubusercontent.com/51914662/146673820-d1bd17ea-3fa1-47fe-bc04-74fff8193a5f.png)

3. Heart Failure :

![image](https://user-images.githubusercontent.com/51914662/146674176-63be18de-aa9e-4426-9f68-84a870451c4d.png)

4. Strokedata :

![image](https://user-images.githubusercontent.com/51914662/146673889-3138a90e-febb-4c0b-ac06-16dbda82665a.png)
