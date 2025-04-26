
library(dplyr)


dirp_lahman <- "C:\\Users\\micha\\OneDrive\\Documents\\data\\lahman_1871-2023_csv\\lahman_1871-2023_csv\\"
teams <- read.csv(file.path(dirp_lahman, "Teams.csv"))
parks <- read.csv(file.path(dirp_lahman, "Parks.csv"))

names(parks)


teams_modern <- subset(teams, yearID >= 2000)

head(teams_modern)


hr_per_park <- teams_modern %>%
  group_by(park) %>%
  summarise(
    avg_HR_per_year = mean(HR, na.rm = TRUE),
    num_seasons = n()
  ) %>%
  filter(!is.na(park) & num_seasons >= 3)  # Keep parks with at least 3 seasons for stability

# Merge with Parks info to get readable names
hr_per_park <- hr_per_park %>%
  left_join(parks, by = c("park" = "parkkey"))


hr_per_park <- hr_per_park %>%
  select(park, parkname, city, state, avg_HR_per_year, num_seasons)

hr_per_park$HR_quintile <- ntile(hr_per_park$avg_HR_per_year, 5)  # 5 quintiles

print(hr_per_park)


summary_table <- hr_per_park %>%
  group_by(HR_quintile) %>%
  summarise(
    avg_HR = mean(avg_HR_per_year),
    min_HR = min(avg_HR_per_year),
    max_HR = max(avg_HR_per_year),
    n_parks = n()
  )

print(summary_table)


boxplot(avg_HR_per_year ~ HR_quintile, data = hr_per_park,
        main = "Home Runs by Ballpark Quintile",
        xlab = "Quintile (1 = lowest HR parks, 5 = highest HR parks)",
        ylab = "Average HR per Year",
        col = "lightblue", border = "darkblue")





