require(lme4)
require(lmerTest)
df <- read.csv(file="/home/sean/Code/d3m-sequences/edit_distance/toR.csv")

modA <- function() {
  m <- lm(max_score_zscore ~ l1_zscore + linf_zscore + count_zscore, data=df)
  return(m)
}

modB <- function() {
  m <- lm(max_score_zscore ~ l1_zscore + linf_zscore + count_zscore + as.factor(category), data=df)
  return(m)
}

modC <- function() {
  ms = c()
  for (c in unique(df$category)){
    dat <- df[df$category==c,]
    m <- lm(max_score_zscore ~ l1_zscore + linf_zscore + count_zscore, data = dat)
    ms <- c(ms,m)
  }
  return(ms)
}

modD <- function() {
  m <- lmer(max_score_zscore ~ l1_zscore + linf_zscore + count_zscore + (1|category), data=df)
  return(m)
}

modE <- function() {
  m <- lmer(max_score_zscore ~ l1_zscore + linf_zscore + count_zscore + 
             (l1_zscore|category) + (linf_zscore|category) + (count_zscore|category),
           data=df)
  return(m)
}
