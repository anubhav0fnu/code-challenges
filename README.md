### Approach:
I used the below agorithm to develop my solution for donation analysis problem.
> for each record in the file:
>> 1. **check for invalid conditions & ignore or skip an entire record**(line) in the file
 * `if ((other_id == empty/NaN) or (trans_dt != INVALID) or (zipCode != INVALID) or \
   (name !=INVALID) or (recipient_id != empty/NaN) or (trans_Amt != empty/NaN) )`
>> 2. **Once you get the valid record**:<br/>
>> 2.1. **identifing the repeating donor**
   * `if the name(donor) matches & the current year is greater than the previous`<br/>
>> 2.1.1 **Then, catch the recipient for each donor**.
        * `if (recipient_id and zipCode and year matches)i.e recipient already contributed in the prior year)`
>>>>   2.1.1.  Now, **for each recipient do the following computation for donation analysis**:
>>>>>  * Calc running percentile of contributions from repeat donors     //run_perc
         * rounded to the whole dollar(```<0.50$ == lower integer, >=0.50$ == Upper interger.``` )
         * it should taken from percentile.txt file
>>>>>  * Calc total number of transactions from repeat donors            //totalCountContrib
>>>>>  * Calc total amount of donations streaming in from repeat donors  //totalAmtRecieved

##### **Assumptions**:
>    1. Federal Election Commission provides data files stretching back years and is regularly updated.(increasing order.)
>>   **CATCH:**  
>>>* Testing will be any order of input lines.
>>>* you should not assume the year field holds any particular value
>>>* All lines are new so no worries of any duplicate transaction lines/entery.
>>>* The o/p repeat_donors.txt file should have only entry for repeated donors with records seperator.
>>>>* recipient_id|zipCode|year|run_perc|total_amt_contib|countOfTrans

### Dependencies:
    No major dependencies. If you have installed conda package manager, it will pre-install everything before hand.
### Run:
    1. run the run.sh command to check on trivial input
    2. Uncomment the 1st line in 8th line in run.sh and comment the 5th line to execute the test case(created by me.)
**Note**: if you want to understand the flow of the code, then please uncomment the print statements in donation_analysis.py file and run the script run.sh. The print statements guide you well throught the approach I have described above.

### Intial Test run: Passed
$ ./run_tests.sh<br/>
running donation_analysis<br/>
[PASS]: test_1 repeat_donors.txt<br/>
running donation_analysis<br/>
[PASS]: your-own-test_1 repeat_donors.txt<br/>
[Wed Feb 14 02:59:42 CST 2018] 2 of 2 tests passed<br/>
