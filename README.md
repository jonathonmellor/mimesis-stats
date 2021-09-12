
# `mimesis-stats`

This package exists to extend the capabilities of [mimesis](https://mimesis.readthedocs.io/index.html) for use in statistical data pipelines.

`mimesis` provides _fast_ fake data generation, and comes with a wide range of [data providers, formats, structures and localised options](https://mimesis.readthedocs.io/api.html). In addition, it provides a [schema structure](https://mimesis.readthedocs.io/getting_started.html#schema-and-fields) which makes data generation for data frames very easy. Before using this package it is recommended to become familiar with the basics of `mimesis` fake data generation, such as through this [getting started page](https://mimesis.readthedocs.io/getting_started.html).

Due to the extensibility, custom data providers can be created for use within the framework. This `mimesis_stats` package aims to use the framework for use in statistical pipelines, particularly for generating dummy data for surveys.

However, `mimesis` data generation / providers have two primary limitations this package extension addresses:

* Uni-variable - each data provider method produces a single value. Often in practice there are dependencies and relationships between different variables / columns.
* Limited in statistical properties - `mimesis` draws samples using a uniform distribution. Real distributions are often weighted, or have specific properties (such as a gaussian)

`mimesis_stats` uses a `StatsSchema` object that allows multiple variables related to one another to be created using methods from `Multivariable`.

`mimesis_stats` adds data providers for discrete choice distributions, as well as the ability to pass in custom functions, such as those from `numpy` or `scipy`

# `mimesis-stats` providers

The package contains two supplementary providers, the main object of generating `mimesis` data. One for producing discrete / continuous distributions and the other for dependent multi-variable samples.

## Distribution

Ideal for generating categorical data with `Distribution.discrete_distribution()` or a numerical variable using `Distribution.generic_distribution()` with a user defined or `numpy/scipy` function.

_All_ `mimesis_stats` providers have `null_prop` and `null_value` arguments to add in missing at random null values. For multi-variable producers this is done by passing in a list of propritionas and missing values corresponding to each variable made.

### Categorical

General use for discrete distributions, the main addition from base `mimesis` are the weighting and null options.

```python console
>>> from mimesis_stats.providers.distribution import Distribution
>>> Distribution.distrete_distribution(
... population=["First", "Second", "Third"],
... weights=[0.01, 0.01, 0.98]
... )
"Third"
>>> Distribution.distrete_distribution(
... population=["Apple", "Banana"],
... weights=[0.5, 0.5],
... null_prop=1.0,
... null_value=None
... )
None
```

## MultiVariable

This provider allows multiple variables dependent or related to each other to be created through one provider call.

In practice, produced dictionary key-value pairs can be separated into different variables.

```python console
>>> from mimesis_stats.providers.multivariable import MultiVariable
>>> MultiVariable.dependent_variables(
...     variable_names=["consent", "favourite_fruit"],
...     options=[("Yes", "Lemon"), ("No", None)],
...     weights=[0.7, 0.3]
... )
{"consent": "Yes", "favourit_fruit": "Lemon")
```

Within the possible combinations other provider calls can be made to extend the complexity of generation.

```python console
>>> from mimesis_stats.providers.multivariable import MultiVariable
>>> from mimesis import Food
>>> MultiVariable.dependent_variables(
...     variable_names=["consent", "favourite_fruit"],
...     options=[("Yes", Food.fruit()), ("No", None)],
...     weights=[0.9, 0.1]
... )
{"consent": "Yes", "favourit_fruit": "Banana")
```

# StatsSchema

For generating samples of many variables consistently it is recommended to use a schema. `mimesis` has a `Schema` object, however, in order to fully take advantage of the seeding and multi-variable nature of the `mimesis_stats.providers` approaches `StatsSchema` should be used instead to define a schema.

A `StatsSchema` object requies a `schema` to be passed to it.

A `schema_blueprint` is a `lambda` function that contains the code to generate each variable when called.

To define a `schema_blueprint` a `StatsField` (equivalent to `Field` from `mimesis`) needs to be declared. This sets a seed and a location basis for providers.

The `schema_blueprint` is then passed to the `StatsSchema` to define the generator.

Example `mimesis_stats` schema:

```python console
>>> from mimesis_stats.stats_schema import StatsField, StatsSchema
>>> from numpy.random import pareto
>>> field = StatsField(seed=42)
>>> schema_blueprint = lambda: {
... "name": field("person.full_name"),
... "salary": field("generic_distribution", func=pareto, a=3)
... }
>>> schema = StatsSchema(schema=schema_blueprint)
>>> schema.create(iterations=1)
[{'name': 'Annika Reilly', 'salary': 0.16932036645405568}]
>>> schema.create(iterations=2)
[{'name': 'Hank Day', 'salary': 1.7274682836709054},
{'name': 'Crystle Osborn', 'salary': 0.5510238033601347}]
```

## Working with `pandas`

Standard use of the package will be with a dataframe.

The code snippets below outline the suggested approach for generating a dataframe of random data, such as a survey responses.

Consider the following basic survey.

We collect the following information:

* An ID code identifying each respondant - `"ID"`
* Their email address - `"email"`
* Their occupation - `"occupation"`
* Whether they are a parent or not - `"parent"`
* How important they think schools are when buying a house (out of 10) - `"school_importance"`

The `# fmt: off/on` lines stop the `black` formatter changing the schema blueprint.

```python
import pandas as pd
from mimesis_stats.stats_schema import StatsField, StatsSchema
from scipy.stats import truncnorm

# Define parameters of truncated normal
lower = 0
upper = 10
mu_true = 7
mu_false = 4
sigma = 2.5

field = StatsField(seed=42)

# fmt: off
schema_blueprint = lambda: {
    "ID": field("random.custom_code", mask='SCHL#####', digit="#"),
    "email": field("person.email"),
    "occupation": field("person.occupation"),
    "parent_school_importance": field(
        "dependent_variables",
        variable_names=["parent", "school_importance"],
        options=[
            (True, truncnorm.rvs(a=(lower-mu_true)/sigma, b=(upper-mu_true)/sigma,
                                    loc=mu_true, scale=sigma)),
            (False, truncnorm.rvs(a=(lower-mu_false)/sigma, b=(upper-mu_false)/sigma,
                                    loc=mu_false, scale=sigma))
        ],
        weights=[0.3, 0.7],
    )
}
# fmt: on

schema = StatsSchema(schema_blueprint)

df = pd.DataFrame(schema.create(iterations=1000))
print(df.head())
```
Output:
```s
          ID                       email           occupation  parent  school_importance
0  SCHL60227   pyoses1812@protonmail.com             Milklady   False           8.009516
1  SCHL68040        dreep1871@yandex.com        Choreographer    True           7.193181
2  SCHL25016  killing1844@protonmail.com            Scientist   False           6.773940
3  SCHL52580         brach1847@gmail.com  Leaflet Distributor   False           0.384972
4  SCHL86319     cyrenaic1813@yandex.com         Yacht Master    True           8.585937
```

```python
# Check the summary stats of the two distributions
# (remember mean of sample != mean of generation parameter due to truncation)
parent_breakdown = df.groupby("parent").agg(["min", "max", "median", "mean"])

print(parent_breakdown)
```
Output:
```s
                     min       max    median      mean
parent
False           0.000246  9.839971  4.129702  4.207750
True            0.036771  9.864353  6.670191  6.435121
```
