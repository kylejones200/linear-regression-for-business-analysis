# Linear Regression for Business Analysis Linear regression analysis estimates the relationship between a
dependent variable and one or more independent variables using a
best-fit...

### Linear Regression for Business Analysis
Linear regression analysis estimates the relationship between a
dependent variable and one or more independent variables using a
best-fit line. The simplest form models the mean value of the dependent
variable based on the value of an independent variable.

The *Independent* variable does not change by the other variables that
you are trying to measure.\
The *Dependent* variable is subject to change based on other factors.

#### Correlation and Regression
Correlation and regression are related concepts. Correlation measures
the relationship between two variables. It can be represented by ordered
pairs. The X variable is the independent variable and the Y variable is
the dependent variable.


Correlation measures how closely two variables are related (a
relationship). To see how close these variables are, we work out a
correlation coefficient. We would use a test like Spearman's rho (or
Pearson's r) to help us find this score.

- positive values mean that as X increases, Y also increases
- negative values mean that as X increases, Y decreases
- the value 0 means there is no linear correlation so a change in X has
  no effect on the value of Y

Correlation is symmetric: it doesn't matter what variable is called X
and what is called Y: \`Corr(X,Y) = Corr(Y,X)\`. Correlation always
falls between −1 and 1. If r=1 (or r=−1) there is a perfect positive (or
negative) LINEAR relationship between X and Y. If r=0, there is no
LINEAR relationship between X and Y but there could be another type of
relationship (example: quadratic).

The strength of correlation is measured by r (rho), the absolute value
of the correlation. For example, a correlation of −0.75 is stronger than
a correlation of 0.30 because \|−0.75\|=0.75, which is \> 0.30.

In real-world data, we usually gather data on several variables for each
observational unit. For example, if we are studying CEO salaries, we
might send a survey to a random sample of CEOs in the US asking them to
also report age, years with the company, company sales and profits, etc.
Then, we are interested in investigating relationships between
variables. There are infinitely many possible relationships.

Usually, we care most about how much of a linear relationship they have
because more complex relationships can often be captured "locally" by
straight lines.

#### Computing the Linear Regression Equation
The equation for a simple linear regression line takes the form: y' =
a + bx\
Where:\
y' is the predicted value of the dependent variable\
x is the independent variable\
a is the y-intercept \
b is the slope

To calculate a and b from a dataset:

1\. Create a table with the x and y values and the summation columns Σx,
Σy, Σxy, Σx², Σy²

2\. Calculate a using: a = (Σy\*Σx² --- Σx\*Σxy) / (n\*Σx² --- (Σx)²)

3\. Calculate b using: b = (n\*Σxy --- Σx\*Σy) / (n\*Σx² --- (Σx)²)

4\. Substitute the values of a and b into y' = a + bx to get the
regression line equation

The slope (b) represents how much the dependent variable changes for a
one unit increase in the independent variable.

For more complex regression models with multiple independent variables,
the calculations are extended but follow the same principles.

#### Example using property data from AirBNB
This is an example looking at the nightly price for an Airbnb property
based on the number of beds the property has. Our basic idea would be
that as the number of beds in a property increases, be cost of the
propery will increase.


<figcaption>Source: Author using AirBNB data and visualized
using Plotly.</figcaption>


The data supports our idea that as the number of goes up, the price also
goes up. But we also can separate the data based on the type of propery.
Here I'm only using two property types: House or Not House. The blue
line in the graph shows the linear regression for a house. As we might
expect, the average price of a house is higher than a Non-house when the
number of beds is low. But there is an inflection point where the
Non-house price is higher than the house price after we reach 7 beds.

As you can see from the histograms, our dataset does not have many
properties with 7, 8 or 9 beds. So we should approach this analsyis with
caution.

We might also conclude that Non-house properties with 7+ beds are
unusual in other ways. Maybe they are specialty properties which command
a higher price not because of the number of beds, per se, be because of
other reasons. After all, there aren't many 9 bedroom apartments that
are just available on the market.

### Video example
This is a video example walking through using the AirBNB data and
building several linear regressions.


<h1 id="an-error-occurred." class="message">An error occurred.</h1>

Unable to execute JavaScript.

### Related Stories
- [[Getting to know Pandas for data analytics with
  Python](https://medium.com/@kylejones_47003/getting-to-know-pandas-for-data-analytics-with-python-7386da28dd33)]
- [[Basic Data Analysis using Pandas Library in
  Python](https://medium.com/@kylejones_47003/basic-data-analysis-using-pandas-library-61ed815b834a)]
- [[Introduction to Statistics for people who do Business
  Analytics](https://medium.com/@kylejones_47003/introduction-to-statistics-for-people-who-do-business-analytics-26878760a14a)]
::::::::By [Kyle Jones](https://medium.com/@kyle-t-jones) on
[April 20, 2024](https://medium.com/p/2407d9fe2942).

[Canonical
link](https://medium.com/@kyle-t-jones/linear-regression-for-business-analysis-2407d9fe2942)

Exported from [Medium](https://medium.com) on November 10, 2025.
