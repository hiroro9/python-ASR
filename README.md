# python-ASR
python scripts for ASR raw data

1 input.py

1-0 input.csv
    load all csv files
    
    csv => DataFrame

1-1 input.strain
    load strain(not temperature) raw data as pandas' DataFrame

    DataFrame => DataFrame


1-2 input.dummy
    load dummpy strain data as pandas' DataFrame

    DataFrame => DataFrame


1-3 input.temperature
    load temperature data as DataFrame

    DataFrame => DataFrame

1-4 input.date
    load date as DataFrame
    
    DataFrame => DataFrame


2 offset.py
  offset strain raw data

  DataFrame => DataFrame


3 dummy_sub.py
  subtracting dummy strain data

  DataFrame => DataFrame

4 sma.py
  simple moving averaging strain data

  DataFrame => DataFrame


5 cat_strain_temp.py
  concatinate strain DataFrame & temperature DataFrame

  DataFrame => DataFrame


6 output_csv.py
  make csv file of strain data

  DataFrame => csv


7 plot.py

7-1 plot.strain
  plot strain data

  DataFrame => png


7-2 plot.each_dirc
  plot each direction of strain 

  DataFrame => png


7-3 plot.dummpy
  plot dummy data 

  DataFrame => png

