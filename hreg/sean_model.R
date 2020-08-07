require(lme4)
require(lmerTest)
df <- read.csv(file="/home/sean/Code/d3m-sequences/edit_distance/toR.csv")
df$diversity <- df$l1_zscore + df$linf_zscore

modA <- function() {
  m <- lm(max_score_zscore ~ l1_zscore + linf_zscore + count_zscore, data=df)
  return(m)
}

modB <- function() {
  m <- lm(max_score_zscore ~ l1_zscore + linf_zscore + count_zscore + as.factor(category), data=df)
  return(m)
}

modBprime <- function() {
  m <- lm(max_score_zscore ~ I(l1_zscore + linf_zscore) + count_zscore + as.factor(category), data=df)
  return(m)
}
modC <- function() {
  coef_mat <- matrix(0, nrow=length(unique(df$category)), ncol=3)
  for (c in unique(df$category)){
    dat <- df[df$category==c,]
    m <- lm(max_score_zscore ~ l1_zscore + linf_zscore + count_zscore, data = dat)
    ind <- which(unique(df$category)==c)
    coefs <- coefficients(m)[2:4]
    coef_mat[ind,] <- coefs
  }
  rownames(coef_mat) <- unique(df$category)
  colnames(coef_mat) <- c('l1_zscore','linf_zscore','count_zscore')
  return(coef_mat)
}

modCprime <- function() {
  coef_mat <- matrix(0, nrow=length(unique(df$category)), ncol=2)
  for (c in unique(df$category)){
    dat <- df[df$category==c,]
    m <- lm(max_score_zscore ~ I(l1_zscore + linf_zscore) + count_zscore, data = dat)
    print(summary(m))
    ind <- which(unique(df$category)==c)
    coefs <- coefficients(m)[2:3]
    coef_mat[ind,] <- coefs
  }
  rownames(coef_mat) <- unique(df$category)
  colnames(coef_mat) <- c('I(l1_zscore+linf_zscore)','count_zscore')
  return(coef_mat)
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

modEprime <- function() {
  m <- lmer(max_score_zscore ~ diversity + count_zscore + (diversity + count || category),
            data=df)
  return(m)
}
