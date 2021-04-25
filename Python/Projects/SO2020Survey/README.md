# Analyzing Stack Overflow 2020 survey
## Interesting bits so far:

- Finding average incomes with:
     - Countries with 25 or more surveys taken.
     - Between $10k to $150k annual USD converted income.
     - Age 25 to 45.
     - Python mentioned.
     - No college degree.
```
Country
United States     $100,103.26
United Kingdom     $71,995.90
Sweden             $68,489.68
Canada             $67,817.88
Germany            $55,816.58
Netherlands        $55,214.63
Spain              $44,835.11
Italy              $41,535.97
Poland             $35,367.55
Brazil             $25,300.00
```
Well now you know *where* you want to work!
- Checking for relationship between compensation and age with a linear regression 
  graph with the same above filters. 
  *Converted Comp* means compensation converted to USD:
![image](https://i.imgur.com/EQW5zv4.png)  

So there definitely seems to be a consistent correlation between age/experience 
and pay increase, fairly dramatically so.
- Now let's see for all language combos, all education levels, and all countries. 
  We'll even color code based on if someone answered yes or no to 
  *"do you like to code as a hobby?"*,
   with a "no" definitely being a euphemism for "I'm only here because it pays well, 
  don't call me after 6":
![image](https://i.imgur.com/evYXaf7.png)  
  
But isn't that interesting? A divergence in pay from hobbyists as people get older! 
I could extrapolate with some confidence that more passion means desire to 
improve naturally (since it happens naturally from enjoyment), which means better 
pay over time for better skills, in lieu of plateauing in familiarity and the 
comfortability that brings from being good at what you already know.  
  
In which case, those that are only developers for the pay would *still* stand to 
benefit from trying to enjoy it as a hobby in their free time too, if higher pay 
really is their ultimate goal. But we all know people get comfortable after awhile,
and then change and improvement become anxiety-inducing, and so they stop and forget
what it's like to improve and push. They forget the great feelings it brings; what got them
to that comfortable position in their current life or situation or job or craft 
in the first place. Don't fall into that trap!  
If you feel anxiety about suddenly
needing to do something new or unfamiliar or uncomfortable, instead **push** into it 
and you'll likely see the anxiety and fear was never real or justified to begin with. 
Then it feels better, you conquer a fear in your mind, and you accomplish things once
again. That even comes down to wrestling something simple like procrastination. 
It's the same mindset, same anxiety.  
  
Anyway, let's keep going!
  
- The previous graph was pay averages for all countries, but let's filter the 
  above to USA only:
![usa only](https://i.imgur.com/uQaPQKW.png)  
  
Considerably higher averages across the board as we might have expected. 
We may not have health insurance in the US but at least we pay our developers well! Haha...
  
- So, what's the population like in software development these days?
![genders](https://i.imgur.com/K14GsEH.png)
  
Probably unsurprising to most, but maybe not, is that the population is **overwhelmingly** 
Male. Even sites like Reddit will have a more even split between male and female users
closer to 50/50, but developers on Stack Overflow are **hugely** male.  
  
- And for sexuality:
![sexuality](https://i.imgur.com/gi0Li8V.png)
  
Developers are overwhelmingly straight, though this particular difference is more 
likely a reflection of humans overall rather than of developers.

If we setup some filters to remove some majorities from the above, we can see 
some interesting comparisons.
  
- Our sexual minorities in Stack Overflow 2020:  
![no_hetero](https://i.imgur.com/ek6VzVd.png)
  
- And our gender minorities in Stack Overflow last year:
![non_binary](https://i.imgur.com/cZGn2kj.png)
  
More cool stuff to come.