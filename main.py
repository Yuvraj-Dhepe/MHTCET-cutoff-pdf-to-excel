from pypdf import PdfReader
import re, json, os

reader = PdfReader(input("Enter the path of the PDF file: "))

alldata = {}

CurrentEntry = {
    "collegeName": "",
    "branches": {},
}

currents = {
    "college_name": "",
    "branch": "",
    "SeatLevel": "",
    "ress": [],
    "ressIndex": 0,
    "nextExpected": "",
}

skippedPages = []

for pageNO, page in enumerate(reader.pages):
    complete_page_text = page.extract_text()
    # if "II" in complete_page_text:
    #     skippedPages.append([pageNO, complete_page_text])
    #     continue
    complete_page_text = complete_page_text.split("\n")
    lineNo = 0
    skippedText = ""
    while lineNo < len(complete_page_text):
        line = complete_page_text[lineNo]
        lineNo += 1
    
        if "Legends: Starting" in line:
            break

        elif line in ['D', 'i'] or "Cut Off List for Maharashtra" in line or "State Common Entrance Tes" in line or "Degree Courses In Engineering and Technology" in line:
            continue
    
        elif re.match(r'^\d{4}(?!\d{2})', line) and line[:4]+" - " in line:
            currents["college_name"] = line
            if line not in alldata: alldata[line] = {}

        elif re.match(r'^\d{9}', line):
            if line not in alldata[currents["college_name"]]: alldata[currents["college_name"]][line] = {}
            currents["branch"] = line
            
            line = complete_page_text[lineNo]
            lineNo += 1
            if "Status: " in line: 
                alldata[currents["college_name"]][currents["branch"]]["status"] = line.replace("Status: ", "")

        elif "Home University" in line or "State Level" in line:
            currents["SeatLevel"] = line
            alldata[currents["college_name"]][currents["branch"]][currents["SeatLevel"]] = {}
            line = complete_page_text[lineNo]
            lineNo += 1

            currents["ress"] = line.split(" ")
            while "  I " not in complete_page_text[lineNo] and "  II " not in complete_page_text[lineNo]:
                line = complete_page_text[lineNo]
                lineNo += 1
                currents["ress"] += line.split(" ")
            for ress in currents["ress"]:
                alldata[currents["college_name"]][currents["branch"]][currents["SeatLevel"]][ress] = [-1,-1]

            line = int(complete_page_text[lineNo].replace("  I ", '').replace("  II ", ''))
            lineNo += 1
            alldata[currents["college_name"]][currents["branch"]][currents["SeatLevel"]][currents["ress"][currents["ressIndex"]]][1] = line
            while True:
                line = complete_page_text[lineNo]
                lineNo += 1
                perTile = float(line[line.index('(')+1:line.index(')')])
                alldata[currents["college_name"]][currents["branch"]][currents["SeatLevel"]][currents["ress"][currents["ressIndex"]]][0] = perTile
                currents["ressIndex"] += 1
                NextRank = line[line.index(')')+1:]
                if NextRank == 'Stage' or NextRank == '':
                    currents["ressIndex"] = 0
                    break
                else:
                    alldata[currents["college_name"]][currents["branch"]][currents["SeatLevel"]][currents["ress"][currents["ressIndex"]]][1] = int(NextRank)
        else:
            skippedText += line+"\n"
        # print(line)
    if page.extract_text().replace("\n", '') in skippedText:
        skippedPages.append([pageNO, skippedText])
        print(f"Page {pageNO+1} Skipped")
    elif skippedText!="":
        skippedPages.append([pageNO, skippedText])
        print(f"Page {pageNO+1} half Skipped")
    else:
        print(f"Page {pageNO+1} Done")

with open("data.json", "w") as outfile:
    outfile.write(json.dumps(alldata, indent=4))

for pageNo, page in skippedPages:
    with open(f"skipped/{pageNo+1}.txt", "w") as outfile:
        outfile.write(page)
