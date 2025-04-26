working_dir <- getwd()
dirp_lahman <- "C:\\Users\\micha\\OneDrive\\Documents\\data\\lahman_1871-2023_csv\\lahman_1871-2023_csv\\"

fp_teams <- file.path(dirp_lahman, "Teams.csv")

teams <- read.csv(fp_teams)

subset_teams <- subset(teams, yearID > 2000)[ , c("teamID", "yearID", "lgID", "G", "W", "L", "R", "RA")]

subset_teams$RD <- with(subset_teams, R - RA)
subset_teams$Wpct <- with(subset_teams, W / (W+L))

plot(subset_teams$RD, subset_teams$Wpct, xlab="run differential", ylab="win pct.")

linfit <- lm(Wpct ~ RD, data=subset_teams)
lm(formula=Wpct~RD, data=subset_teams)
abline(a=coef(linfit)[1], b=coef(linfit)[2], lwd=2)


coef_vals <- coef(linfit)
eqn <- paste0("Wpct = ", round(coef_vals[1], 3), 
              " + ", round(coef_vals[2], 3), " * RD")
text(x = min(subset_teams$RD), 
     y = max(subset_teams$Wpct), 
     labels = eqn, 
     pos = 4)


subset_teams$linWpct <- predict(linfit)
subset_teams$linResiduals <- residuals(linfit)


mean_resid <- mean(subset_teams$linResiduals)
linRMSE <- sqrt(mean(subset_teams$linResiduals ^ 2))
within_1rmse <- nrow(subset(subset_teams, abs(linResiduals) < linRMSE)) / nrow(subset_teams)
within_2rmse <- nrow(subset(subset_teams, abs(linResiduals) < 2 * linRMSE)) / nrow(subset_teams)

plot(subset_teams$RD, subset_teams$linResiduals,
     xlab = "Run Differential (RD)", ylab = "Residual",
     main = "Residuals vs RD")

abline(h = 0, lty = 2)  # optional: add horizontal line at 0 residual

text(x = min(subset_teams$RD), 
     y = max(subset_teams$linResiduals), 
     labels = paste0(
       "Mean Residual = ", round(mean_resid, 4), "\n",
       "RMSE = ", round(linRMSE, 4), "\n",
       "% within 1 RMSE = ", round(100 * within_1rmse, 1), "%\n",
       "% within 2 RMSE = ", round(100 * within_2rmse, 1), "%"
     ),
     pos = 4, cex = 0.8)

