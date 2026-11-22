# \# Model Selection

# 

# \## The question

# This model decides whether a telecom customer will churn (cancel their subscription).

# A false negative means a churning customer is not flagged, so the business loses them with no retention offer.

# 

# \## Candidates

# 

# | Candidate         | Why I tried it                        | AUC   | F1    | F1 lowest slice | p95 latency (ms) | Size (KB) | MLflow run ID    |

# |-------------------|---------------------------------------|-------|-------|-----------------|------------------|-----------|------------------|

# | logreg            | Fast, interpretable baseline          | 0.798 | 0.495 | check MLflow    | 6.7              | 4         | 7e59e0e8         |

# | random\_forest     | Handles non-linear patterns           | 0.759 | 0.454 | check MLflow    | 26.6             | 3160      | 64a7b8fe         |

# | gradient\_boosting | Strong ensemble, good on imbalanced   | 0.748 | 0.417 | check MLflow    | 7.1              | 142       | 851a6651         |

# 

# \## The champion

# I picked \*\*logreg\*\* (Logistic Regression).

# It had the highest AUC (0.798) and F1 (0.495), the lowest p95 latency (6.7 ms), and the smallest size (4 KB).

# I accepted losing the ability to capture complex non-linear patterns that tree-based models offer.

# 

# \## My promotion rules

# Latency budget (p95): 100 ms, because the API must respond in under 100 ms for a real-time retention system.

# Minimum gain to replace the champion (F1 points): 0.01, because a smaller gain does not justify the risk of a new deployment.

# 

# \## What I would check next

# The F1 on Month-to-Month contract customers: this is the highest-churn slice and if the model performs poorly there, the business impact is large even if overall F1 looks acceptable.

