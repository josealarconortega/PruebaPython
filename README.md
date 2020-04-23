# Eduardo Iragorri

## Mummy-Money

The famous Mummy from horror folklore always wanted to be rich! Thus, he came up with a plan to accomplish his goal. Knowing that the world is full of naive people, and in order to pay homage to his Egyptian roots, he decided to use a Pyramid Scheme to easily and quickly generate wealth 😊.

The Mummy created a new currency called Mummy Money (MM$) and founded the **“Mummy Money, Get Rich Quick Program!”** for ambitious (and unwary investors) and started with 10 members chosen randomly from the general population. The mummy money investors selected had the following attributes:

1. **Innocence:** float between 0 and 1
2. **Experience:** float between 0 and 1
3. **Charisma:** float between 0 and 1

### How the Pyramid Scheme Works

Each investor pays MM\$500 to join the program and receives MM\$100 per any new member they recruit.

The probability of each member finding another member to invest in the Mummy Money program is: 

*Experience\*Charisma\*(1-math.log(X,10)) where X are direct members recruited* 
Note: math.log(X,10) = logarithm base 10 of X 

**IMPORTANT: The logarithm base N of 0 is not defined, so to keep the same expected behavior, I'll replace X with X+1 in the formula to avoid this situation.**

The probability that a candidate accepts the offer is: 

*Innocence\*(1-Experience))* 

The maximum number of weeks that a member can remain in the program without recovering their investment is: 

*math.floor((1-Innocence)\*Experience\*Charisma\*10)* 

If their investment has not been recovered the member will be eliminated from the program.

#### Application Specifications

As an experienced application developer, the Mummy requests that YOU create an app to help him manage his Mummy Money program. The following are his specifications for the app: 

1. Model the Pyramid Scheme so that: 
    * The Mummy is the only at the top of the pyramid 
    * The attributes of each investor can be stored 
    * Each investor is assigned a unique id 
    * Each member can see their Mummy Money in real time (including the Mummy) 
    * The follow metrics can be stored and calculated each week: 
        - Member tree
        - New members 
        - Members leaving 
        - Mummy Money for each member 
2. Can generate a population of n investors using a: 
    * [Uniform random distribution](https://en.wikipedia.org/wiki/Uniform_distribution_(continuous)) for each attribute 
    * [Normal random distribution](https://en.wikipedia.org/wiki/Normal_distribution) for each attribute 
3. Can simulate a week’s membership every n second(s). To simulate, each n second(s) pick each active member except the Mummy and: 
    * Generate a float random number between 0 and 1 for each member 
    * If the number is greater than the member’s probability to recruit a candidate, pick a new investor from the population of potential investors 
    * Generate a random, float number between 0 and 1. If the generated number is greater than the probability for a candidate to accept the offer, mark them as a new member.

        **IMPORTANT: it only makes sense that the generated number must be less than the actual probability for a candidate to accept the offer, and that's what the program will do**

    * After running this simulation for all members, mark the members that will leave the program as inactive.
4. The Mummy can see when to terminate the program and escape using a simple dashboard. The Dashboard must have: 
    * Total population 
    * Total members 
    * New Members for current week 
    * Members leaving during current week 
    * Mummy Money earned by the Mummy 
    * Average Mummy Money for each member

#### Technical Requirements

The app must be developed with the following technical requirements: 

- Use Python 3.7 
- Use a simple SPA (Single Page Application) framework for the dashboard like [Vue](https://vuejs.org/).
- Use a git repository from scratch (you can use Github, Gitlab or any free SaaS) 
  
You are free to choose any framework/libraries/database that you want. Try to keep it simple and use simple local databases like [SqlLite3](https://docs.python.org/3/library/sqlite3.html) or [TinyDB](https://github.com/msiemens/tinydb).

**The goal is be able to run the simulation and watch the status in real-time using the Dashboard.** You can use either a Pull or Push protocol to update the dashboard.

#### Evaluation Criteria

You will be evaluated based on the following factors:

- Git good practices
- Python Good Practices
- Tests and code checks
- [12factors](https://12factor.net/)

#### Project Deliverables

The deliverables of this project are:

- Provide install and use instructions
- Provide Git repository access
- Provide an app package (Use of Docker and Docker Compose is permissible for simplicity but is not mandatory)