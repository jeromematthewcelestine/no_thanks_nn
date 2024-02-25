library(tidyverse)

df <- read_csv('2024-02-18_no_thanks_training_data_03.csv', col_names = FALSE)

df_train <- df %>% slice_sample(prop = 0.75)
df_test <- df %>% anti_join(df_train)

nrow(df_train)
nrow(df_test)

write_csv(df_train, '2024-02-18_no_thanks_training_data_03_train.csv', col_names = FALSE)
write_csv(df_test, '2024-02-18_no_thanks_training_data_03_test.csv', col_names = FALSE)
