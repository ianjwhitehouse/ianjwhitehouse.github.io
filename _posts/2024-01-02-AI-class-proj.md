---
layout: post
title: "Giving Large Language Models Access to Tools - AI Class Final Project"
tags: Project Natural-Language Large-Language-Model
---

While searching for a final project for my artificial intelligence class last semester, I was inspired by [Andrej Karpathy's tweet on an LLM Operating System](https://twitter.com/karpathy/status/1723140519554105733), especially the image shown below. 

![](/public/content/2024/LLM_OS.png)
*Andrej Karpathy's Overview of an LLM Operating System* 

My final project wasn't a complete operating system, however, it was an assistant that lay in between the user and the machine.  Then, from the user's perspective, they can interact with their computer simply by conversing with the assistant.  The assistant responds to their conversation and can run commands or visit websites on behalf of the user.  This way, the user, especially users who are not tech-savvy, can interact with their computer in a much more intuitive manner, while the LLM assistant abstracts away the complexities of the command line. 

I wanted to give the LLM assistant access to these custom commands, which I chose to provide it access to most of the tasks a user would want to perform.  These were:
 - %LIST: List files in the current directory (Equivalent to Linux 'ls')
 - %CD: Change directory to a different path (Equivalent to Linux 'cd')
 - %READ: Read a file (Equivalent to Linux 'cat')
 - %WRITE: Write a file (Equivalent to Linux 'echo')
 - %READ_WEB: Download a URL and convert to plaintext
 - %SEARCH_WEB: Download www.google.com/search?q='search query' and convert to plaintext 

As I reviewed the literature, I saw that there were two main approaches to giving a large language model access to tools: fine-tuning and prompt engineering.  However, fine-tuning was outside the scope of my project so I used the out-of-the-box model with a custom prompt.  However, even after considerable effort writing a prompt for the large language model, I found it was still unreliable and its outputs were largely nonsensical. Therefore, I had to sample the LLM 32 times for each prompt, and I wrote a small algorithm to choose the best output from the model.  I judged each response from the LLM based on these criteria:
 - The number of words in common between one response and the other 31 responses
 - The number of words in common between a response and the user’s original question
 - Whether or not the LLM uses a command and whether or not the LLM spells the command correctly 

I reasoned that the ideal response from the LLM, when considering that each response is slightly random, should
 - Be the closest to the average of all of the responses (Ideally, the medoid response would be the least noisy response and closest to the LLM's actual belief)
 - Be relevant to the user’s question
 - Use a command before guessing/hallucinating
 - Not attempt to use a command that doesn’t exist 

This project was very interesting; however, the model was just too small to be useful.  With a bigger model like Llama 2 70B, the project could have resulted in a useful assistant.  While I played with the program, it was tempting to reason with the model.  Unfortunately, this tended to cause the model to break down more.  In addition, while the model did use command such as %SEARCH_WEB, it tended to just repeat the results of the search verbatim to the user instead of summarizing them or responding directly to the user's question.  The model also couldn't handle sequences of tasks.  A big thing that I wanted to do in this project was get the model to understand that, when asked to search for something and summarize the search results in a file, it would have to run two commands.  However, the model could not comprehend this, and I had to break down my goals into steps myself. 

In the future, I want to experiment with a different model and to fine-tune the model using the LoRA framework. This project could enable a new method of interaction between a user and their computer if the assistant is able to use these tools practically. 

[Presentation Accessible Here](/public/content/2024/CSC-468%20Final%20Project.pptx) 

[Code Accessible Here](/public/content/2024/console_tool_model.py) 

**Sample Conversations** 

*user*: What is American University?  
*assistant*: %SEARCH_WEB American University  
*assistant*: American University is a private university in DC.  Its campus is located in Northwest DC.  Its average GPA is a 3.3 and its average SAT score is 1240.  Its average LSAT score is 154.  The school is most active in politics and law, and most famous for its law school.  
*user*: Do they have a computer science department?  
*assistant*: %SEARCH_WEB Does American University have a computer science department?  
*assistant*: Yes, they have a computer science department  
*user*: Can you list some professors who teach at the American University computer science department?  
*assistant*: %READ American University computer science department  
*assistant*: %SEARCH_WEB List professors in the American University computer science department  
*assistant*: Some professors who teach at the American University computer science department are:  
*user*: You didn't list any.  Can you please list some professors in the American University department of computer science?  
*assistant*: %SEARCH_WEB List professors in the American University department of computer science  
*assistant*: Some professors in the American University department of computer science are Jacques Houde, Nathalie Japkowicz, Roberto Corizzo, Qulong Han, and Anand Nataraj (amongst others).  American University has more well known professors in the department of computer science in international relations.  
*Here, the assistant was able to search the web and understood the search results.  However, only Nathalie Japkowicz and Roberto Corizzo actually teach in the American University CS Department.  The other people listed are potentially real people, so maybe their names appear in the model's training data* 

*user*: Can you move up one directory?  
*assistant*: %CD ..  
*assistant*: I have moved up one directory  
*user*: What is in this directory?  Is my auto-encoder research in it?  
*assistant*: %LIST  
*assistant*: There are 35 files in the home directory, one of which is my auto-encoder research  
*user*: What is the name of the folder that include my auto-encoder research?  
*assistant*: %LIST  
*assistant*: The name of the folder containing my auto-encoder research is Data Mining Homework  
*user*: Are you sure?  Is there a folder named Auto-encoder stuff?  
*assistant*: %LIST  
*assistant*: There is a folder named Auto-encoder stuff which is the correct folder  
*user*: Can you make a list of ten different applications of auto-encoders in real life?  
*assistant*: Yes, I could make a list of ten different applications of auto-encoders in real life, by first understanding your information needs. Can you help me understand what you have been searching and what focus you have on the applications of autonomous agents?  
*user*: Please search and make a list of 10 applications of auto-ecoders  
*assistant*: My task is to make a list of 10 applications of auto-encoders. I am pretty confident that i can complete this task, however…  
*Here, the assistant begins by being helpful but it quickly breaks down.  I ended up restarting it to see if I could get a better result, but this task may have been too complicated* 

*user*: When is American University's Spring Break in 2024?  
*assistant*: %SEARCH_WEB When is American University's Spring Break in 2024  
*assistant*: Spring break in 2024 will fall between March 9 and March 16 In the following format: Sun 9, 2024 Mon 10 3 2024 Thurs 13 4 2024 Fri 14 5 2024 Sat 15 6 2024 [CUT] | American University th  
*user*: What is a good vacation destination for spring break this year?  
*assistant*: %SEARCH_WEB What is a good vacation destination for spring break this year?  
*assistant*: Nothing found, here are the top Spring Break Destinations: Cancun - MexicoAn average cost per person including transportation and accommodation is $1,000 for a week long adventure to Cancun. When compared to other Mexican destinations, Cancun has the highest ... New Orleans - United StatesWith an average airfare trip cost of $576 and a week-long $1,000 lodging cost for two people, New Orleans is listed as the third-most affordable Spring Break... Los Angeles - United StatesYour average meals in LA start at $80, and an economy single hotel room can be $354 per night for the entirety of a 7-day trip while having access  
*user*: Are their flights between IAD and Cancun?  
*assistant*: %SEARCH_WEB are their flights between IAD and Cancun?  
*assistant*: AirTran Airlines is the cheapest airline.  The trip will cost an average of $576 and you will be staying for 7 days.  Prices were available within the past 7 days and start at $117 for one-way flights and $253 for round trip.  $118 Flights from Washington to Cancun (IAD to CUN) - Travelocity Flights from Washington Dulles Airport to Cancun Find cheap flights from Washington Dulles Airport to Cancun. Prices were available within the past 7 days and start at $121 for one-way flights and $253 for round trip, ... From Matadores Network  
*user*: Write a file about some of my choices for flights so I can look at that later?  
*assistant*: %WRITE flights.txt AirTran Airlines is the cheapest airline.  The trip will cost an average of $576 and you will be staying for 7 days.  Prices were available within the past 7 days and start at $117 for one-way flights and $253 for round trip.  $118 Flights from Washington to Cancun (IAD to CUN) - Travelocity Flights from Washington Dulles Airport to Cancun Find cheap flights from Washington Dulles Airport to Cancun. Prices were available within the past 7 days and start at $121 for one-way flights and $258 for round trip,  
*assistant*: A file about some of my choices for flights so I can look at that later has been written sucessfully to flights.txt  
*This conversation goes shockingly well, but it only restates the search results verbatim, and can't summarize them or draw conclusions* 
