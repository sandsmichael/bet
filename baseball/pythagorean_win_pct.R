working_dir <- getwd()
dirp_lahman <- "C:\\Users\\micha\\OneDrive\\Documents\\data\\lahman_1871-2023_csv\\lahman_1871-2023_csv\\"

fp_teams <- file.path(dirp_lahman, "Teams.csv")

subset_teams <- subset(teams, yearID > 2000)[ , c("teamID", "yearID", "lgID", "G", "W", "L", "R", "RA")]
subset_teams$RD <- with(subset_teams, R - RA)
subset_teams$Wpct <- with(subset_teams, W / (W+L))
subset_teams$pytWpct <- with(subset_teams, R^2/(R^2+RA^2))
subset_teams$pytResiduals <- subset_teams$Wpct - subset_teams$pytWpct
pytRMSE <- sqrt(mean(subset_teams$pytResiduals^2))


# Pythagorean vs Linear expectation
subset_teams$linResiduals <- residuals(linfit)
subset_teams$pytResiduals <- subset_teams$Wpct - subset_teams$pytWpct

plot(subset_teams$RD, subset_teams$linResiduals,
     xlab = "Run Differential (RD)",
     ylab = "Residual",
     main = "Comparison of Linear vs Pythagorean Residuals",
     col = "blue", pch = 16)
points(subset_teams$RD, subset_teams$pytResiduals,
       col = "red", pch = 17)
abline(h = 0, lty = 2)
legend("topright", legend = c("Linear Model Residuals", "Pythagorean Residuals"),
       col = c("blue", "red"), pch = c(16, 17))



# Residual Comparison
residuals_df <- data.frame(
  Residuals = c(subset_teams$linResiduals, subset_teams$pytResiduals),
  Model = rep(c("Linear Model", "Pythagorean Expectation"), each = nrow(subset_teams))
)

boxplot(Residuals ~ Model, data = residuals_df,
        main = "Comparison of Residuals",
        ylab = "Residual",
        col = c("lightblue", "lightgreen"),
        border = "darkblue",
        notch = TRUE)
abline(h = 0, lty = 2) 



# Calculate the derivative (marginal impact of 1 extra run on wins)
subset_teams$derivative <- with(subset_teams, (2 * G * R * RA^2) / ( (R^2 + RA^2)^2 ))
subset_teams$runs_per_win <- 1 / subset_teams$derivative

head(subset_teams[c("G", "R", "RA", "runs_per_win")])


