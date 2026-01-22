UIDAI District Decision Intelligence Engine

This repository contains the source code and analytical pipeline developed for the UIDAI Data Hackathon 2026.

The project analyses anonymised Aadhaar Enrolment Demographic Update and Biometric Update datasets to identify district level operational stress signals. It constructs interpretable indicators related to migration pressure labour related biometric wear and Aadhaar service access stress and maps them to practical administrative actions.

Project Structure

data
Raw UIDAI datasets and reference master files

src
Python scripts for data preparation and signal construction

output
Final district level decision intelligence output

How to Run

1 Install Python 3 10 or above  
2 Install dependencies using pip install -r requirements.txt  
3 Run python src/01_merge_and_prepare.py  
4 Run python src/02_signal_engine.py  

The final output will be generated as output district_decision_intelligence csv

Visualisation

Static visualisations and dashboards were created using Tableau using the generated output file.

Disclaimer

This project uses only anonymised and aggregated data provided as part of the UIDAI Data Hackathon and does not contain any personal data.
