Usage
=====

.. _installation:

Installation
------------

To use MedX, first install it using pip:

.. code-block:: console

   (.venv) $ pip install -i https://test.pypi.org/simple/ medx

Calculating Medication Regimen Complexity
----------------

To calculate a list  Medication Regimen Complexity
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


