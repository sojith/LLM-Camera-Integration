# LLM-Camera-Integration
This is an attempt at using LLMs to call functions , but without the "function calling" or "tool calling" integrations that the AI companies give us developers

I find these "function calling" integrations, atleast at this time, unreliable (As is evident here - https://gorilla.cs.berkeley.edu/leaderboard.html)
They aren't as accurate, and when used the LLMs refuse to answer general queries sometimes

 As is evident in the code, I use the system prompt to LLMs to help me with calling the right function. I am still refining this technique. It is quite possible that in this process o\I might hit a ceiling. Perhaps by then the accuracy of "tool calling" integrations will have become far better than they are now.

 The technicque is quite simple.
 I have created a json, at line 155. It relates a question that the user might have, to a function name. This json is then used at the system prompt at line 167
 If the user's question is similar in verbiage to any of the "Key"s in this json, then the LLM's output would be the corresponding Value of that Key.
 The code then takes this output, and compares it with the function_map I have provided at line 148.
 Once the code determines the correct function name, it calls that function (line 183, 184)
 
 Quite straight forward from there, just be sure that the function returns the output to the LLM. This is so that the LLM can keep a track of the function called.

 
