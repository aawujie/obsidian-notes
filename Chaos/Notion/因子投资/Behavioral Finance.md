---
notion-id: 30378d23-e296-80ef-ad3a-edcf408e82ed
base: "[[因子投资.base]]"
Last edited time: 2026-02-11T18:43:00
Tags: []
Verification: unverified
Owner:
  - 杰 吴
---
该系列文章的核心观点在于：**量化投资中的“因子”（Factors）不仅仅是系统性风险的补偿，更多时候是市场参与者非理性行为导致的错误定价（Mispricing）。**[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]

---

### 核心框架：行为金融学的两大支柱

传统金融学建立在“理性人”和“有效市场假说”（EMH）之上，而行为金融学则基于**两大支柱**来解释市场异象：

1. **心理学（Psychology）：** 解释为什么投资者会犯错（产生非理性交易）。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]
2. **套利限制（Limits to Arbitrage）：** 解释为什么聪明钱（Smart Money）无法完全纠正这些错误（导致错误定价持续存在）。

---

### 第一支柱：心理学（投资者为什么犯错？）[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFI6BSGu54uWYS4XrDRykt63KojIwbS3dhZLAt_mwIOJfzQUBsi8JpVCxo6TY7ychBNgMrkuVrxcxiyv7rnHO9ZsHOvo-tdKu2UqlmnR_0zq8DWRTHFiAAWuYeaZXitW3geV_thMoTZglq4Qv098vg8Gg%3D%3D)]

文章将投资者的非理性行为细分为三个维度：

### 1. 预期中的偏差 (Biases in Beliefs)

投资者在形成对未来的预期时，并非像贝叶斯公式那样理性更新信息。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]

- **过度自信 (Overconfidence)：** 投资者高估自己的知识和预测能力，导致过度交易（Over-trading）和低估风险。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]
- **代表性偏差 (Representativeness)：** 倾向于根据近期的表现简单外推未来（如：认为过去涨的股票未来还会涨），这是导致**动量（Momentum）**和**反转（Reversal）**效应的重要原因。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]
- **锚定效应 (Anchoring)：** 过于依赖某个特定的参考点（如买入成本、历史高点）来做决策。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]
- **保守主义 (Conservatism)：** 对新信息的反应过慢，导致价格对信息的反应不足（Under-reaction）。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]

### 2. 风险偏好中的偏差 (Biases in Preferences)

投资者对风险的态度并非恒定不变，也非完全理性。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFI6BSGu54uWYS4XrDRykt63KojIwbS3dhZLAt_mwIOJfzQUBsi8JpVCxo6TY7ychBNgMrkuVrxcxiyv7rnHO9ZsHOvo-tdKu2UqlmnR_0zq8DWRTHFiAAWuYeaZXitW3geV_thMoTZglq4Qv098vg8Gg%3D%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHI5PtOdon57uwNfQwqtAiZJ_m5erhFQIzrsUypGiQ2dtw_02Ir3R9CfxWP9Nm7A_Ak5wAf1jxItP0CUS-vtP9MwZATFmQJ3e3xx3bKYR0Dhb8aVs6MbkNVwk4BVHyjeezsyi1gBSFEFUT8azA%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGfkywAgguBgQh0c40WWdrOtp_qotS61FHm-O0ctRLBTmeSiL7ku7hbttQinBshns7OE7S1ZrvVQYhe-iW3Ipw5v7vAdz9jae8zKorwLkhvJQfQQvxa79NXgByRK_KYXInrEytuAyDdGmmHRjDkO8OFyI0yFjRbr-AkjVoZ8PUXfQqzPkAFNs8UFXFd84u6o1-OGCpvuOw611eCtjDYsSOtPF3h)]

- **前景理论 (Prospect Theory) & 损失厌恶 (Loss Aversion)：**
    - 人对“亏损”的痛苦感远大于同等金额“盈利”的快乐感（通常是2倍以上）。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]
    - 导致投资者**“过早止盈，死扛亏损”**（处置效应，Disposition Effect）。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]
- **模糊厌恶 (Ambiguity Aversion)：** 相比于已知概率的风险，人们更讨厌未知概率的不确定性。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]

### 3. 认知限制 (Cognitive Limits)

- **注意力有限 (Limited Attention)：** 大脑无法瞬间处理所有市场信息。投资者倾向于关注那些“显眼”的股票（如新闻头条、涨停股），而忽略那些隐蔽但重要的信息。这解释了为什么财报发布后的价格漂移（PEAD）现象存在。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]

---

### 第二支柱：套利限制 (为什么错误定价不消失？)

既然市场有非理性的人送钱，为什么理性的套利者不把价格打回原形？因为套利是有风险和成本的。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]

3. **基本面风险 (Fundamental Risk)：** 即使你买入被低估的股票，基本面可能进一步恶化。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]
4. **噪音交易者风险 (Noise Trader Risk)：** “市场在证明你正确之前，可能先把你消灭。”[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)] 价格被非理性推高后，可能在短期内进一步推高，导致做空者爆仓。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]
5. **实施成本 (Implementation Costs)：** 交易佣金、冲击成本、卖空限制（做空不仅成本高，有时甚至无法借到券）。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]

**结论：** 由于套利限制的存在，非理性行为导致的价格偏离（Alpha）无法被迅速抹平，从而形成了可持续的因子收益。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]

---

### 行为金融学与因子投资 (Application)[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFI6BSGu54uWYS4XrDRykt63KojIwbS3dhZLAt_mwIOJfzQUBsi8JpVCxo6TY7ychBNgMrkuVrxcxiyv7rnHO9ZsHOvo-tdKu2UqlmnR_0zq8DWRTHFiAAWuYeaZXitW3geV_thMoTZglq4Qv098vg8Gg%3D%3D)][[5](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHy3yoePfVSQ53rEahW5_xNihu0QfxrwptqWhPs8J_mAWpWhaW-Cc4Be4aq9ah_DIC48njnmMAhJHC5viDkNe5KEBBjG09AJwCr5zdXrkEEtZrcA-yx)][[6](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQE4YhuBTjx_rrqgfu7DkZkqDgOKGoy9W_j2wx6_app_oAynvDczregq-6e6Q-SAKw4R36V37xpy7uqUY5FYnu-YPNqfPIkjzB5LO0gvZPAFFKHTvCqWnwrI6yM%3D)]

该小册子最终将理论落地到具体的**因子投资**上：

- **价值因子 (Value)：** 并非仅是风险补偿，更多是对**过度反应**的修正。投资者对坏消息反应过度，导致股价跌过头，随后均值回归。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]
- **动量因子 (Momentum)：** 源于**反应不足**（Under-reaction）和**追涨杀跌**。投资者初期对好消息反应不够（导致价格慢慢涨），后期又因羊群效应过度追入。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]
- **低波因子 (Low Volatility)：** 解释了“彩票型股票”的溢价。由于投资者喜欢博取小概率的高收益（像买彩票一样买高波动股票），导致这类股票价格被高估，长期回报反而低。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]

### 总结 (Key Takeaways)

6. **人是有限理性的：** 市场并不是完全有效的，因为人不仅会犯错，而且会犯系统性的、可预测的错。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]
7. **Alpha 的来源：** 许多因子的超额收益，本质上是你在赚取那些“受行为偏差影响的投资者”的钱。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]
8. **理解痛苦：** 了解行为金融学不仅是为了进攻（寻找因子），也是为了防守（避免自己成为那个非理性的“韭菜”）。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)]

Sources  help

9. [quant-wiki.com](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEUmpAS1Zr-SUccF0S-qmk4ZxKVXQfT8NlD-q-ujI55S64YBhhyth9xWmJ80-LiJ7tUQAc8ZV7DEkWkNM-SjxEkGi9bbJt66_O23PlEiIcc4Qp74Q-iIaZ87btLA4NxWbapU4j9eP8dWLzNyVd2AfTBH_iwQZwjEq5Ywr8%3D)
10. [creighton.edu](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFI6BSGu54uWYS4XrDRykt63KojIwbS3dhZLAt_mwIOJfzQUBsi8JpVCxo6TY7ychBNgMrkuVrxcxiyv7rnHO9ZsHOvo-tdKu2UqlmnR_0zq8DWRTHFiAAWuYeaZXitW3geV_thMoTZglq4Qv098vg8Gg%3D%3D)
11. [wikipedia.org](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHI5PtOdon57uwNfQwqtAiZJ_m5erhFQIzrsUypGiQ2dtw_02Ir3R9CfxWP9Nm7A_Ak5wAf1jxItP0CUS-vtP9MwZATFmQJ3e3xx3bKYR0Dhb8aVs6MbkNVwk4BVHyjeezsyi1gBSFEFUT8azA%3D)
12. [corporatefinanceinstitute.com](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGfkywAgguBgQh0c40WWdrOtp_qotS61FHm-O0ctRLBTmeSiL7ku7hbttQinBshns7OE7S1ZrvVQYhe-iW3Ipw5v7vAdz9jae8zKorwLkhvJQfQQvxa79NXgByRK_KYXInrEytuAyDdGmmHRjDkO8OFyI0yFjRbr-AkjVoZ8PUXfQqzPkAFNs8UFXFd84u6o1-OGCpvuOw611eCtjDYsSOtPF3h)
13. [factorwar.com](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHy3yoePfVSQ53rEahW5_xNihu0QfxrwptqWhPs8J_mAWpWhaW-Cc4Be4aq9ah_DIC48njnmMAhJHC5viDkNe5KEBBjG09AJwCr5zdXrkEEtZrcA-yx)
14. [shichuan.info](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQE4YhuBTjx_rrqgfu7DkZkqDgOKGoy9W_j2wx6_app_oAynvDczregq-6e6Q-SAKw4R36V37xpy7uqUY5FYnu-YPNqfPIkjzB5LO0gvZPAFFKHTvCqWnwrI6yM%3D)

### Google Search Suggestions

Display of Search Suggestions is required when using Grounding with Google Search. [ Learn more](https://ai.google.dev/gemini-api/docs/grounding/search-suggestions)

![[24px.svg]]

- ["behavioral finance"](https://www.google.com/search?q=%20%22behavioral%20finance%22&client=app-vertex-grounding&safesearch=active)
- [factorwar 行为金融学 笔记](https://www.google.com/search?q=factorwar%20%E8%A1%8C%E4%B8%BA%E9%87%91%E8%9E%8D%E5%AD%A6%20%E7%AC%94%E8%AE%B0&client=app-vertex-grounding&safesearch=active)
