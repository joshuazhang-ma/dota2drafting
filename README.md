# dota2drafting

Project started: Summer 2020

Goal: Create a recommendation system for a team captain to maximize their winning chances during the drafting phase of a match.

Context: In a professional match in DotA 2, two teams of five players each enter an arena, with the ultimate objective being to destroy the command tower of the other team. Each team has one captain, who chooses the characters that each of his team members will control during a given match. Characters are unique, meaning only one of each character can be selected per match. There is a non-negotiable sequence for drafting, which was instituted to marginalize the advantages of pick order. In addition to picking characters, both teams also ban characters. A banned character cannot be chosen to represent either team for the given match. All picks and bans are public information, so both teams have knowledge of which characters are picked, banned, and available. The sequence of bans and picks are as follows:

# Ban Phase 1

1b -> 2b -> 1b -> 2b ->                 

# Pick Phase 1

1p -> 2p -> 1p -> 2p ->                 

# Ban Phase 2

1b -> 2b -> 1b -> 2b -> 1b -> 2b ->     

# Pick Phase 2

2p -> 1p -> 2p -> 1p ->                 

# Ban Phase 3

1b -> 2b -> 1b -> 2b ->                 

# Pick Phase 3

1p -> 2p                                

Key:

[T][p/b]

T = team number

p/b = pick or ban

Subject Expertise: After every major tournament called The International, in which millions of dollars will be awarded to the winner, the game will activate a game patch that usually drastically changes the gameplay. This event promotes the need for constant evolution in strategies and training for the players. Because players have limited time to practice with their team, an important factor to consider for a team coach is: which characters should each player commit time to learn and perfect for competitive play?

Along the same note, changes in gameplay often enhance the effectiveness of one character and hinder others. The recommendation system should take into account the relative performance of a character against other characters, from head-to-head up to five on five. Along the same argument, some players handle certain characters better than others. This should also be reflected in the recommendation system.

There are broad strategies that can be employed to win in DotA 2, and some characters are better suited to a strategy than another. The reecommendation system should also analyze the synergy between characters for certain broad strategies, and highlight them. 

Business Analyst Question:
The manager of a team would like to know how to coach his team members so that the team has the best chance to win the multi-million dollar prize at the end of The International.
