[![ASR](Images/ASR.png "ASR")](https://github.com/hiroro9/python-ASR.git)

# python-ASR
python scripts for ASR raw data

# 1 input.py

## 1-0 input.csv
    load all csv files
    
    csv => DataFrame

## 1-1 input.strain
    load strain(not temperature) raw data as pandas' DataFrame

    DataFrame => DataFrame


## 1-2 input.dummy
    load dummpy strain data as pandas' DataFrame

    DataFrame => DataFrame


## 1-3 input.temperature
    load temperature data as DataFrame

    DataFrame => DataFrame

## 1-4 input.date
    load date as DataFrame
    
    DataFrame => DataFrame

# 2 manipulation.py

## 2-1 manipulation.offset
    offset strain raw data

    DataFrame => DataFrame


## 2-2 manipulation.dummy_sub
    subtracting dummy strain data

    DataFrame => DataFrame

## 2-3 manipulation.sma
    simple moving averaging strain data

    DataFrame => DataFrame


## 2-4 manipulation.cat_DataFrame
    concatinate strain DataFrame & temperature DataFrame

    DataFrame => DataFrame
   
## 2-5 manipulation.output_csv
    make csv file of strain data

    DataFrame => csv


# 3 plot.py

## 3-1 plot.strain
    plot strain data

    DataFrame => png


## 3-2 plot.each_dirc
    plot each direction of strain 

    DataFrame => png


## 3-3 plot.dummy
    plot dummy data 

    DataFrame => png

