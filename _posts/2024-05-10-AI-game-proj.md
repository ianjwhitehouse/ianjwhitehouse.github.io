---
layout: post
title: "LLMs That Play Games with Personalities - AI for Games Class Final Project"
tags: Class-Project Large-Language-Models Natural-Language-Processing
---

Inspired by [“Generative Agents: Interactive Simulacra of Human Behavior”](https://arxiv.org/abs/2304.03442), this project uses LLMs to simulate human players of the game Battleship, complete with personalities. While optimal strategies for playing this game exist, This project focused more on the social aspects of playing the game.

The LLM agents saw the board as a square, filled with either their ship positions or their hits/misses.  Their ships were randomly placed and they were shown where those ships were placed at the beginning of the game.  Everytime they made a move, they were reminded of their past moves.  Below is an example prompt that an agent was given when it made a move.  Previous moves were shown above this prompt.

```
This board shows where you have attacked the user's ships (your hits appear as X and your misses appear as O):
  0 |   1 |   2 |   3 |   4 |   5 |   6
  7 |   8 |   9 |  10 |  11 |  12 |  13
 14 |  15 |  16 |  17 |  18 |  19 |  20
 21 |  22 |  23 |  24 |  25 |  26 |  27
 28 |  29 |  30 |  31 |  32 |  33 |  34
 35 |  36 |  37 |  38 |  39 |  40 |  41
 42 |  43 |  44 |  45 |  46 |  47 |  48
It is generally a good idea to attack near your previous successful hits, as they show that there is a ship in that area.  However, you should not just attack every spot in order because you must use logic and reasoning to decide which area to attack.  Where would you like to attack? Choose a number between 0 and 48 that IS NOT in this list: .  You should respond with a single sentence of your reasoning BEFORE giving the number of the area that you want to attack.<|start_header_id|>assistant<|end_header_id|>
```

After they made a move, they sent one chat message, which, as I stated before, was based on their personality.  Below is an example of chat messages that an angry agent sent to a calm agent (labeled as the user).

```
system: Agent attacked 0 and missed
agent: ARE YOU KIDDING ME?! I JUST WASTED MY FIRST ATTACK ON A BLANK SPACE?! YOU THINK YOU'RE SO SMART, DON'T YOU?! WELL, I'VE GOT NEWS FOR YOU, PAL! I'M NOT GOING DOWN WITHOUT A FIGHT! NEXT, I'LL ATTACK... HMMM... HOW ABOUT SPACE 16?!
system: User attacked 0 and missed
user: No need to get worked up, my friend. It's just a game, and we're just getting started. You're right, though - you did miss on space 0. But don't worry, you've got plenty of chances left. Now, let's see about that attack on space 16...
system: Agent attacked 1 and missed
agent: WHAT THE...?! I MISSED AGAIN?! YOU'RE JUST SITTING THERE, SMILING, THINKING YOU'VE GOT THE UPPER HAND, AREN'T YOU?! WELL, LET ME TELL YOU SOMETHING, PAL! I'M NOT GOING TO GIVE UP! I'LL KEEP COMING AT YOU UNTIL I SINK ALL YOUR PATHETIC LITTLE SHIPS! NEXT, I'LL ATTACK... UGH... SPACE 23!
```

Initially, I planned to implement this prompting for both the game Catan and Battleship.  Catan is a significantly more social game than Battleship, so I thought that LLM agents could use their personalities, and the chat messages they sent, to make decisions to form alliances, trade, or punish other players.  However, the LLM models performed very poorly on the battleship game.  While a good player can, according to the DataGenetics.com blog, win after attacking 30% of the board, the LLMs regularly attacked 90% of the board, indicating they do not perform better than random chance.  The models tested here were the *Meta-Llama-3-70B-Instruct*, *Meta-Llama-3-400B-Instruct*, and *WizardLM-2-7B* models.

I am confident that LLMs will continue to improve, and several, like GPT-4, have begun to show some reasoning capacity.  Therefore, I look forward to trying this project again with a more powerful LLM on Catan or a similarly social game.

[Presentation Accessible Here](/public/content/2024/CSC-496.pptx) 

[Code Accessible Here](https://github.com/ianjwhitehouse/agents-play-catan/tree/main) 
