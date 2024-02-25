library(tidyverse)

df <- read_csv('2024-02-18_no_thanks_training_data_03.csv', col_names = FALSE)

samp1 <- df %>% slice_sample(n = 1000)
write_csv(samp1, '2024-02-19_no_thanks_training_data_04.csv', col_names = FALSE)

samp1 %>% pull(X25) %>% mean()

mean(df %>% duplicated())
any(df %>% duplicated())
df %>% duplicated()

df %>% select()

df %>% head()

library(ggplot2)

df %>% group_by(X21) %>%
  summarize(mean = mean(X25))

mod <- lm(data = df, X25 ~ X21 + X22 + X23 + 
            X1 + X2 + X3 + X4 + X5 + 
            X6 + X7 + X8 + X9 + X10 + 
            X11 + X12 + X13 + X14 + X15 + 
            X16 + X17 + X18 + X19 + X20)
mod
summary(mod)

df %>% 
  group_by(X5) %>%
  summarize(mean = mean(X25))

df %>% group_by(X25) %>% summarize(n())
