Usage
=====

.. _installation:

Installation
------------

To use MedX, first install it using pip:

.. code-block:: console

   (.venv) $ pip install -i https://test.pypi.org/simple/ medx==1.0.1

Alternative way to install it is to download or clone directly from the 
`GitHub Home Page <https://github.com/tirilab/medx>`_.

Install required Python versions and dependencies if needed, and run the following command in its root directory:

.. code-block:: console

   (.venv) $ pip install .

Calculating Medication Regimen Complexity
----------------

To calculate a list of Medication Regimen Complexity
and Medication Count for each patient,
you can use the ``medx.mrciCalc()`` function:

.. autofunction:: medx.mrciCalc

The ``ifilename`` parameter is the filename of input EHR data that contains medications list.

The ``ofilename`` parameter is the filename of output calculation.

Both ``ifilename`` and ``ofilename`` should be in .csv format.

The ``doseCol`` parameter is the column name of dose information in the input file; 
if not specified, the default value is ``Dose``.

The ``sigCol`` parameter is the column name of SIG in the input file; 
if not specified, the default value is ``SIG``.

The ``ndcCol`` parameter is the column name of NDC Code in the input file; 
if not specified, the default value is ``NDC Code``.

The ``medCol`` parameter is the column name of medication name in the input file; 
if not specified, the default value is ``Medication Name``.

The ``idenCol`` parameter is the column name of patient identifier in the input file; 
if not specified, the default value is ``MRN``.

The ``includeMC`` parameter is boolen option to include medcation count in the result; 
if not specified, the default value is ``True``.

:py:func:`medx.mrciCalc` will return 1 indicating calulation and
writing result succeded, otherwise will raise exceptions or errors.

For example:

>>> import medx
>>> medx.mrciCalc('sample_med.csv', 'tests/result.csv')
1

Comparing Medication Regimen Complexity at 2 time points
----------------

To calculate and compare Medication Regimen Complexity
and Medication Count for each patient along a time phase,
you can use the ``medx.mrciCompa()`` function:

.. autofunction:: medx.mrciCompa

The ``ifilename`` parameter is the filename of input EHR data that contains medications list.

The ``ofilename`` parameter is the filename of output calculation.

Both ``ifilename`` and ``ofilename`` should be in .csv format.

The ``doseCol`` parameter is the column name of dose information in the input file; 
if not specified, the default value is ``Dose``.

The ``sigCol`` parameter is the column name of SIG in the input file; 
if not specified, the default value is ``SIG``.

The ``ndcCol`` parameter is the column name of NDC Code in the input file; 
if not specified, the default value is ``NDC Code``.

The ``medCol`` parameter is the column name of medication name in the input file; 
if not specified, the default value is ``Medication Name``.

The ``idenCol`` parameter is the column name of patient identifier in the input file; 
if not specified, the default value is ``MRN``.

The ``timeCol`` parameter is the column name of time identifier in the input file;
if not specified, the default value is ``Time_period``.

The ``time1`` parameter is one of the time idenfier of input file (this function only allow comparison between two time points);
if not specified, the default value is ``current at enrollment``.

The ``includeMC`` parameter is boolen option to include medcation count in the result; 
if not specified, the default value is ``True``.


:py:func:`medx.mrciCompa` will return 1 indicating calulation and
writing result succeded, otherwise will raise exceptions or errors.

For example:

>>> import medx
>>> medx.medx.mrciCompa('sample_med.csv', 'tests/result.csv', timeCol = "Time", time1 = "three months after")
1

Load and Write data
----------------

**The medx.mrciCalc() and medx.mrciCompa() functions has already include the load and write data in their pipeline, 
so there is no need to manually load and write data if you are trying to call the previous two function.**

To load data from input file,
you can use the ``medx.load()`` function:

.. autofunction:: medx.load

The ``ifilename`` parameter is the filename of input data.
The input data need to be in .csv format.


:py:func:`medx.load` will return a Pandas Dataframe containing data from the input file, otherwise will raise exceptions or errors.

To write data to an output file,
you can use the ``medx.write()`` function:

.. autofunction:: medx.write

The ``df`` parameter is the data to write to file.
The ``df`` is a Pandas Dataframe.

The ``ofilename`` parameter is the ename of output file.
The output data need to be in .csv format.


:py:func:`medx.write` will return 1 if writing succeded, otherwise will raise exceptions or errors.

For example:

>>> import medx
>>> df = medx.load('sample_med.csv')
>>> medx.write(df, 'sample_med_copy.csv')
1
