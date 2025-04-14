import pandas as pn 
import os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import re
from scipy.stats import spearmanr
import seaborn as sns
import matplotlib.pyplot as plt

import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kruskal
import scikit_posthocs as sp


currentDir= os.path.dirname(__file__)

data_text = f"{currentDir}/data.xlsx" 

print(data_text)


cheat_question_text = 'During a diet, how often do you have a  "cheat meal" or "cheat day"?'
age_group_text = "What age group are you in?"
difficulty_finding_text = "How easy is it to locate specific products in an unfamiliar shop"
shopping_experience_text = "Do you enjoy the shopping 'experience'"
budget_shop_text = "Do you have a budget when you shop groceries?"
chore_shop_text = "Do you consider shopping to be a chore?"

def turnNumber(string):

    exp = re.compile("([0-9]{2}).*([0-9]{2})")
    res = re.finditer(exp,string)
    if res is not None:
        for idx, match in enumerate(res, 1):

            grp1 = match.group(1)
            grp2 = match.group(2)

            res = (int(grp2)+int(grp1))/2
            return res


def mealPlanNum(string):

    match(string):
        case "Always":
            return 3
        case "Sometimes":
            return 2
        case "Never":
            return 3
        
        case _:
            return 10000


def giveMeanAge(X):
    integer_version = []

    for a in range(X.shape[0]):
        res = turnNumber(X.iloc[a,0])
        integer_version.append(res)

    integer_vers_np = np.array(integer_version)

    return integer_vers_np


def ageChart(age_column):
    age_group =  age_column.groupby(age_column["What age group are you in?"]).size()

    print(age_group)
    unique_agecolumn = age_column["What age group are you in?"].unique()
    chart = plt.bar(unique_agecolumn,list(age_group))
    
    plt.show() 

    return age_group
def difficultyWithAgeGroup(original_data,age_group_text):
    original_data.groupby(age_group_text)[shopping_experience_text].median().reset_index()
    
    print(original_data)
    sns.boxplot(x=age_group_text, y=difficulty_finding_text, data=original_data)
    plt.title("Difficulty Finding Unfamiliar Items by Age Group")
    plt.show()


def enjoyShoppingExperience_withBUSY():
    pass

def countBudgetbyAge(original_data, age_column):
    filtered_df = original_data[original_data["Do you have a budget when you shop groceries?"].isin(["Yes", "Occasionally"])]
    
    groupByFull = original_data.groupby(age_column["What age group are you in?"])["Do you have a budget when you shop groceries?"].count().reset_index()

    people_who_yes = filtered_df.groupby(age_column["What age group are you in?"])["Do you have a budget when you shop groceries?"].count().reset_index()


    print(groupByFull)
    print(people_who_yes)
    pn.merge(people_who_yes, groupByFull[["What age group are you in?", "Do you have a budget when you shop groceries?"]], on=["What age group are you in?"])




    people_who_yes["percentage"] = (people_who_yes["Do you have a budget when you shop groceries?"] / groupByFull["Do you have a budget when you shop groceries?"])

    print(people_who_yes)


def shoppingEXPwithChore(original_data):

    original_data[chore_shop_text] = original_data[chore_shop_text].map({'No': 0, 'Yes': 1})

# Independent variable
    X = original_data[[shopping_experience_text]]
    X = sm.add_constant(X)  # Add intercept

    # Dependent variable
    y = original_data[chore_shop_text]

    logit_model = sm.Logit(y, X)
    result = logit_model.fit()

# Print summary
    print(result.summary())

    logit_model = sm.Logit(y, X)
    result = logit_model.fit()
    
    # Generate X values for prediction (e.g., a range covering your data)
    X_range = np.linspace(X[shopping_experience_text].min(), X[shopping_experience_text].max(), 100)
    X_pred = sm.add_constant(X_range)  # Add intercept term
    
    # Predict probabilities
    y_pred = result.predict(X_pred)
    
    # Plot
    plt.figure(figsize=(8, 5))
    plt.scatter(X[shopping_experience_text], y, alpha=0.5, label="Actual Data")  # Scatter plot of actual data
    plt.plot(X_range, y_pred, color='red', label="Logistic Curve")  # Logistic regression curve
    plt.xlabel("Shopping Experience Score")  # Adjust label based on what this represents
    plt.ylabel("Chore Shopping (0=No, 1=Yes)")
    plt.title("Logistic Regression Model")
    plt.legend()
    plt.show()


def shoppingEXPmean(shopping_experience_column):

    average_enjoyment_shopping = shopping_experience_column.mean()


    

    print("Shopping Experience Mean : " + str(average_enjoyment_shopping))
def cheatingWithFamiliarity():
    pass

def main():
    with open(data_text, "rb") as data:
        original_data = pn.read_excel(data)
        print(original_data)
        print(original_data.columns)
    
    
        # QUESTIONS into pandas columns
        
        shopping_experience_column=original_data.loc[:,[shopping_experience_text]] 
        age_column = original_data.loc[:,[age_group_text]]
    
    
        budget_when_shop_column = original_data[budget_shop_text]
    
        shopping_chore_column = original_data.loc[:, [chore_shop_text]]
    
    
        supermarket_saving_column = original_data["Do you use any supermarket-saver or discount apps?"]
        meal_plan_column = original_data.loc[:,["Do you meal plan? (Planning future meals?)"]]
    
        important_nutritional_information_see_column = original_data["How important is it for you to see detailed nutritional information before you purchase a product?"]
    
    
        interested_see_alternative_column = original_data["Would you be interested in seeing the alternative ingredients you can use for a given recipe"]
    
    
        regularly_seeing_purchases_column = original_data["Would seeing your regular purchases be important to you?"]
    
        cheating_days_column = original_data[[cheat_question_text]]
    
        
        how_easy_unfamiliar_column = original_data[difficulty_finding_text]
    
        # Whether they want to be positively rewarded for contributing for steward goals
        rewarded_positively_column = original_data["Would you like to be rewarded for positively contributing against food-waste / low CO2 / other steward goals"]
    
    
    
        allergies_or_dietary_req = original_data["Do you have any allergies or dietary requirements"]
        
    
        # Convert meal plan which is in textual format into numerical format
    
        mealplan_arr = []
    
        for a in range(meal_plan_column.shape[0]):
    
            # This converts each textual representation into a number 
            mealplan_arr.append(mealPlanNum(meal_plan_column.iloc[a,0]))
        
    
        # Find mean age of meal planners
    
        mean_age_arr = giveMeanAge(age_column)
        mean_age_pd = pn.DataFrame(data=mean_age_arr, columns=["age"])
        
        mealplan_pd = pn.DataFrame(data=mealplan_arr, columns=["meal_freq"])
        print(mean_age_pd)
    
        
        
    
    # Meal Planning related
        X = mean_age_pd[['age']]  # Predictor variable (age)
        y = mealplan_pd  # Outcome variable (response: daily = 0, weekly = 1, monthly = 2)
    
    # Standardize the predictor
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
       
    
    
        # Fit multinomial logistic regression
        model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
        model.fit(X_scaled, age_column)
    
        print("Model Coefficients:", str(model.coef_))
    
        model = OrderedModel(y, mean_age_pd, distr="probit")
        res = model.fit(method="bfgs")
    
        print(res.summary())
    
    
        sns.boxplot(x=mealplan_pd['meal_freq'], y=mean_age_pd['age'])
        plt.xlabel("Meal Planning Frequency")
        plt.ylabel("Age")
        plt.title("Age vs. Meal Planning Frequency")
        plt.show()
    
        correlation, p_value = spearmanr(mean_age_pd['age'], mealplan_pd['meal_freq'])
        print(f"Spearman correlation: {correlation}, p-value: {p_value}")
    
    
    #### FINISHED MEAL Planning
    
        # amount of people per age
        ageChart(age_column)
    
        # shopping experience box-plot
    
        shoppingBarChart = original_data.groupby(original_data[age_group_text])[shopping_experience_text]
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=original_data[age_group_text], y=original_data[shopping_experience_text])
        
        # Labels and title
        plt.xlabel("Age Group")
        plt.ylabel("Shopping Experience")
        plt.title("Shopping Experience Distribution Across Age Groups")
        plt.xticks(rotation=45)  # Rotate x-axis labels if needed
    
    # Show the plot
        plt.show()
        print("SHOPPING BAR CHART")
        print(shoppingBarChart)
        # percentage wise of different age groups having a budget when shopping
    
        countBudgetbyAge(original_data, age_column)
    
    
        #shopping experience mean
        shoppingEXPmean(shopping_experience_column)
        
    
        # Cheating days associated with difficulty finding items
    
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(cheating_days_column)
    
    
        model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
        model.fit(X_scaled, how_easy_unfamiliar_column)
    
        corr, p_value = spearmanr(cheating_days_column, how_easy_unfamiliar_column)
        
        print(f"Spearman Correlation: {corr}, P-value: {p_value}")
    
    
        sns.regplot(x=cheating_days_column, y=how_easy_unfamiliar_column, lowess=True, scatter_kws={"alpha": 0.5})
        plt.xlabel("Cheating Occurences")
        plt.ylabel("Familiarity in Shop")
        plt.title("Cheating Occurences vs Familiarity in Shop (Spearman: -0.28)")
        plt.show()
    
    
        
    
        # PERCENTAGE OF PEOPLE WHO HAVE A BUDGET WHEN SHOPPING
        
        filtered_df = original_data[original_data["Do you have a budget when you shop groceries?"].isin(["Yes", "Occasionally"])]
    
        print("Percentage of people who have a budget when shopping groceries")
        print(filtered_df.size/original_data.size)
    
    
    
    
        # DEVIATION FINDING OF AGE GROUP WITH CHEATING (IS THERE A DIFFERENCE BETWEEN AGE GROUP?)
    
        groups = [group[cheat_question_text].dropna() for _, group in original_data.groupby("What age group are you in?")]
    
    
        h_stat, p_value = kruskal(*groups)
    
        print(f"Kruskal-Wallis H-statistic: {h_stat}, P-value: {p_value}")
    
    
        dunn_test = sp.posthoc_dunn(original_data, val_col=cheat_question_text, group_col=age_group_text, p_adjust='bonferroni')
        print(dunn_test)
    
        dunn_test = sp.posthoc_dunn(original_data, val_col=shopping_experience_text, group_col=age_group_text, p_adjust='bonferroni')
        print(dunn_test)
    
    
        # difficulty finding items in relation to age group
        difficultyWithAgeGroup(original_data, age_group_text)
    
    
        # shopping experience with difficulty finding items (reg)
    
    
    
    
    
    
    
        order=[1,2,3,4,5]
    
       # Convert to ordered categorical variables  
        original_data[shopping_experience_text] = pn.Categorical(original_data[shopping_experience_text], categories=order, ordered=True)  
        original_data[difficulty_finding_text] = pn.Categorical(original_data[difficulty_finding_text], categories=order, ordered=True)  
        
        # Convert to numeric codes  
        original_data[shopping_experience_text] = original_data[shopping_experience_text].cat.codes  
        original_data[difficulty_finding_text] = original_data[difficulty_finding_text].cat.codes  
        
        # Fit the Ordered Logit Model  
        model = OrderedModel(original_data[difficulty_finding_text],  
                             original_data[[shopping_experience_text]],  
                             distr="logit")  
        
        result = model.fit(method="bfgs")  
        print(result.summary())  
    
        rho, p_value = spearmanr(original_data[shopping_experience_text], original_data[difficulty_finding_text])
        print(f"Spearman's correlation: {rho}, p-value: {p_value}")
    
        # Shopping associated with chore
    
        shoppingEXPwithChore(original_data)


main()
