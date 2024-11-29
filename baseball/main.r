working_dir <- getwd()
fp_teams <- file.path(working_dir, "code\\sports\\baseball\\data\\lahman_csv\\Teams.csv")
teams <- read.csv(fp_teams)
print(teams)

# wins = teams[["W"]]
wins = teams[, c("name", "W") ]

print(wins)