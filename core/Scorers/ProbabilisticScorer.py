# TODO

# this scorer is supposed to calculate the average number of solutions lef
# after a guess based on the size of the groups

# for example, a guess with groups 1, 1, 1, 1, 1, 45 has 50 total
# 4 groups with propability 1 / 50 and 1 group with probability 9 / 10

# this means the average number of solutions left is 4 * (1 / 50) + 45 * (9 / 10) = 40.6

# compared to a guess with less groups (so you would think its worse)
# with groups 10, 10, 10, 10, 10 has a total of 50 as well
# but the average number of solutions left is 10 which is much better