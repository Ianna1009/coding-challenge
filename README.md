Median Degree of Venmo Transaction -- Implemented by Yanhuan Li
===========================================================

# Table of Contents
1. [Implementation Summary](README.md#implement-summary)
1. [Assumptions](README.md#Assumptions)
    2. [Maintaining Data within the 60 Second Window by Time Pointer](README.md#Maintaining Data within the 60 Second Window by Time Pointer)
3. [Directory Structure](README.md#Directory Structure)
4. [How to Test and Run the Code](README.md#How to Test and Run the Code)



## Implementation Summary
[Back to Table of Contents](README.md#table-of-contents)

### Assumptions

This implementation requires following assumptions:

1. If the transaction includes invalid timestamp (format for instance), invalid person (no `actor` or `target` entry), then we view this transaction as invalid transaction. Therefore the median degree calculation shouldn't be affected.
2. Based on the fist assumption, if same situation happens at the beginning of stream, median degree is 0.
2. If person in one transaction is `''`, ie information of this person (`actor` or `target`) didn't show up in the record, the we assume this transaction is valid and median degree should be affected. (In reality perhaps this person's information is protect)


### Maintaining Data within the 60 Second Window by Time Pointer
[Back to Table of Contents](README.md#table-of-contents)

In my tool, I used the latest event timestamp (`ts_ending`) as my time pointer. Every time a new payment with a new timestamp (`ts_new`) arrives in, there will be always three cases:


1. ts_new > ts_ending, then new time pointer should be assigned by ts_new.
2. ts_new < ts_ending and ts_new is in 60s window, then `ts_ending` remains the same, yet the only change maybe determined by delete old transaction or not.
3. ts_new < ts_enidng and ts_new is out of 60s window, pass.


## Directory Structure
[Back to Table of Contents](README.md#table-of-contents)

	├── README.md
	├── run.sh
	├── src
	│  	└── rolling_median.py
	├── venmo_input
	│   └── venmo-trans.txt
	├── venmo_output
	│   └── output.txt
	└── insight_testsuite
	 	   ├── run_tests.sh
		   └── tests
	        	└── test-1-venmo-trans
        		│   ├── venmo_input
        		│   │   └── venmo-trans.txt
        		│   └── venmo_output
        		│       └── output.txt
        		└── your-own-test
            		 ├── venmo_input
            		 │	  └── venmo-trans.txt
            		 └── venmo_output
            			  └── output.txt

## How to Test and Run the Code
[Back to Table of Contents](README.md#table-of-contents)

* bash run_tests.sh under insight_testsuite
* bash run.sh under root directory