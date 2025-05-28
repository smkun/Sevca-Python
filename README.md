# SEVCA Client Worksheet App

A standalone desktop application for managing SEVCA client worksheet data. Built in Python with a simple Tkinter interface.

Created as a favor by **Scott Kunian**  
© 2025. Not for commercial use.

---

## Features

- Fill out client intake forms using a clean, tabular layout
- Add or remove rows dynamically
- Save worksheet data to `.json`
- Load saved worksheets from `.json`
- Export a well-formatted `.pdf` version of the data
- Includes SEVCA logo and consistent header formatting across pages
- Supports date picker (via `tkcalendar`)
- Uses landscape PDF output with proper column sizing

---

## Requirements

Python 3.10+  
Install dependencies with:

```bash
pip install fpdf tkcalendar
