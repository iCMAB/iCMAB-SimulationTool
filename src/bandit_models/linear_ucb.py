import numpy as np
import math

from src.utils import CONFIG
from .mab_model import MABModel


class LinearUCB(MABModel):
    def __init__(
            self,
            n_arms: int,
    ):
        super().__init__(n_arms)

        self.d = CONFIG["models"]["linear_ucb"]["d"]
        self.alpha = CONFIG["models"]["linear_ucb"]["alpha"]

        self.a = [np.identity(self.d)] * self.n_arms
        self.b = [np.zeros((self.d, 1))] * self.n_arms
        self.theta = [np.zeros((self.d, 1))] * self.n_arms

        # Initialize internal models of arm rewards
        self.arms = [_Arm(arm_index=i, d=self.d, alpha=self.alpha) for i in range(n_arms)]

    def select_arm(self, context: list[float]) -> int:
        self.context = np.ndarray((len(context),), buffer=np.array(context))

        highest_ucb = -1
        candidate_arms = []

        for arm_index in range(len(self.arms)):
            # Calculate ucb based on each arm using current covariates at time t
            arm_ucb = self.arms[arm_index].calculate_ucb(self.context)

            # Compare UCB to highest and update candidates accordingly
            if arm_ucb > highest_ucb:  # New highest resets candidate list
                highest_ucb = arm_ucb
                candidate_arms = [arm_index]
            elif arm_ucb == highest_ucb:  # Match highest adds to candidate list
                candidate_arms.append(arm_index)

        # Return random candidate
        self.arm_choice = np.random.choice(candidate_arms)
        return self.arm_choice

    def update_reward(self, reward: float) -> None:
        self.arms[self.arm_choice].update_dist(reward=reward, x_array=self.context)

    @property
    def name(self):
        return "Linear UCB"


class _Arm:
    def __init__(self, arm_index: int, d: int, alpha: float):
        self.index = arm_index
        self.alpha = alpha

        # A: (d x d) matrix = D_a.T * D_a + I_d.
        # The inverse of A is used in ridge regression
        self.a = np.identity(d)

        # b: (d x 1) corresponding response vector.
        # Equals to D_a.T * c_a in ridge regression formulation
        self.b = np.zeros([d, 1])

    def calculate_ucb(self, context) -> float:
        # Find A inverse for ridge regression
        a_inv = np.linalg.inv(self.a)

        # Perform ridge regression to obtain estimate of covariate coefficients theta
        theta = np.dot(a_inv, self.b)  # theta is (d x 1) dimension vector

        # Reshape covariates input into (d x 1) shape vector
        x = context.reshape([-1, 1])

        # Find ucb based on p formulation (mean + std_dev)
        # p is (1 x 1) dimension vector
        p = np.dot(theta.T, x) + self.alpha * np.sqrt(np.dot(x.T, np.dot(a_inv, x)))

        return p

    def update_dist(self, reward, x_array):
        # Reshape covariates input into (d x 1) shape vector
        x = x_array.reshape([-1, 1])

        # Update A which is (d * d) matrix.
        self.a += np.dot(x, x.T)

        # Update b which is (d x 1) vector
        # reward is scalar
        self.b += reward * x
