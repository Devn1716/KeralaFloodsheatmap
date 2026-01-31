# KeralaFloodsheatmap
Recurring floods in Kerala are driven by extreme rainfall, land-use change, and drainage limitations. This repository presents a geospatial heatmap analysis of flood-affected areas, integrating environmental and spatial data to identify high-risk zones.


KeralaFloodsHeatmap: Configure and Run Guide
    Step 1: Clone the repository

        Open PowerShell or Git Bash and run:

        git clone https://github.com/Devn1716/kerala_floods_heatmap.git
        cd kerala_floods_heatmap


This downloads the project to your local computer and moves into the project folder.

    Step 2: Create a Python virtual environment

        Recommended to avoid dependency conflicts.

        python -m venv env


This creates a folder env/ containing a clean Python environment.

    Step 3: Activate the virtual environment

        Windows (PowerShell):

        .\env\Scripts\Activate


        Linux / Mac:

        source env/bin/activate


    Once activated, your prompt should show (env) at the start.

    Step 4: Install project dependencies
        pip install --upgrade pip
        pip install -r requirements.txt


Installs all Python libraries needed to run the project.

    Step 5: Prepare datasets

        All data files (CSV, shapefiles, GeoTIFFs) should be in the datasets/ folder.

        Example datasets:

            datasets/
                    ├── rainfall_data.csv
                    ├── flood_zones.shp
                ├── land_use.tif


    ⚠️ If you don’t have the real datasets, you can put sample data for testing.

    Step 6: Run the Streamlit app
        streamlit run scripts/frontend.py


    Streamlit will start a local server.

    You’ll see messages like:

    You can now view your Streamlit app in your browser.

    Local URL: http://localhost:8501
    Network URL: http://192.168.1.5:8501


    Open the Local URL in your browser to see the app.

    Step 7: Explore the app

        The web interface will display:

        Flood heatmap for Kerala

        Options to select datasets or filter by regions

        Interactive map features (zoom, pan, etc.)

        Optional: Update the code

        Scripts are in the scripts/ folder.

        You can modify frontend.py to:

        Change map styles

        Add new dataset layers

        Update visualizations