library(ggplot2)
library(dplyr)
library(moderndive)
library(readr)
library(infer)
library(knitr)

# The data set that I chose to work with is about the game League of Legends and I got it off of Kaggle.com. League of Legends is an online, team-based strategy game where there are two teams (blue and red) that fight to destroy the others base. Each team consists of five players who use champions which have different abilities in the game to accomplish this task of destroying the base. 

# This game has a competitive mode called "ranked" where wins give you points that help you climb the ranking ladder. 

# This data set contains information about both the red team and blue teams in high diamond ranked League of Legends games during the first ten minutes of the game. 

# I will be doing analysis on this data to determine: what early game (first ten minutes) decisions/stats help contribute to the blue team winning in ranked League of Legends?

# Lets first read in our data. 
```{r}
high_diamond_ranked_10min <- read_csv("high_diamond_ranked_10min.csv")
```
# I wanted to re-name this data frame to something more efficient to work with. Then, since this data set has over 9,000 entries, I wanted to look over a smaller section of the data to determine what questions I should be asking. 
```{r}
ranked_game_data <- high_diamond_ranked_10min
```

```{r}
head(ranked_game_data)
```


# My interest in this data set is to see what early game decisions the Blue team made that might have impacted the outcome of the game,
# whether they lost or won. 

# I added two columns to show which team (Red or Blue) won and which team got the first blood (first kill of the game).
```{r}
ranked_game_data $win <- factor(ranked_game_data$blueWins, levels = c(0, 1), labels = c("Red team", "Blue team"))
ranked_game_data $firstBlood <- factor(ranked_game_data$blueFirstBlood, levels = c(0, 1), labels = c("Red team", "Blue team"))
```


# I then used **descriptive statistics** to ask: How many total wins did the blue team have?
```{r}
ranked_game_data %>% count(blueWins)
```

# The Blue team had 4,930 wins and 4,949 loses.

# Next, I want to do some **data wrangling** to determine the average amount of kills the blue team had when they won and lost.
```{r}
avg_kills <- ranked_game_data %>%
  group_by(blueWins) %>%
  summarize(average_kills = mean(blueKills, na.rm = TRUE))

avg_kills
```
# This code is grouping by the Blue wins and then finding the mean of the number of kills blue got in each game. The 1 under the title "blueWins" means that they won and the 0 means that they had lost. 

# The average amount of kills when the blue team won was around 7.20 and when they lost it was around 5.17.

# Then, I created two plots to better **visualize** this!
```{r}
ggplot(ranked_game_data, aes(x= win, y=blueKills))+
  geom_col()+
  labs(x= "Winning Team", y= "Blue Kills")

ggplot(data = ranked_game_data, mapping = aes(group = blueWins, x = blueKills, y = blueWins)) +
  geom_boxplot()+
  labs(x = "Blue Kills", y= "Blue Wins")
```
# The bar plot shows the total kills the Blue team had when either the Blue or Red team won. 
# The box plot is showing the Blue team's average kills for each game when either the Blue or Red team won. 

# Next, I want to see if having the first blood in the game has an impact on which team wins. 
# I used the new column that I created earlier via **data wrangling** called "firstBlood" to create a **visualization** of first bloods and wins for both teams.
```{r}
ggplot(ranked_game_data) +
  aes(x = win, fill = firstBlood) +
  geom_bar(color="black", position="dodge") +
  labs(x = "Winning team", y = "Count", fill = "Team Having First Blood")
```

# Now, it is shown that when either the Blue or Red team won, most of the time that team also had the first kill. Meaning, getting the first blood in the game might actually influence the outcome. 

# I will see if the champion level relates to whether the blue team won or lost.
# Next, I used **descriptive statistics** to find the median level of blue team players in the games and **visualize** it with a bar chart.

```{r}
median_AvgLevel <- median(ranked_game_data$blueAvgLevel)

ggplot(ranked_game_data, aes(x= blueAvgLevel, y= blueWins))+
  geom_col()+
  labs(x="Average Level", y="Wins", title = "Blue Team Wins vs. Level")+
  geom_vline(aes(xintercept=median_AvgLevel), linetype="dashed", color = "red")
```

# Now, it is shown that most wins for the blue team had players with champions that had a median level of 7 in the first 10 minutes of the game. 

# This makes me ask: Do higher level champions get more kills that might influence the outcome of the game?
# I used a scatter plot to **visualize** the correlation. 

```{r}
ggplot(ranked_game_data, aes(x= blueKills, y= blueAvgLevel))+
  geom_point()+
  labs(x="Number of Kills", y="Average Level", title = "Blue Kills vs Blue Level of Champions")
```


# Then, I added a best fit line **fit a linear model** to better see this correlation. I also calculated the correlation. 
```{r}
ggplot(ranked_game_data, aes(x= blueKills, y= blueAvgLevel))+
  geom_point()+
  geom_smooth(method = 'lm', se = FALSE)
  labs(x="Number of Kills", y="Average Level", title = "Blue Kills vs Blue Level of Champions")
  
get_correlation(ranked_game_data, blueKills ~ blueAvgLevel)
```

# This shows that there is a positive correlation (0.435) between the kills that a player gets and their champion level. 
# So, we could say that if a player got more kills in the first ten minutes, they are going to level up to a higher level and that has a 
# chance of influencing the outcome of the game. 

# I want to **test a hypothesis** to see if the amount of kills the blue team gets in the first ten minutes is effecting if they won. 
# My null hypothesis is: there is no correlation between the amount of kills the blue team gets in the first ten minutes and if they won.
# My alternative hypothesis is that there is a correlation between the amount of kills the blue team gets in the first ten minutes and if they won.

```{r}
obs_stat_blue <- ranked_game_data %>% 
  specify(blueKills ~ win) %>%
  calculate(stat = "diff in means", order = c("Blue team", "Red team"))

null_distribution_blue <- ranked_game_data %>% 
  specify(blueKills ~ win) %>% 
  hypothesize(null = "independence") %>%
  generate(reps = 1000, type = "permute") %>%
  calculate(stat = "diff in means", order = c("Blue team", "Red team"))

p_value_blue <- null_distribution_blue %>%
  get_p_value(obs_stat = obs_stat_blue, direction = "both")

visualize(null_distribution_blue) + 
  shade_p_value(obs_stat = obs_stat_blue, direction = "both")

p_value_blue
```
# With the p-value being zero, this indicates that the observed number of kills in the actual data is significantly different from what I would expect if there was no effect of winning or losing on the number of kills the team got in the first ten minutes.  

# Thus, I would reject the null hypothesis, concluding that there's evidence in the data to suggest that the number of kills a team gets in the first ten minutes is associated with whether they win or lose.

# Overall, from my observations with this data, I think that if the Blue team has more kills, a higher champion level, and the first blood in the first ten minutes of the game, they will win the game. 
