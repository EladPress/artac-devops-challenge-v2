# AI Workflow Documentation
I used Claude Code with the Pro subscription as an extension within VSCode.

It took me a few days to comb over anything I think I can improve and implement in this project, Claude helped me save many hours by helping me implement both things i'm already familiar with and could quickly understand what Claude gives me, such as Semantic Release and Dockerfiles, but it also helped me implement things i'm not as familiar with, such as GitHub Actions and AWS SSM.

Specific examples of prompts that worked well for me:
1. Conceptual questions about the tooling: Verifying i'm following best practices and understanding the code Claude gives me.
2. Is there anything i'm missing? Claude had the context of this assignment and could find flaws in the application that I could not.
3. Fix typos I made while documenting. I type too fast for me to notice mistypings :)

I prefer simplicity over convoluted solutions, and while Claude gives good enough solutions compared to other AI models I tried, there were times when I had to doubt its solution and point it somewhere else. A good example of this is the CI process. At first Semantic Release ran on a different workflow which was followed by the rest of the CI/CD process. To make both workflows run sequentially and move variables from one workflow to another, Claude offered me complicated options, and I decided to go simple and merge both workflows into one.
Of course Claude experiences context bloat as with every AI model, so once I noticed Claude started hallucinating, I started clearing the context every once in a while.