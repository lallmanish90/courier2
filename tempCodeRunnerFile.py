from typing import cast
import pdfplumber
import re
import os
import glob
import csv
import pandas as pd

folder = (glob.glob("*.pdf"))

sum = 0
case1 = 0
case2 = 0
case3 = 0
case4 = 0

for file_name in folder:
    # it will open each file in the directory
    try:
        pdf = pdfplumber.open(file_name)
        page = pdf.pages[0]  # selecting the first page
        text = page.extract_text()  # extracting the text
        sum += 1
        print(sum)
        print(file_name)
        try:
            if ((text.split('\n')[0] == 'Provisional Certiﬁcate for COVID-19 Vaccination - 1st Dose ' or text.split('\n')[0] == 'Final Certiﬁcate for COVID-19 Vaccination') and text.split('\n')[6] != 'Unique Health ID (UHID)'):
                try:
                    case1 += 1
                    print(file_name, "case1 - health id present")
        #             print(case1)
                except:
                    print("Manish - missed", file_name)
                    continue

            elif ((text.split('\n')[0] != 'Provisional Certiﬁcate for COVID-19 Vaccination - 1st Dose ' or text.split('\n')[0] != 'Final Certiﬁcate for COVID-19 Vaccination') and text.split('\n')[6] == 'Unique Health ID (UHID)'):
                try:
                    case2 += 1
                    print(file_name, "case2 - no health ID")
        #             print(case2)
                except:
                    print("Manish - missed", file_name)
                    continue
            elif (text.split('\n')[0] == 'Certiﬁcate for COVID-19 Vaccination'):
                try:
                    case3 += 1
                    print(file_name, "case3 - certificate")
        #             print(case3)
                except:
                    print("Manish - missed", file_name)
                    continue
            else:
                try:
                    case4 += 1
                    print(file_name, "case4 - different design4")
        #             print(case4)
                except:
                    print("Manish - missed", file_name)
                    continue
        except:
            print("manish - image in pdf", file_name)

    except:
        print("manish - not a pdf file", file_name)

print(case1, "case1 - health id present")
print(case2, "case2 - no health ID")
print(case3, "case3 - certificate")
print(case4, "case4 - different design4")
