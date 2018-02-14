import csv, math, datetime, re, argparse, sys

def skip_record_validation(validity):
    ''' Validate the recipient_id, trans_dt, zipCode, name, recipient_id, trans_Amt
        on each record before processing.
    '''
    try:
        flags = dict.fromkeys(["isValid_Date", "isValid_ZipCode", "isValid_Name",\
                               "isValid_recipient_id","isValid_trans_Amt","isValid_other_id"], True)
        datetime.datetime.strptime(validity[0], '%m%d%Y') # if not valid it throws exception.
    except ValueError:
        flags.update(dict.fromkeys(["isValid_Date"], False))
    if (validity[1]=='' or len(validity[1])<5): # empty & len<5
        flags.update(dict.fromkeys(["isValid_ZipCode"], False))
    if (validity[2] =='' or (validity[2].isalnum()==True) or (re.match(r"[a-zA-Z\s]+,[a-zA-Z\s]+",validity[2]) == None)):  # empty & malformed{ NAME, NAME}
        flags.update(dict.fromkeys(["isValid_Name"], False))
    if (validity[3]=='' ): # empty
        flags.update(dict.fromkeys(["isValid_recipient_id"], False))
    if (validity[4]=='' ): # empty
        flags.update(dict.fromkeys(["isValid_trans_Amt"], False))
    if (validity[5] != ""): # empty
        flags.update(dict.fromkeys(["isValid_other_id"], False))
    return flags

def main():
     """This the main function.
        Program base is written here.
        Just uncomment the all the print statements and you will
        see a nice execution of the whole program.
     """
with open(sys.argv[1], "r") as itcont,\
        open(sys.argv[3],'w', newline='') as repeat_donors,\
            open(sys.argv[2],'r') as computePercentile :


        outputFromat              = csv.writer(repeat_donors, delimiter='|')
        line                      = computePercentile.readlines()
        percentileValue           = int(line[0][:2])
        collection = []
        validRecordCount,inValidRecordCount,index, output=(0 for i in range(4))
        # for each line from the input file
        for record in itcont:
            columns =record.split('|')
            recipient_id, donor_id, donor_name, zip_code, trans_dt, trans_amt, other_id= columns[0],columns[7]+'+'+columns[10][:5], columns[7], columns[10][:5], columns[13], columns[14],columns[15]
            collPercentile,sortedCollPercentile=([] for i in range(2))
            s = trans_amt.strip()
            totalAmtRecieved = float(trans_amt) if s else 0
            validity=[trans_dt,zip_code,donor_name,recipient_id ,trans_amt, other_id]

            if False not in skip_record_validation(validity).values():#only valid records will move further, invalid will be catched in the inValidRecordCount counter.
                validRecordCount+=1
#                 print("Start",validRecordCount,'st record with collection size',len(collection))
# First scan of the valid lines collected into the collection yet.
                for cursor in collection:
                        if donor_name == cursor.get('donor_name'):
                            if trans_dt[-4:] > cursor.get('trans_dt')[-4:]:
                                # the above two if-statements ensures a repeat donor
                                contrib= 1
                                collPercentile.append(trans_amt) # this is to collect the current transaction amounts
                                # second scan of the valid lines collected so far to catch the recipient for each repeat donor.
                                for cursor2 in collection:
                                    if (recipient_id == cursor2.get('recipient_id') and zip_code == cursor2.get('zip_code') and\
                                        trans_dt[-4:] == cursor2.get('trans_dt')[-4:]):

                                        collPercentile.append(cursor2.get('trans_amt'))
                                            # 3. Calc total number of transactions from repeat donors
                                        contrib+=1
                                            # 2. Calc total amount of donations streaming in from repeat donors
                                        totalAmtRecieved= totalAmtRecieved + float(cursor2.get('trans_amt'))
#                                     else: print("didn't find any contribution")
#                                 print('<<',collPercentile)
                                    # 1. Calc running percentile of contributions from repeat donors
                                sortedCollPercentile= sorted(collPercentile)
                                index= math.ceil((percentileValue/100)* len(sortedCollPercentile))
#                                 print('>>',sortedCollPercentile)
                                outputFromat.writerow([recipient_id,zip_code,trans_dt[-4:],round(float(sortedCollPercentile[index-1])),round(totalAmtRecieved),contrib])
#                             else:print("Can't match Year")
#                         else:print("can't match donor_name ")

#                 print('...'*10,validRecordCount,'th record checked & added')
                record= {'recipient_id':recipient_id,'donor_name':donor_name,\
                                   'zip_code':zip_code,'trans_dt':trans_dt,'trans_amt':trans_amt,\
                                    'donor_id':donor_name+zip_code}
                collection.append(record)

            else:
                inValidRecordCount+=1
#         print('validRecordCount',validRecordCount,'inValidRecordCount',inValidRecordCount,)
itcont.close()
repeat_donors.close()
print("running donation_analysis")

if __name__ == "__main__":
 '''The programs entry point'''
 main()
