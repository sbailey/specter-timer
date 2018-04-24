# specter-timer

A timing benchmark wrapper for spectral extractions using
https://github.com/desihub/specter .

Stephen Bailey<br/>
Lawrence Berkeley National Lab<br/>
April 2018

## Installation and running

Starting with an Anaconda python distribution:
```
conda create --yes -n specter-timer python=3.6 scipy numpy astropy numba
source activate specter-timer
pip install git+https://github.com/desihub/specter.git@0.8.4#egg=specter
git clone https://github.com/sbailey/specter-timer
cd specter-timer
python specter-timer.py --nproc 32
```

## Example results

On NERSC Cori Haswell with 32 cores:
```
$> python specter-timer.py --nproc 32
Tue Apr 24 15:00:29 2018 Reading input data
Tue Apr 24 15:00:32 2018 Splitting data into subregions
Tue Apr 24 15:00:36 2018 Extracting spectra in 220 subregions
I/O time: 3.0 sec
Prep time: 3.8 sec
Extraction time: 202.3 sec
Total time: 209.0 sec
```
