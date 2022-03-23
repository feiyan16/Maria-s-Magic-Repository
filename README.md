# Bamboo HR Timesheet Reader
## Prerequisites HELLO MARIA!:
* Timesheet report(s) in **.csv** format **NOT** any excel extensions
* python 3.8 or above installed on your computer, see https://www.python.org/doc/ on how to download and install python
## Set up & Run:
1. Make sure all your files, bambooHR_time.py and .csv timesheet report(s), are in the same directory (aka folder)
   
   <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159301169-143b615f-a42d-436a-ae88-b01aedaa3f07.png">
2. In your command-prompt / terminal, navigate into the folder that contains all the files by typing ```cd [the directory path]``` see https://www.howtogeek.com/659411/how-to-change-directories-in-command-prompt-on-windows-10/#:~:text=If%20the%20folder%20you%20want,window%2C%20and%20then%20press%20Enter. for more information on how to change directories
3. Once you have navigated successsfully to the directory, type ```python3 bambooHR_time.py [file name of your .csv report]``` and press [ENTER]. 
   This is a sample run:
   
   <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159330088-e991bad5-7bde-4ae0-a5a8-1c654d17c16c.png">
   
   <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159339072-736c22ef-ac82-4a6b-adc1-dd1bdec52a28.png">
   
   <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159339176-7da249cc-8653-482b-b6d7-42e2dc8672f5.png">
   
   <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159339216-27d659a0-ec6e-48f1-baeb-be544fee3dbe.png">
4. Your output file, report.csv, will be generated in the same directory as all the other files
   
   <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159303930-916f9647-db11-48a6-a95e-1bea4e820f13.png">
## Things to Note:
* The program output will tell you what it is doing at each step, so read the output to know what the program is doing:
  
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159326123-95002345-d0c5-496b-8873-c2d449dfa3dd.png">
* At each row, it will show the row it is parsing:
  
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159326398-1ada765e-ce7b-4e2e-8f29-a1400ce13f5b.png">
* Warnings will show up saying that the program altered some information, etc. but it will not stop your program:
  
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159326712-995332ae-f329-4da6-b850-23bca4dd30c2.png">
### Errors:
* This means that the program cannot find the timesheet report .csv file, make sure that your file is in the same directory as the program .py file and that you've spelled the file name correctly.
  
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159327140-4a51a103-b237-4b5d-a3a2-c72abe33d3f5.png"> 
* This means that the file is not in .csv format, make sure your timesheet report is actually in csv format and not in excel of anyother formats
  
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159329313-56d68c91-d983-432c-afdd-31d5a100fe86.png">

# Dell Invoice Reader
## Prerequisites:
* Dell invoice from 2021 and later in **.pdf** format. **DO NOT** use any other formats
* python 3.8 or above installed on your computer, see https://www.python.org/doc/ on how to download and install python
* Package module, pdfplumber, installed. See https://pypi.org/project/pdfplumber/ on how to download and install
## Set up and Run
1. Make sure you have all your files, dell_invoice_reader.py and pdf(s), in the same directory. 
2. In your command-prompt / terminal, navigate into the folder that contains all the files by typing ```cd [the directory path]``` see https://www.howtogeek.com/659411/how-to-change-directories-in-command-prompt-on-windows-10/#:~:text=If%20the%20folder%20you%20want,window%2C%20and%20then%20press%20Enter. for more information on how to change directories
3. Once you have navigated successsfully to the directory, type ```python3 dell_invoice_reader.py [pdf_file name]``` and press [ENTER]. 
   This is a sample run:
   
   <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159568175-932d2c95-7e46-4d8a-a725-a95c2395eda5.png">
4. Your output file, hardware.csv, will be generated in the same directory as all the other files
## Things to Note:
* The program can pick up multiple invoices and products from that invoice. This means you can join all the invoices into one pdf and run the program with that joined pdf.
* The program will tell you what page it is currently parsing and everytime a new invoice or product is found. Use these to check if the program is reading correctly

  <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159568730-468cf340-ff3c-4515-b3cf-7e3831c3db05.png">

* If you run the program more than once, the output file will not be overwritten with new content. New content will be added to the existing output file. Meaning, you should only run the program once.
## Errors:
* This means that the program cannot find the pdf file, make sure that your file is in the same directory as the program .py file and that you've spelled the file name correctly.

  <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159569939-338db501-f563-45df-b380-0b847919d952.png">
* This means that the pdf file you're using is in the wrong format, make sure that the file is in **.pdf** format

  <img width="500" alt="image" src="https://user-images.githubusercontent.com/55895535/159569868-764f9774-b6aa-46bb-8e70-26d06becd4a6.png">



 
