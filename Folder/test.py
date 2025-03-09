def knapsack_with_bonuses(weights, values, W, bonuses):
    n = len(weights)
    
    # Initialize a DP table
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    
    # Fill the DP table
    for i in range(1, n + 1):
        for w in range(W + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    
    # Apply bonuses
    for items, bonus in bonuses:
        total_weight = sum(weights[i - 1] for i in items)
        total_value = sum(values[i - 1] for i in items) + bonus
        
        for w in range(W, total_weight - 1, -1):
            dp[n][w] = max(dp[n][w], dp[n][w - total_weight] + total_value)
    
    return dp[n][W]

# Example usage
# Example usage
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
W = 9
bonuses = [([1, 4], 5)] # Bonus for selecting items with indices 1 and 4

result = knapsack_with_bonuses(weights, values, W, bonuses)
print(result)
