## Quick example script for hierarchical modeling

require(lme4)

# For simplicity of exposition, let's imagine 1 continuous explanatory variable, x,
#   one grouping variable, gpr, and a continous outcome, y.

# data for a varying-intercept model

N <- 100
x <- rnorm(N)
grp <- c(rep(1, 45), rep(2, 45), rep(3, 10))
intercept_values <- rnorm(3, 0, 2)
intercepts <- c(rep(intercept_values[1], 45), rep(intercept_values[2], 45), rep(intercept_values[3], 10))
grp_errors <- c(rnorm(45, 0, .8), rnorm(45, 0, 1.5), rnorm(10, 0, 1))
errors <- rnorm(N)
y <- intercepts + 1.5*x + grp_errors + errors
plot(x,y,col=grp, pch=19)

# Varying-intercept model.
# aka random effect on intercept, fixed effect on slope
vimod <- lmer(y ~ x + (1|grp)  )
summary(vimod)
intercept_values
coefficients(vimod)
est_intercepts <- coefficients(vimod)$grp[,1]
est_slope <- coefficients(vimod)$grp[1,2]
abline(est_intercepts[1], est_slope, col=1, lwd=2)
abline(est_intercepts[2], est_slope, col=2, lwd=2)
abline(est_intercepts[3], est_slope, col=3, lwd=2)



# data for a varying-intercept, varying-slope model

N <- 100
x <- rnorm(N)
grp <- c(rep(1, 45), rep(2, 45), rep(3, 10))
intercept_values <- rnorm(3, 0, 2)
slope_values <- norm(3, 1.5, .5)
slopes <- c(rep(slope_values[1], 45), rep(slope_values[2], 45), rep(slope_values[3], 10))
intercepts <- c(rep(intercept_values[1], 45), rep(intercept_values[2], 45), rep(intercept_values[3], 10))
grp_errors <- c(rnorm(45, 0, .8), rnorm(45, 0, 1.5), rnorm(10, 0, 1))
errors <- rnorm(N)
y <- intercepts + slopes*x + grp_errors + errors
plot(x,y,col=grp, pch=19)

# plot the truth...
abline(intercept_values[1], slope_values[1], col=1)
abline(intercept_values[2], slope_values[2], col=2)
abline(intercept_values[3], slope_values[3], col=3)

# Varying-intercept, varying-slope model.
# aka random effect on intercept and slope
vimod <- lmer(y ~ x + (x|grp)  )
summary(vimod)
coefficients(vimod)
intercept_values
slope_values
est_intercepts <- coefficients(vimod)$grp[,1]
est_slope <- coefficients(vimod)$grp[,2]
abline(est_intercepts[1], est_slope[1], col=1, lwd=2)
abline(est_intercepts[2], est_slope[2], col=2, lwd=2)
abline(est_intercepts[3], est_slope[3], col=3, lwd=2)


# Exercise for the reader:
# Group==3 is small. How would we go about showing that a hierarhcical model has
#  estimated a "better" intercept or slope for that group? How might we use repeated
#  simulations to show that hierarhcical modeling is better on average, even if not in all cases?


