
working_dir <- getwd()
dirp_lahman <- "C:\\Users\\micha\\OneDrive\\Documents\\data\\lahman_1871-2023_csv\\lahman_1871-2023_csv\\"


fp_teams <- file.path(dirp_lahman, "Teams.csv")
teams <- read.csv(fp_teams)

teams <- subset(teams, yearID > 2000)

par(mfrow = c(2, 2))  # 2 rows, 2 columns

aggregateHR <- aggregate(HR ~ yearID, data = teams, sum)
plot(aggregateHR$yearID, aggregateHR$HR, type = "l",
     main = "Total Home Runs per Year",
     xlab = "Year", ylab = "Total HR", lwd = 2, col = "purple")


teams$RunsPerGame <- teams$R / teams$G
avg_runs <- aggregate(RunsPerGame ~ yearID, data = teams, mean)
plot(avg_runs$yearID, avg_runs$RunsPerGame, type = "l",
     main = "Average Runs/Game Over Time",
     xlab = "Year", ylab = "Runs/Game", lwd = 2, col = "darkgreen")


teams$HR_per_Game <- teams$HR / teams$G
teams$Wpct <- teams$W / teams$G
plot(teams$HR_per_Game, teams$Wpct,
     main = "HR/Game vs Winning %",
     xlab = "HR per Game", ylab = "Winning %", pch = 19, col = "orange")
abline(lm(Wpct ~ HR_per_Game, data = teams), col = "red", lwd = 2)


teams$SO_per_Game <- teams$SO / teams$G
avg_SO <- aggregate(SO_per_Game ~ yearID, data = teams, mean)
plot(avg_SO$yearID, avg_SO$SO_per_Game, type = "l",
     main = "Avg Strikeouts/Game Over Time",
     xlab = "Year", ylab = "Strikeouts/Game", lwd = 2, col = "blue")


par(mfrow = c(1, 1))
