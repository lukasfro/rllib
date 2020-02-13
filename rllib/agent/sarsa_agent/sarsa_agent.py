"""Implementation of vanilla SARSA Algorithm."""

from .abstract_sarsa_agent import AbstractSARSAAgent


class SARSAAgent(AbstractSARSAAgent):
    """Implementation of SARSA (On-Line)-Control."""

    def _td(self, state, action, reward, next_state, done, next_action):
        pred_q = self.q_function(state, action)

        target_q = self.q_function(next_state, next_action)
        target_q = reward + self.gamma * target_q * (1 - done)

        return pred_q, target_q