# Welcome to my Quantitative Finance Playground!

### Overview
This repository serves as a hub for listing my articles and experiments. I primarly focus on Quantitative Finance and Machine Learning.

I am currently studying Hasbrouck’s *Empirical Market Microstructure*, an interesting technical introduction on market making.

### About Me
Starting with a background in Physics and spending six years in finance, I've currently found my groove as a Quant.

When I'm not crunching numbers, I'm absorbed in the pages of a book or tending to my garden.

## Articles
Below are my articles, sorted by their most recent publication dates. Where applicable, I will provide links to Python notebooks containing the plots and computations used in each piece.



- [**When should an investor prefer a Market Order over a Limit Order?**](https://medium.com/@lu.battistoni/when-should-an-investor-prefer-a-market-order-over-a-limit-order-593bc0fd6dd9)
  
   -- August 2024 --
  
  [Notebook](https://github.com/Peropero0/quantitative_finance_playground/blob/main/notebooks/Hasbrouck_Market_Microstructure/order_book_simulations/experiment_1_CMSW_framework.ipynb)

  *As I am finishing my journey through Hasbrouck’s Empirical Market Microstructure, I would like to talk about an interesting model that he describes in chapter 12. This model, called CMSW by the initials of its inventors, focuses on one fundamental question: When should an investor prefer a Market Order over a Limit Order? In this article, I will illustrate the assumptions of the model and the reasoning behind it. Moreover, I will use the framework built in one of my previous articles to run some simulations and test some theories.*



- [**An Order Book simulator in Python**](https://medium.com/@lu.battistoni/an-order-book-simulator-in-python-b7b59ec82258)
  
   -- July 2024 --
  
  [Folder](https://github.com/Peropero0/quantitative_finance_playground/tree/main/notebooks/Hasbrouck_Market_Microstructure/order_book_simulations)

  *While I was studying the theory regarding market microstructure, I had the urge to run some practical experiments. Getting quality data about the Order Book is not an easy task for an individual: data can be really expensive, it contains a lot of information and has a huge size. These two issues motivated me to build a fast and reliable framework in which you can run experiments. This framework is highly customizable and will allow you to make your own hypothesis about the Traders, Market Makers and the general behavior of the Order Book, in order to develop algorithmic trading strategies. In this article, I will explain to you how to use the framework, what are its limitations and what you can do to improve it. In the next months, I will implement new features to overcome the limitations of the very first building blocks that I am proposing you. Moreover, I will myself run experiments using this framework, getting inspiration from books and papers.*


- [**A brilliant way to represent the Order Flow in Python**](https://medium.com/@lu.battistoni/a-brilliant-way-to-represent-the-order-flow-in-python-fb96318e1070)
  
   -- July 2024 --
  
  [Notebook](https://github.com/Peropero0/quantitative_finance_playground/blob/main/notebooks/Hasbrouck_Market_Microstructure/order_book_simulations/order_flow_representation.ipynb)

  *In this article I will show you an insightful way to plot the Order Flow in Python. I learned about this method while reading Algorithmic and High-Frequency Trading, Álvaro Cartea (2015) and I was immediately fascinated by it. This representation provides an intuitive description of the evolution of the Order Book and of the change in price.*

- [**Exploratory Data Analysis in Python**](https://medium.com/@lu.battistoni/exploratory-data-analysis-in-python-6a41a7505f5b)
  
   -- June 2024 --
  
  [Notebooks](https://github.com/Peropero0/quantitative_finance_playground/tree/main/notebooks/finance_notebooks/temperature_analysis)

  *When working with new datasets, one of the initial steps is to familiarize yourself with the data. This involves thoroughly understanding the contents and characteristics of the new information you are handling. This process is called Exploratory Data Analysis (EDA) and can highlight serious problems with data. When feeding data into machine learning algorithms, you want to avoid some specific problems. In this article I will download a dataset for US Temperatures and I will point out some of these relevant problems. In particular, I will solve a seasonality and non-stationarity problem and I will underline a non-point-in-timeness issue.*

- [**Understanding Futures contract specifications**](https://medium.com/@lu.battistoni/understanding-futures-contract-specifications-c8be50844acd)
  
   -- June 2024 --

  *Navigating the vast world of financial Futures can be overwhelming: there are a lot of concepts to understand and not grasping something could lead to huge potential losses. In this article, I would like to show you some example of how to read the specifications of Futures contracts, discuss what tick size and lot size are and in general clarify some details that I struggled with in my early days of Futures trading.*

- [**8 Options Trading rules to be successful**](https://medium.com/@lu.battistoni/8-options-trading-rules-to-be-successful-5418f469137f)
  
   -- May 2024 --

  *I recently started reading George Kleinman’s book about Futures and Options trading and I was fascinated by his writing style and how clearly he explains complex concepts.
  In this article I want to share with you a passage about Options trading and what to do and to avoid in Mr. Kleinman’s opinion, based on his vast trading experience.*


- [**Understanding Pandas MultiIndex in Finance**](https://medium.com/@lu.battistoni/understanding-pandas-multiindex-in-finance-cdfdda16f792)
  
   -- May 2024 --

  [Notebook](https://github.com/Peropero0/quantitative_finance_playground/blob/main/notebooks/general_python_tutorials/multiindexing_tutorial.ipynb)

  *Pandas is just a great Python library for Quantitative Finance and Data Science in general. It allows you to easily manipulate data and in particular timeseries. Something that new users usually struggle with is using Pandas MultiIndexes effectively. A deep understanding of basic functions like groupby, stack and resample is crucial in your journey to becoming a Pandas pro! In this article I will show you some examples to clarify how to use MultiIndexing together with the functions mentioned above.*


- [**Backtesting a systematic trading strategy in Python**](https://medium.com/@lu.battistoni/backtesting-a-systematic-trading-strategy-in-python-e08263e888ab)
  
   -- May 2024 --

  [Notebook](https://github.com/Peropero0/quantitative_finance_playground/blob/main/notebooks/simple_vectorial_backtest/simple_vectorial_backtest.ipynb)

  *In quantitative finance, and algorithmic trading in general, it’s crucial to test your ideas in the past to have a guess of how they could perform in the future. In this article, I will help you build a fast vectorial backtest in Python that can easily be customised for any of your need.*

- [**Distribution of the Order Flow in Python**](https://medium.com/technological-singularity/distribution-of-the-order-flow-in-python-d7ba059dbf13)
  
   -- Apr 2024 --

  [Notebook](https://github.com/Peropero0/quantitative_finance_playground/blob/main/notebooks/Hasbrouck_Market_Microstructure/sequential_trade_model_part_3.ipynb)

  *In this article, instead of focusing on the spread, we will illustrate the probability distribution of the volume of buy and sell orders. To this aim, we will first study the probability of having b buys given n trades under a Binomial distribution, then the probability of having b buys and s sells during a trading day under a Poisson distribution. This will allow us to estimate the fraction of informed agents in the market μ.*


- [**Sequential Trade Model for Asymmetrical Information — Part 2**](https://medium.com/technological-singularity/sequential-trade-model-for-asymmetrical-information-part-2-74ce13070bdd)

  -- Apr 2024 --

  *In this piece, I’ll extend my exploration into the Sequential Trade Model proposed by Hasbrouck in Chapter 5 of Empirical Market Microstructure. Moreover, I will solve the suggested exercises, offering my insights and discussing potential further developments.*

  

- [**Sequential Trade Model for Asymmetrical Information**](https://medium.com/@lu.battistoni/sequential-trade-model-for-asymmetrical-information-54245268f802)
  
  -- Apr 2024 --

  [Notebook 1](https://github.com/Peropero0/quantitative_finance_playground/blob/main/notebooks/Hasbrouck_Market_Microstructure/sequential_trade_model.ipynb)

  [Notebook 2](https://github.com/Peropero0/quantitative_finance_playground/blob/main/notebooks/Hasbrouck_Market_Microstructure/sequential_trade_model_part_2.ipynb)

  *In this piece, I will further explore the Bid-Ask spread dynamics by assuming that the market is populated by two types of agents with two different sets of information: fully informed and completely uninformed traders. Fully informed traders already know the security’s end-of-day value, while uninformed traders don’t. To address this scenario, I will use a specific case of Glosten and Milgrom model, to analyse how different levels of information among market participants influence overall market activity and define trading strategies.*


- [**Relaxing Linear Regression assumptions — A Roll model application**](https://medium.com/@lu.battistoni/relaxing-linear-regression-assumptions-a-roll-model-application-59e310dde6ce)

   -- Mar 2024 --

  [Notebook](https://github.com/Peropero0/quantitative_finance_playground/blob/main/notebooks/Hasbrouck_Market_Microstructure/roll_model_relaxing_of_assumptions.ipynb)
    
  In the world of quantitative finance and data science, linear regression is widely used to explore the relation between variables. Being a simple and powerful tool, it’s easy to fall into the pitfall of using it without testing its basic assumptions. In this article, I will use the Exercises 4.2 and 4.3 of Hasbrouck’s Empirical Market Microstructure to show how violation of linear regression assumptions can impact parameter estimation of a Roll model. 


- [**The Roll Model Under Serial Dependence**](https://python.plainenglish.io/roll-model-under-serial-dependence-f9ba693446f9)

  -- Feb 2024 --

  [Notebook](https://github.com/Peropero0/quantitative_finance_playground/blob/main/notebooks/Hasbrouck_Market_Microstructure/roll_model_serial_dependence.ipynb)
  
  While approaching to univariate timeseries analysis, one could struggle with applying the mathematical theory to simple practical cases. In this article, I will use the Excercise 4.1 of Hasbrouck’s Empirical Market Microstructure to study the dynamics of an autoregressive toy model.




## Feedback and Contacts
Your feedback is important! If you have any questions, suggestions, or feedback, please don't hesitate to reach out to me via [**LinkedIn**](https://www.linkedin.com/in/luigi-battistoni/).




