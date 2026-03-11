Getting Started
===============

Install dependencies with ``uv sync --extra dev`` and run:

.. code-block:: bash

   uv run resonance-pipeline --input path/to/data.csv --output-dir manuscript/artifacts

Or use the short top-level API:

.. code-block:: python

   import resonance_risk_screening as rrs
   outputs = rrs.screen("data/substation_scada_33_11kv.csv", "manuscript/artifacts")

Method-chaining workflow:

.. code-block:: python

   session = rrs.ScreeningSession().load("data/substation_scada_33_11kv.csv").prep().fit()
   print(session.summary())
