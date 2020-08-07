# EDA and model for D3M Pipeline Data
# Nathan Danneman
# Begun: 05/08/2020
# Updated: 05/08/

dat <- read.csv(file="/home/sean/Code/d3m-sequences/edit_distance/toR.csv")

# quick look
head(dat)

# check for collinearity in diversity measures
cor(dat$linf, dat$l1) # 0.56, very correlated
plot(dat$linf, dat$l1)

# check for collinearity among other variables
cor(dat$count, dat$l1)  # 0.64, another strongly correlated pair
cor(dat$count, dat$linf) # essentially none

# quick check to make sure there is some unique variance here...
m <- lm(dat$l1 ~ dat$linf + dat$count)
summary(m)
# R-Squared = 0.73. So vast majority of l1 is a function of linf and count.

# Take a closer look at some variables
hist(dat$l1, breaks=30)  # lots of tiny values, some out to 1500
hist(dat$linf, breaks=30)
boxplot(dat$l1~dat$category) # not too strong correlation across category...

# So, we want to know if diversity (2 measures) affects 'mx'
boxplot(dat$max_score~dat$category)  # welp, that isn't helpful
hist(dat$max_score)
hist(dat$max_score[dat$max_score>0])
length(which(dat$max_score > 0)) / dim(dat)[1]  # 71% of data has max score > 0
# none are greater than one
# some are very negative
hist(dat$max_score[dat$max_score > -100])
boxplot(dat$max_score[dat$max_score > -100]~dat$category[dat$max_score > -100])  # welp, that isn't helpful
# clearly the max_score means very different things in different problem types
# or the data has been mis-coded or mangled elsewhere...

# more evidence the outcome variable is odd
#   often bounded between 0 and 1 with strong edge effects
#   often has wild range
cats <- unique(dat$category)
for (c in cats){
  print(c)
  print(summary(dat$max_score[dat$category==c]))
}

# linf looks better
for (c in cats){
  print(c)
  print(summary(dat$linf[dat$category==c]))
}

# l1 range and median vary wildly
for (c in cats){
  print(c)
  print(summary(dat$l1[dat$category==c]))
}

# check out a bivariate plot or two
plot(dat$l1[dat$max_score > -20], dat$max_score[dat$max_score > -20], col=as.numeric(as.factor(dat$category)))
# No way these slopes or intercepts are drawn from the same distribution

# Take a look at normalized versions...
plot(dat$l1_zscore, dat$max_score_zscore, col=as.numeric(as.factor(dat$category)))
plot(dat$linf_zscore, dat$max_score_zscore, col=as.numeric(as.factor(dat$category)))
# Very little evidence of correlation...
cor(dat$l1_zscore, dat$max_score_zscore)
# oops, some z-score versions are missing
which(is.na(dat$max_score_zscore))

table(dat$category)

# I'm starting to think think linear regression is a bad idea
# Also, because of how non-comparable the predictors *and* outcome measures are, HLM is a bad idea too
# Can't use the 'complete pooling' model because of non-comparabilities
# Many measures are very, very skewed, making me wary of simply normalizing (via z-score) the variables and charging onward

# Tentative plan: 
# Treating best as outcome and moving to logit paradigm
# This throws away lots of information, but helps handle limited-range dependent variables
# Could also build tiers to help recover some info (e.g. top-2, next-3, etc).

# Let's check it out quickly:
for (c in cats){
  print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
  mdat <- dat[dat$category==c,]
  mdat$binary <- as.logical(mdat$best)*1
  print(c)
  # make/get first PC
  d <- mdat[,c("l1", "linf")]
  pca_res <- prcomp(d, scale=TRUE)
  dist <- pca_res$x[,1]*-1

  mod <- glm(mdat$binary ~ dist + mdat$count)
  print(summary(mod))
}

# Not much evidence that diversity helps you have the best pipeline
# Mayyybe a tiny effect, but doubtful.


# Broaden to top2
for (c in cats){
  print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
  mdat <- dat[dat$category==c,]
  mdat$top2 <- (mdat$ranking < 3)*1
  print(c)
  # make/get first PC
  d <- mdat[,c("l1", "linf")]
  pca_res <- prcomp(d, scale=TRUE)
  dist <- pca_res$x[,1]*-1
  
  mod <- glm(mdat$top2 ~ dist + mdat$count)
  print(summary(mod))
}

# Still no effect.


