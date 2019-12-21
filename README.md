# PID control visualizer
A simple visualization of how each parameter in a **P**roportional-**I**ntegral-**D**erivative controller works

## Math form
Let $$T(t)$$ as the target value at time t, $$M(t)$$ as the measured value at time t, $$e(t)=T(t)-M(t)$$ as the error at time t. A PID controller use the following formula to control the output $$u(t)$$:
$$u(t) = K_p e(t) + K_i \int_0^t e(t')~dt' + K_d \frac{de(t)}{dt}$$
where $$K_p, K_i, K_d$$ are the non-negative coefficients (gains) for the porportional, integral, and derivative operation, respectively.