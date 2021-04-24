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
- Checking for relationship between compensation and age with a linear regression graph with the same above filters:

![image](https://i.imgur.com/EQW5zv4.png)  
  
*Converted Comp* means compensation converted to USD.  
So there definitely seems to be a consistent correlation between age/experience and pay increase, fairly dramatically so.
- Now let's see for all language combos, all education levels, and all countries. 
  We'll even color code based on if someone answered yes or no to *"do you like to code as a hobby?"*:  
    
![image](https://i.imgur.com/evYXaf7.png)  
  
Interesting divergence from hobbyists as people get older! Maybe more passion means desire to improve (since it happens naturally from enjoyment), which means better pay over time?  
  
- But let's filter the above to USA only:  
  
![usa only](https://i.imgur.com/uQaPQKW.png)  
  
Considerably higher averages across the board as we might have expected. We've got some things going for us over here haha.  
  
More to come.