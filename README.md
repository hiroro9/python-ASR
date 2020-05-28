# python-ASR
python scripts for ASR raw data


1.input_strain.py
  load strain(not temperature) raw data as pandas' DataFrame

  normal_strain.csv => DataFrame


2.input_dummy.py
  load dummpy strain data as pandas' DataFrame

  normal_strain.csv => DataFrame


3.input_temperature.py
  load temperature data as DataFrame

  normal_strain.csv => DataFrame


4.offset.py
  offset strain raw data

  DataFrame => DataFrame


5.dummy_sub.py
  subtracting dummy strain data

  DataFrame => DataFrame


6.cat_strain_temp.py
  concatinate strain DataFrame & temperature DataFrame

  DataFrame => DataFrame


7.output_csv.py
  make csv file of strain data

  DataFrame => csv


8.plot.py
  plot strain data

  DataFrame => png


9.plot_each_dirc.py
  plot each direction of strain 

  DataFrame => png


10.plot_dummpy.py
  plot dummy data 

  DataFrame => png

