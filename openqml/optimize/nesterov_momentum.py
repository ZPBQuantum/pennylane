# Copyright 2018 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Nesterov momentum optimizer"""

import autograd

from .momentum import MomentumOptimizer
from .optimizer_utilities import _flatten, _unflatten


class NesterovMomentumOptimizer(MomentumOptimizer):
    r"""Gradient-descent optimizer with Nesterov momentum.

    Nesterov Momentum works like the :class:`Momentum optimizer <.openqml.optimize.MomentumOptimizer>`,
    but shifts the current input by the momentum term when computing the gradient of the cost:

    .. math:: a^{(t+1)} = m a^{(t)} + \eta \nabla f(x^{(t)} - m a^{(t)}).

    The user defined parameters are:

    * :math:`\eta`: the step size
    * :math:`m`: the momentum

    Args:
        stepsize (float): user-defined hyperparameter :math:`\eta`
        momentum (float): user-defined hyperparameter :math:`m`
    """
    def compute_grad(self, objective_fn, x, grad_fn=None):
        r"""Compute gradient of the objective_fn at at
        the shifted point :math:`(x - m\times\text{accumulation})`.

        Args:
            objective_fn (function): the objective function for optimization
            x (array): NumPy array containing the weights
            grad_fn (function): Optional gradient function of the
                objective function with respect to the weights ``x``.
                If ``None``, the gradient function is computed automatically.

        Returns:
            array: NumPy array containing the gradient :math:`\nabla f(x^{(t)})`
        """

        x_flat = _flatten(x)

        if self.accumulation is None:
            shifted_x_flat = list(x_flat)
        else:
            shifted_x_flat = [e - self.momentum * a for a, e in zip(self.accumulation, x_flat)]

        shifted_x = _unflatten(shifted_x_flat, x)[0]

        if grad_fn is not None:
            g = grad_fn(shifted_x)  # just call the supplied grad function
        else:
            # default is autograd
            g = autograd.grad(objective_fn)(shifted_x) # pylint: disable=no-value-for-parameter
        return g
