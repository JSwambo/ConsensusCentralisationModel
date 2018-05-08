# ConsensusCentralisationModel

An implementation of a highly simplified model of the dynamics of mining pools in Bitcoin-like systems.
The initial model (in its simplest form) assumes the following:
* Mining agents have one of three types of preferences; risk-averse, risk-neutral, and risk-seeking.
* These preferences translate into action based on a set of probabilities p_join, p_create, and p_dn (do nothing).
* Since decisions are only based on a generic set of risk preferences, and no calculation about expected utility is explicitly being done (in this version of the model), then properties such as compute power (total and relative), reward, fees (network and pool operator), network difficulty, and block time need not be considered. 
* Initially there are no pools. At each round/ time step/ block, solo miners choose whether or not to create or join a pool, or to remain solo. The simulation algorithm assumes that the first actions in a round are the creation of new pools, such that miners who decide to join a pool can join newly created ones in that same round. 
* The choice of which pool to join with is based on the stochastic preferential attachment model. I.e. the larger the pool, the higher the probability that a solo miner joins that pool. The motivation for preferential attachment is that a larger pool will minimise payout uncertainty risk. 
* No switching or merging of pools is considered.

