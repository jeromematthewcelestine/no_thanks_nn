library(tidyverse)
library(rpart)

# TAKE = 0, PASS = 1

df <- read_csv('2024-02-20_no_thanks_training_data_05.csv', col_names = FALSE)
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
) %>% mutate(
  PD_1 = 1 - (P1_1 + P2_1 + P3_1 + PX_1),
  PD_2 = 1 - (P1_2 + P2_2 + P3_2 + PX_2),
  PD_3 = 1 - (P1_3 + P2_3 + P3_3 + PX_3),
  PD_4 = 1 - (P1_4 + P2_4 + P3_4 + PX_4),
  PD_5 = 1 - (P1_5 + P2_5 + P3_5 + PX_5),
  N1 = (P1_1 + P1_2 + P1_3 + P1_4 + P1_5),
  N2 = (P2_1 + P2_2 + P2_3 + P2_4 + P2_5),
  N3 = (P3_1 + P3_2 + P3_3 + P3_4 + P3_5),
  NX = (PX_1 + PX_2 + PX_3 + PX_4 + PX_5),
  NT = (N1 + N2 + N3 + NX),
  HaveAdjacent = as.numeric((PX_1 & P1_2) | 
                              (PX_2 & P1_1) | (PX_2 & P1_3) | 
                              (PX_3 & P1_2) | (PX_3 & P1_4) |
                              (PX_4 & P1_3) | (PX_4 & P1_5) |
                              (PX_5 & P1_4)),
  HaveBelow = as.numeric((PX_2 & P1_1) | 
                           (PX_3 & P1_2) |
                           (PX_4 & P1_3) |
                           (PX_5 & P1_4)),
  HaveAbove = as.numeric((PX_1 & P1_2) | 
                           (PX_2 & P1_3) |
                           (PX_3 & P1_4) |
                           (PX_4 & P1_5)),
)


tree <- rpart(data = df2,
      A ~ P1_1 + P1_2 + P1_3 + P1_4 + P1_5 + 
        P2_1 + P2_2 + P2_3 + P2_4 + P2_5 + 
        P3_1 + P3_2 + P3_3 + P3_4 + P3_5 + 
        PX_1 + PX_2 + PX_3 + PX_4 + PX_5 + 
        PD_1 + PD_2 + PD_3 + PD_4 + PD_5 +
        N1 + N2 + N3 + NX + NT + 
        HaveAdjacent + HaveAbove + HaveBelow +
        C1 + C2 + C3 + CX,
      method = 'class',
      control = rpart.control(minsplit = 1, maxdepth = 30, cp = 0.01, minbucket = 5))
tree
predictions <- predict(tree, data = df2, type = 'class')
pred_int <- as.numeric(predictions)-1
mean(abs(pred_int - df2$A))
plot(tree)

