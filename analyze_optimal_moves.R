library(tidyverse)

df <- read_csv('data/2024-02-20_no_thanks_training_data_05.csv', col_names = FALSE)
df2 <- df %>% rename(
  P1_1 = X1,
  P1_2 = X2,
  P1_3 = X3,
  P1_4 = X4,
  P1_5 = X5,
  P2_1 = X6,
  P2_2 = X7,
  P2_3 = X8,
  P2_4 = X9,
  P2_5 = X10,
  P3_1 = X11,
  P3_2 = X12,
  P3_3 = X13,
  P3_4 = X14,
  P3_5 = X15,
  PX_1 = X16,
  PX_2 = X17,
  PX_3 = X18,
  PX_4 = X19,
  PX_5 = X20,
  C1 = X21,
  C2 = X22,
  C3 = X23,
  CX = X24,
  A = X25
) %>%
  mutate(n_cards_1 = P1_1 + P1_2 + P1_3 + P1_4 + P1_5,
         n_cards_2 = P2_1 + P2_2 + P2_3 + P2_4 + P2_5,
         n_cards_3 = P3_1 + P3_2 + P3_3 + P3_4 + P3_5,
         n_cards_x = PX_1 + PX_2 + PX_3 + PX_4 + PX_5,
         cards_out = n_cards_1 + n_cards_2 + n_cards_3 + n_cards_x,
        active_card = case_when(PX_1 == 1 ~ 1,
                                PX_2 == 1 ~ 2,
                                PX_3 == 1 ~ 3,
                                PX_4 == 1 ~ 4,
                                PX_5 == 1 ~ 5,
                                TRUE ~ -1)
  )
df2 %>% filter(cards_out == 1) %>%
  select(active_card, A, n_cards_1, n_cards_2, n_cards_3, C1, C2, C3, CX)
temp <- df2 %>% filter(cards_out == 2, n_cards_1 == 1, C1 > 0) %>%
  select(P1_1, P1_2, P1_3, P1_4, P1_5, active_card, n_cards_1, n_cards_2, n_cards_3, C1, C2, C3, CX, A) %>%
  arrange(active_card)

dt <- read_csv('2024-02-20_no_thanks_tree_01.csv')
turn1 <- dt %>% filter(current_player == 0, n_cards_left == 3)
turn2 <- dt %>% filter(current_player == 1, n_cards_left == 2, p1_cards == "(1,)")

# TAKE = 0, PASS = 1
nrow(dt) # 10,001
dt %>% filter(action == 1) # 
nrow(dt %>% filter(action == 1)) # 2,834
dt %>% filter((current_player == 0 & p1_chips > 0) |
                (current_player == 1 & p2_chips > 0) |
                (current_player == 2 & p3_chips > 0))
