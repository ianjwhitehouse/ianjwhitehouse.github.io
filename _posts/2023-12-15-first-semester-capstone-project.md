---
layout: post
title: "Supervised Intelligent Agents - First Semester Capstone Project"
tags: Class-Project Decision-Making Autonomy
---

For my first capstone project during my senior year, I worked on designing an autonomous agent to play a game of tag against another agent.  The premise of this project was simple: I wanted to build an AI system that could be trained using supervised learning and then play a semi-complex game using only visual input.  This project was primarily inspired by Yann LeCun's essay ["A Path Towards Autonomous Machine Intelligence"](https://openreview.net/pdf?id=BZ5a1r-kVsf) and his [talk at Northeastern University](https://www.youtube.com/watch?v=mViTAXCg1xQ). 

![](/public/content/2023/inference.svg)
*Inference pipeline for the autonomous agent* 

My model uses three fully-connected neural networks: the encoder, the predictor, and the cost calculator.  The encoder encodes an image frame as input to generate a latent representation, the predictor takes a latent representation and an action state (i.e., the current positions of a joystick) and calculates the latent representation of a future frame, and the cost calculator takes a latent representation and calculates the discomfort the agent feels in that frame.  I tried to base my model on the Joint-Embedding Predictive Architecture discussed in LeCun's paper.  In this architecture, the predictor's role is made less complicated because it only has to predict a latent representation instead of a raw input, and, theoretically, the encoder filters out extraneous information from the latent representation. 

![](/public/content/2023/run_lens.png)
*Lengths of the tag game in different generations* 

I trained the model on my tag game by first running a completely random agent, which was Generation 0, and training Generation 1 based on it.  Each generation was trained on between 7.5 and 12.5 minutes of the previous generation's gameplay.  Because the tagger agent is slightly faster than the agent it is chasing, each generation should last longer than the previous one (to a point), and each generation's runs should end with a tag more often than its previous generation.  These statements were true for every generation except generation 3, and, in the presentation below, some GIFs show the agent acting strategically.  However, as I trained more generations, they began to perform worse, which was unexpected and made me ask if some element of AI data cannibalization was occurring, such as in AI art. 

![](/public/content/2023/run_ends.png)
*Ending states of the tag game in different generations* 

I am excited for the opportunity to expand on this project next semester.  More specific information is in the posts below, including the GIFs of the agents performing the specific strategies that I mentioned above. 

[Presentation Accessible Here](/public/content/2023/capstone_1.pptx)  

[Report Accessible Here](/public/content/2023/capstone_1.pdf) 