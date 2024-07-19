import json, openpyxl

def next_col(current_col, n=1):
    current_col = current_col.upper()
    base = ord('A')
    num_chars = 26
    current_num = sum((ord(c) - base + 1) * (num_chars ** i) for i, c in enumerate(reversed(current_col)))
    next_num = current_num + n
    result = ""
    while next_num > 0:
        next_num, remainder = divmod(next_num - 1, num_chars)
        result = chr(base + remainder) + result
    return result

if __name__ == '__main__':

    try: wb = openpyxl.open('output.xlsx')
    except: wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "CollegeList"

    with open('data.json') as f: allData = json.load(f)
    res = {}
    for college in allData:
        for branch in allData[college]:
            status = allData[college][branch]['status']
            for seatHeading in allData[college][branch]:
                if seatHeading == 'status': continue
                if seatHeading not in res: res[seatHeading] = []
                for reservation in allData[college][branch][seatHeading]:
                    if reservation not in res[seatHeading]: res[seatHeading].append(reservation)

    xlCur = {
        'sh': ['F', 2],
    }
    
    ReservationColBindings = {}

    ws['B2'] = 'Sr. No'
    ws.merge_cells('B2:B4')
    ws['C2'] = 'College Name'
    ws.merge_cells('C2:C4')
    ws['D2'] = 'Branch'
    ws.merge_cells('D2:D4')
    ws['E2'] = 'Status'
    ws.merge_cells('E2:E4')

    center_alignment = openpyxl.styles.Alignment(horizontal='center', vertical='center')
    for row in ws["B2:E4"]:
        for cell in row:
            cell.alignment = center_alignment

    for seatHeading in res:
        ws[f"{xlCur['sh'][0]}{xlCur['sh'][1]}"] = seatHeading
        ws[f"{xlCur['sh'][0]}{xlCur['sh'][1]}"].alignment = center_alignment
        # print(f"{xlCur['sh'][0]}{xlCur['sh'][1]} Set to {seatHeading}") #DEBUG
        
        xlCur['r'] = [xlCur['sh'][0], 3]
        ReservationColBindings[seatHeading] = {}
        
        for n, reservation in enumerate(res[seatHeading]):
            ws[f"{xlCur['r'][0]}{xlCur['r'][1]}"] = reservation
            ws[f"{xlCur['r'][0]}{xlCur['r'][1]}"].alignment = center_alignment
            ReservationColBindings[seatHeading][reservation] = xlCur['r'][0]
            # if reservation in ReservationColBindings:
            #     print(f"Dublicate Reservation FOUND: {seatHeading}:{reservation}")
            #     print(json.dumps(res, indent=4))
            #     exit()
            # else:
            #     ReservationColBindings[seatHeading][reservation] = xlCur['r'][0]
            # print(f"{xlCur['r'][0]}{xlCur['r'][1]} Set to {reservation}") #DEBUG
            
            nextColOfRes = next_col(xlCur['r'][0])
            
            ws[f"{xlCur['r'][0]}{xlCur['r'][1]+1}"] = "%ile"
            ws[f"{nextColOfRes}{xlCur['r'][1]+1}"] = "Rank"
            # print(f"{xlCur['r'][0]}{xlCur['r'][1]+1}, {nextColOfRes}{xlCur['r'][1]+1} Set to %ile, Rank") #DEBUG

            ws.merge_cells(f"{xlCur['r'][0]}{xlCur['r'][1]}:{nextColOfRes}{xlCur['r'][1]}")
            # print(f"{xlCur['r'][0]}{xlCur['r'][1]}:{nextColOfRes}{xlCur['r'][1]} MERGED") #DEBUG
            xlCur['r'][0] = next_col(nextColOfRes) if n < len(res[seatHeading])-1 else nextColOfRes
        
        ws.merge_cells(f"{xlCur['sh'][0]}{xlCur['sh'][1]}:{xlCur['r'][0]}{xlCur['sh'][1]}")
        # print(f"{xlCur['sh'][0]}{xlCur['sh'][1]}:{xlCur['r'][0]}{xlCur['sh'][1]} MERGED") #DEBUG
        
        xlCur['sh'][0] = next_col(xlCur['r'][0])
    
    xlCur = {
        "sr": 1,
        "sr_col": 'B',
        "college_col": 'C',
        "branch_col": 'D',
        "stat_col": 'E',
        "row": 5,
    }

    for college in allData:
        for branch in allData[college]:
            status = allData[college][branch]['status']
            ws[f"{xlCur['sr_col']}{xlCur['row']}"] = xlCur['sr']
            ws[f"{xlCur['college_col']}{xlCur['row']}"] = college
            ws[f"{xlCur['branch_col']}{xlCur['row']}"] = branch
            ws[f"{xlCur['stat_col']}{xlCur['row']}"] = status
            ws[f"{xlCur['stat_col']}{xlCur['row']}"] = status
            for seatHeading in allData[college][branch]:
                if seatHeading == 'status': continue
                for reservation in allData[college][branch][seatHeading]:
                    PerTile = allData[college][branch][seatHeading][reservation]
                    Rank = PerTile[1]
                    PerTile = PerTile[0]
                    PerTileCOL = ReservationColBindings[seatHeading][reservation]
                    rankCol = next_col(PerTileCOL)
                    ws[f"{PerTileCOL}{xlCur['row']}"] = PerTile
                    ws[f"{rankCol}{xlCur['row']}"] = Rank
            xlCur['row'] += 1
            xlCur['sr'] += 1

    wb.save('output.xlsx')