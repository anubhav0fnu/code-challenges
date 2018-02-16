import csv, math, datetime, re, argparse, sys

def skip_record_validation(validity):
    ''' Validate the recipient_id, trans_dt, zipCode, name, recipient_id, trans_Amt
        on each record before identifying repeat donor & calculations for a recipient.
    '''
    try:
        flags = dict.fromkeys(["isValid_Date", "isValid_ZipCode", "isValid_Name",\
                               "isValid_recipient_id","isValid_trans_Amt","isValid_other_id"], True)
        # data validity check
        datetime.datetime.strptime(validity[0], '%m%d%Y')
    except ValueError:
        flags.update(dict.fromkeys(["isValid_Date"], False))

        # empty & len<5
    if (validity[1]=='' or len(validity[1])<5):
        flags.update(dict.fromkeys(["isValid_ZipCode"], False))
        # empty & malformed{ NAME, NAME}
    if (validity[2] =='' or (validity[2].isalnum()==True) or \
            (re.match(r"[a-zA-Z\s]+,[a-zA-Z\s]+",validity[2]) == None)):
        flags.update(dict.fromkeys(["isValid_Name"], False))
        # empty
    if (validity[3]=='' ):
        flags.update(dict.fromkeys(["isValid_recipient_id"], False))
        # empty
    if (validity[4]=='' ):
        flags.update(dict.fromkeys(["isValid_trans_Amt"], False))
        # empty
    if (validity[5] != ""):
        flags.update(dict.fromkeys(["isValid_other_id"], False))
    return flags

def main():
     """relevant Fields from itcont.txt input file.
                ------GIVEN---------||-------My_Convention_fot_easy_understanding------------------
                ++++++++++++++++++++==+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # CMTE_ID           ::  recipient_id ( recipient of a contribution                 )
                # NAME              ::  donor_name   ( name of the donor                           )
                # ZIP_CODE          ::  zip_code     ( zip code of the contributor                 )
                # TRANSACTION_DT    ::  trans_dt     ( date of the transaction                     )
                # TRANSACTION_AMT   ::  trans_amt    ( amount of the transaction                   )
                # OTHER_ID          ::  other_id     ( contribution came from a person or an entity)

     **NOTE**: In order to see indepth execution of the program, just uncomment all the print statements.

     Output file format:
     "recipient of the contribution" |"zip code of the contributor"| "year of the contribution" | \
     "running percentile of contributions" | "total amount of contributions" | "total number of transactions received by recipient"

     For Percentile computation, I have used:
     Nearest-rank method
     """
     # picking up input files from command-line args.
with open(sys.argv[1], "r") as itcont,\
        open(sys.argv[3],'w', newline='') as repeat_donors,\
            open(sys.argv[2],'r') as computePercentile :

            # create a writer object to convert (list containing calculations) ==> (delimited strings in repeat_donors.txt.
        outputFromat              = csv.writer(repeat_donors, delimiter='|')
            # read percentile value (1-100) from percentile.txt file.
        line                      = computePercentile.readlines()
        percentileValue           = int(line[0])
            # imagine it as a collection of objects of kind dict.
        collection = []
            # VALID & INVALID record counters.
        validRecordCount,inValidRecordCount,index, output=(0 for i in range(4))
            # run for reach record in itcont.txt file pointer.
        print('~'*50,'Start','~'*50)
        for record in itcont:
                # splitting each record on the basis of "|" delimiter.
            columns =record.split('|')
                # fill in relevant easy to read variable
            recipient_id, donor_id, donor_name, zip_code, trans_dt, trans_amt, other_id= columns[0],\
            columns[7]+'+'+columns[10][:5], columns[7], columns[10][:5], columns[13], columns[14],columns[15]
            collPercentile,sortedCollPercentile=([] for i in range(2))

            validity=[trans_dt,zip_code,donor_name,recipient_id ,trans_amt, other_id]

            if False not in skip_record_validation(validity).values():#only valid records will move further, invalid will be catched in the inValidRecordCount counter.
                validRecordCount+=1
                totalAmtRecieved = float(trans_amt)
                # seperate VALID & INVALD records
#                print("Start",validRecordCount,'st record with collection size',len(collection))

                # First scan of the collection (having valid lines) to catch repeat donors.
                for cursor in collection:
                            # Identify repeat donor.
                        if donor_name == cursor.get('donor_name'):
                            if trans_dt[-4:] > cursor.get('trans_dt')[-4:]:
                                # counter to track repeat donor
                                contrib= 1
                                # list1 to collect current transaction amount.
                                collPercentile.append(float(trans_amt))

                                # Second scan of collection (having valid lines) to catch the recipient for each repeat donor.
                                for cursor2 in collection:
                                        # Identify recipient
                                    if (recipient_id == cursor2.get('recipient_id') and zip_code == cursor2.get('zip_code') and\
                                        trans_dt[-4:] == cursor2.get('trans_dt')[-4:]):

                                            # list1 to collect matched recipient based on above conditions.
                                        collPercentile.append(float(cursor2.get('trans_amt')))
                                            # 3. Calc total number of transactions from repeat donors
                                        contrib+=1
                                            # 2. Calc total amount of donations streaming in from repeat donors
                                        totalAmtRecieved= totalAmtRecieved + float(cursor2.get('trans_amt'))
#                                     else: print("didn't find any contribution")
#                                 print('<<',collPercentile)
                                    # 1. Calc running percentile of contributions from repeat donors(Nearest-rank method)
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
        print('validRecordCount',validRecordCount,'inValidRecordCount',inValidRecordCount,)
        print('~'*50,'Over','~'*50)
itcont.close()
repeat_donors.close()
# print("running donation_analysis")

if __name__ == "__main__":
 '''The programs entry point'''
 main()
